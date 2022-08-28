import random
import json

import clip
import torch

from datgen.config import IMGS_PATH
from datgen.input_prepro.object import DGObject


class MatchedObject(DGObject):
    """Object with corresponding searched and matched images.

    Parameters
    ----------
    DGObject : class
        Object with preprocessed specification values.
    """
    def __init__(self, vals):
        super(MatchedObject, self).__init__(vals)
        self.annot_ids = {}
        self.matched_imgs = []
        self.backup_imgs = []
    
    
    def search_vg(self, obj_info, attr_info):
        """Search the Visual Genome dataset for images matching specifications.

        Parameters
        ----------
        obj_info : dict
            Object information of the Visual Genome dataset.
        attr_info : list
            Attribute information of the Visual Genome dataset.

        Returns
        -------
        dict
            Image IDs matching inputs categorized by priorities.
        """
        # Search inputs
        imgs = {}
        # Search object
        try:
            imgs_obj = obj_info[self.obj_name]
            # Search visual attribute
            imgs_attr = []
            for img in attr_info:
                img_id = img['image_id']
                if img_id in imgs_obj:
                    for i in img['attributes']:
                        try:
                            if (self.obj_name in i['names']) & (any(
                                    a in i['attributes'] for a in self.vis_attr
                            )):
                                imgs_attr.append(img_id)
                        except:
                            continue
            imgs_attr = list(set(imgs_attr))
        except:
            imgs_obj = []
            imgs_attr = []
        
        # Search location
        try:
            imgs_loc = [obj_info[l] for l in self.loc]
            imgs_loc = [i for l in imgs_loc for i in l]
        except:
            imgs_loc = []

        # Divide into priorities
        self.annot_ids['vg'] = self.divide_priorities(
            imgs_obj, imgs_attr, imgs_loc
        )
        return imgs


    def divide_priorities(self, imgs_obj, imgs_attr, imgs_loc):
        """Divide images into match priorities.

        Parameters
        ----------
        imgs_obj : list
            Image IDs related to object.
        imgs_attr : list
            Image IDs related to object with visual attribute.
        imgs_loc : list
            Image IDs related to location.

        Returns
        -------
        Dict
            "p1" are the images in the dataset that match all user
            specifications; "p2" are the images that match at least one
            specification; "p3" are the images related to the object requested
            that do not match the specifications.
        """
        imgs = {}
        if (self.vis_attr != ['']) and (self.loc != ['']):
            imgs['p1'] = [i for i in imgs_attr if i in imgs_loc]
            imgs['p2'] = [i for i in imgs_attr if i not in imgs['p1']]
            imgs['p3'] = list(set([
                i for i in (imgs_obj + imgs_loc)
                if (i not in imgs['p1']) & (i not in imgs['p2'])
            ]))
        elif (self.vis_attr  != ['']) and (self.loc == ['']):
            imgs['p1'] = [i for i in imgs_attr]
            imgs['p2'] = [i for i in imgs_obj if i not in imgs['p1']]
            imgs['p3'] = []
        elif (self.vis_attr  == ['']) and (self.loc != ['']):
            imgs['p1'] = [i for i in imgs_loc if i in imgs_obj]
            imgs['p2'] = [i for i in imgs_obj if i not in imgs['p1']]
            imgs['p3'] = [i for i in imgs_loc if i not in imgs['p1']]
        else:
            imgs['p1'] = imgs_obj
            imgs['p2'] = []
            imgs['p3'] = []
        return imgs


    def search_cc(self, captions, labels):
        # Search inputs
        imgs = {}

        # Search object
        cc_info = get_cc_object_info(self.obj_name, captions, labels)
        cc_info['file'] = cc_info['file'].apply(lambda x: x.split('.jpg')[0])
        imgs_obj = cc_info['file'].tolist()
        
        # Search visual attribute
        if self.vis_attr != ['']:
            imgs_attr = [
                cc_info.loc[
                    cc_info['caption'].str.contains(self.obj_attr[i])
                ]['file'].tolist() for i in range(len(self.obj_attr))
            ]
            imgs_attr = [i for a in imgs_attr for i in a]
        else:
            imgs_attr = []

        # Search location
        if self.loc != ['']:
            imgs_loc = [
                cc_info.loc[
                    cc_info['caption'].str.contains(self.loc[i])
                ]['file'].tolist() for i in range(len(self.loc))
            ]
            imgs_loc = [i for l in imgs_loc for i in l]
        else:
            imgs_loc = []

        # Divide into priorities
        self.annot_ids['cc'] = self.divide_priorities(
            imgs_obj, imgs_attr, imgs_loc
        )
        return imgs


    def compute_match(self, model, occ):
        # Get caption embeddings
        txt_fts = []
        for captions in self.captions: 
            txt_ft = clip.tokenize(captions)
            with torch.no_grad():
                txt_ft = model.encode_text(txt_ft)
            txt_ft /= txt_ft.norm(dim=-1, keepdim=True)
            txt_fts.append(txt_ft)
        # Get images per priority and dataset
        for prio in ['p1', 'p2', 'p3']:
            for ds in self.annot_ids.keys():
                p_imgs = self.annot_ids[ds][prio]
                if p_imgs == []:
                    continue
                else:
                    # Get embeddings of random images
                    all_imgs = [
                        i for p in self.annot_ids[ds].values() for i in p
                    ]
                    random_imgs = get_random_cc_imgs(all_imgs)
                    random_ft = []
                    for i in random_imgs:
                        random_ft.append(torch.load(i))
                    random_ft = torch.squeeze(torch.stack(random_ft))
                    random_ft /= random_ft.norm(dim=-1, keepdim=True)
                    # Compute match
                    for i in p_imgs:
                        # Get image embedding
                        try:
                            img_ft = torch.load(IMGS_PATH / f'{ds}/{i}.pt')
                        except:
                            continue
                        img_ft /= img_ft.norm(dim=-1, keepdim=True)
                        # Append image tensor with random images
                        img_ft = torch.vstack([img_ft, random_ft])
                        # Compute match
                        topk_res = []
                        for txt_ft in txt_fts:
                            match = torch.squeeze((img_ft @ txt_ft.T), dim=0)
                            match = torch.mean(match, dim=1)
                            topk_res.append(match.topk(15)[1])
                        # Append image to dataset if it was found 
                        if all(0 in m for m in topk_res):
                            # Append to different lists depending on occupancy
                            try:
                                for o, v in  occ[ds][str(i)].items():
                                    if self.obj_name in o:
                                        obj_occ = v
                                        break
                                if obj_occ >= self.size_min:
                                    self.matched_imgs.append([i, ds])
                            except:
                                self.backup_imgs.append([i, ds])
                            # Break if all images have been found
                            if len(self.matched_imgs) >= self.n_images:
                                break
                    else:
                        continue
                    break
            else:
                continue
            break
        return self.matched_imgs


def get_cc_object_info(obj, captions, labels):
    # Search by tag
    imgs_tag = labels.loc[labels['tags'].str.contains(obj)]['file']
    # Search by word
    imgs_captions = captions.loc[captions['caption'].str.contains(obj)]['file']
    # Get unique values
    imgs_ids = list(set(imgs_tag.tolist() + imgs_captions.tolist()))
    # Get object info
    object_info = captions.loc[captions['file'].isin(imgs_ids)]

    return object_info


def get_random_cc_imgs(exclude_ids, n=300):
    """Get a set of random images IDs from Conceptual Captions that exclude some
    set of predefined IDs.

    Parameters
    ----------
    exclude_ids : list
        Image IDs to exclude from random generation.
    n : int, optional
        Number of random images, by default 300

    Returns
    -------
    list
        Image IDs randomly selected from Conceptual Captions.
    """
    imgs_paths = get_cc_imgs_paths()
    imgs = []
    while len(imgs) < n:
        random_img = imgs_paths.pop(random.randrange(len(imgs_paths)))
        if random_img.stem not in exclude_ids:
            imgs.append(random_img)
    return imgs


def get_cc_imgs_paths():
    """_summary_

    Returns
    -------
    _type_
        _description_
    """
    cc_imgs_file = IMGS_PATH / 'cc_imgs.json'
    if not cc_imgs_file.is_file():
        imgs_paths = list((IMGS_PATH / 'cc').iterdir())
        imgs_save = [str(p) for p in imgs_paths]
        with open(cc_imgs_file, 'w') as f:
            json.dump(imgs_save, f)
    else:
        with open(cc_imgs_file, 'r') as f:
            imgs_paths = json.load(f)
        imgs_paths = [IMGS_PATH / '/'.join(p.split('/')[8:]) for p in imgs_paths]
    return imgs_paths


