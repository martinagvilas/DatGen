import json
from pathlib import Path
from collections import OrderedDict

import pandas as pd

ANNOT_PATH = Path('../../data/datgen_data/image_metas/annot')


## Ideas for optimization
# VG: list of objects and only look if object is present
## --> same for CC but using labels and words of captions


def search_annotations(inputs):
    """_summary_ Searches annotations (captions, labels and other type of annotations)

    Parameters
    ----------
    inputs : Dict
        _description_

    Returns
    -------
    Dict
        Separate entry for each dataset and object requested. Each 
        dataset/object combination entry contains lists of images with three
        levels of priority: "p1" are the images in the dataset that match all
        user specifications; "p2" are the images that match at least one
        specification; "p3" are the images related to the object requested that
        do not match the specifications.
    """
    imgs_ids = OrderedDict()

    # Search Visual Genome dataset
    imgs_ids['vg'] = search_vg(inputs)

    # Search Conceptual Captions dataset
    imgs_ids['cc'] = search_cc(inputs)

    return imgs_ids


def search_cc(inputs):
    labels = pd.read_csv(ANNOT_PATH / 'cc/classification_data.csv')[['file', 'tags']]
    labels = labels.dropna()
    imgs = {}
    for obj, vals in inputs.items():
        imgs[obj] = {}
        obj_name = vals['obj']
        cc_info = get_cc_object_info(obj_name, labels)
        if vals['obj_attr'] != []:
            imgs_attr = [
                cc_info.loc[
                    cc_info['caption'].str.contains(vals['obj_attr'][i])
                ]['file'].tolist() for i in range(len(vals['obj_attr']))
            ]
            imgs_attr = [i for a in imgs_attr for i in a]
        if vals['loc'] != []:
            imgs_loc = [
                cc_info.loc[
                    cc_info['caption'].str.contains(vals['loc'][i])
                ]['file'].tolist() for i in range(len(vals['loc']))
            ]
            imgs_loc = [i for l in imgs_loc for i in l]
        match_imgs = imgs_attr + imgs_loc
        imgs[obj]['p1'] = [i.split('.jpg')[0] for i in imgs_attr if i in imgs_loc]
        imgs[obj]['p2'] = [i.split('.jpg')[0] for i in match_imgs if i not in imgs[obj]['p1']]
        imgs[obj]['p3'] = [
            i.split('.jpg')[0] for i in cc_info['file'].tolist()
            if (i not in imgs[obj]['p1']) & (i not in imgs[obj]['p2'])
        ]
    return imgs


def get_cc_object_info(obj, labels):
    ## TODO: search testing captions too

    captions_file = ANNOT_PATH / 'cc' / f'cc_training_captions.csv'
    captions = pd.read_csv(captions_file, sep=',')

    # Search by tag
    imgs_tag = labels.loc[labels['tags'].str.contains(obj)]['file']
    # Search by word
    imgs_captions = captions.loc[captions['caption'].str.contains(obj)]['file']
    # Get unique values
    imgs_ids = list(set(imgs_tag.tolist() + imgs_captions.tolist()))
    # Get object info
    object_info = captions.loc[captions['file'].isin(imgs_ids)]

    return object_info


def search_vg(inputs):
    # Load object dictionary
    try:
        with open((ANNOT_PATH / 'vg' / 'object_info.json'), 'r') as f:
            obj_info = json.load(f)
    except:
        obj_info = create_vg_obj_dict()

    # Search if requested objects are in dataset and if not return empty list
    obj_present = False
    for obj_vals in inputs.values():
        if obj_vals['obj'] in obj_info.keys():
            obj_present = True
            break
    if obj_present == False:
        return []

    # Search for attributes
    attr_file = ANNOT_PATH / 'vg' / 'attributes.json'
    with open(attr_file, 'r') as f:
        attr_info = json.load(f)
    imgs = {}
    for obj, vals in inputs.items():
        obj_name = vals['obj']
        obj_attr = vals['vis_attr']
        
        # Continue if object is not present in visual genome database
        try:
            imgs_obj = obj_info[obj_name]
        except:
            imgs[obj] = {}
            imgs[obj]['p1'] = []
            imgs[obj]['p2'] = []
            imgs[obj]['p3'] = []
            continue
        
        for img in attr_info:
            img_id = img['image_id']
            if img_id in imgs_obj:
                for i in img['attributes']:
                    try:
                        if (obj_name in i['names']) & \
                                (any(a in i['attributes'] for a in obj_attr)):
                            imgs_attr.append(img_id)
                    except:
                        continue
        imgs_attr = list(set(imgs_attr))
        imgs_loc = [obj_info[l] for l in vals['loc']]
        imgs_loc = [i for l in imgs_loc for i in l]

        imgs[obj] = {}
        imgs[obj]['p1'] = [i for i in imgs_attr if i in imgs_loc]
        match_imgs = imgs_attr + imgs_loc
        imgs[obj]['p2'] = [i for i in match_imgs if i not in imgs[obj]['p1']]
        imgs[obj]['p3'] = [i for i in imgs_obj if i not in match_imgs]

    return imgs


def create_vg_obj_dict():
    attr_file = ANNOT_PATH / 'vg' / f'attributes.json'
    with open(attr_file, 'r') as f:
        attr_info = json.load(f)
    obj_dict = {}
    for img_info in attr_info:
        img_id = img_info['image_id']
        for obj in img_info['attributes']:
            obj_name = obj['names'][0]
            try:
                # if img_id not in obj_dict[obj_name]:
                obj_dict[obj_name] += [img_id]
            except KeyError:
                obj_dict[obj_name] = [img_id]
    for obj_name, obj_vals in obj_dict.items():
        obj_dict[obj_name] = list(set(obj_vals))
    with open((ANNOT_PATH / 'vg' / 'object_info.json'), 'w') as f:
        json.dump(obj_dict, f)
    return obj_dict
