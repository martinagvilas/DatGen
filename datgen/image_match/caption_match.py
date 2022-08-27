from pathlib import Path
import json
import random

import clip
import torch

from .annot_search import search_annotations

# TODO: add warning to user if not enough images with occupancy are retrieved
# TODO: use images without occupancy if not enough are found


## PATH
current_path = Path().parent.resolve()
if 'm_vilas' in str(current_path):
    ANNOT_PATH = Path('/Users/m_vilas/uni/software_engineering/DatGen/datasets/annot')
    IMGS_PATH = Path('/Users/m_vilas/uni/software_engineering/DatGen/datasets/images')
else:
    ANNOT_PATH = Path('../../data/datgen_data/image_metas/annot')
    IMGS_PATH = Path('../../data/datgen_data/image_metas/images')


CAPTIONS_TYPE = ['all', 'obj', 'loc']
PRIORITY_IMGS = ['p1', 'p2', 'p3']


def compute_match(inputs):
    device = 'cpu'
    model, _ = clip.load('ViT-B/32', device)
    model.to(device)

    # Get matching images by annotations
    imgs_ids = search_annotations(inputs)

    # Load object occupancy
    occ = {}
    with open(ANNOT_PATH / 'occ_vg.json', 'r') as f:
        occ['vg'] = json.load(f)
    with open(ANNOT_PATH / 'occ_cc.json', 'r') as f:
        occ['cc'] = json.load(f)

    # Check images in annotations
    imgs = {o: {d: [] for d in imgs_ids.keys()} for o in inputs.keys()}
    temp_imgs = {o: {d: [] for d in imgs_ids.keys()} for o in inputs.keys()}
    for id, obj_info in inputs.items():
        # Get text features
        txt_fts = []
        for c in CAPTIONS_TYPE:
            captions = obj_info[f'captions_{c}']
            txt_ft = clip.tokenize(captions)
            with torch.no_grad():
                txt_ft = model.encode_text(txt_ft)
            txt_ft /= txt_ft.norm(dim=-1, keepdim=True)
            txt_fts.append(txt_ft)
        # Get image information
        n_imgs = obj_info['n_images']
        # Get images per priority
        for prio in PRIORITY_IMGS:
            # Get images per dataset
            for dataset in imgs_ids.keys():
                # Get image information from dataset and priority
                dataset_imgs = imgs_ids[dataset][id]
                p_imgs = dataset_imgs[prio]
                if p_imgs == []:
                    continue
                else:
                    all_imgs = [i for p in dataset_imgs.values() for i in p]
                    random_imgs = get_random_cc_imgs(all_imgs)
                    # Get embeddings of random images
                    random_ft = []
                    for i in random_imgs:
                        random_ft.append(torch.load(i))
                    random_ft = torch.squeeze(torch.stack(random_ft))
                    random_ft /= random_ft.norm(dim=-1, keepdim=True)
                    # Compute match
                    for i in p_imgs:
                        # Load image tensor
                        try:
                            img_ft = torch.load(IMGS_PATH / f'{dataset}' / f'{i}.pt')
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
                                for o, v in  occ[dataset][str(i)].items():
                                    if obj_info['obj'] in o:
                                        obj_occ = v
                                        break
                                if obj_occ >= obj_info['size_min']:
                                    imgs[id][dataset].append(i)
                            except:
                                temp_imgs[id][dataset].append(i)
                            # Break if all images have been found
                            if sum(len(v) for v in imgs[id].values()) >= n_imgs:
                                break
                    else:
                        continue
                    break
            else:
                continue
            break
    return imgs, inputs


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
