import json
from collections import OrderedDict

import pandas as pd

from datgen.config import ANNOT_PATH


def search_annotations(inputs):
    """Search input specification in the annotations of the Visual Genome and
    Conceptual Captions dataset.

    Parameters
    ----------
    inputs : Dict
        Contains information about each input specification

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


def search_vg(inputs):
    """Search Visual Genome dataset for input specification.

    Parameters
    ----------
    inputs : dict
        Containing input specifications obtained from website form.

    Returns
    -------
    Dict
       Image IDs divided by priorities of search.
    """
    # Load object and attribute information
    obj_info = load_vg_obj_info()

    attr_file = ANNOT_PATH / 'vg' / 'attributes.json'
    with open(attr_file, 'r') as f:
        attr_info = json.load(f)
    
    # Search inputs
    imgs = {}
    for obj, vals in inputs.items():    
        
        # Search object
        try:
            obj_name = vals['obj']
            imgs_obj = obj_info[obj_name]
            # Search visual attribute
            obj_attr = vals['vis_attr']
            imgs_attr = []
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
        except:
            imgs_obj = []
            imgs_attr = []
        
        # Search location
        try:
            imgs_loc = [obj_info[l] for l in vals['loc']]
            imgs_loc = [i for l in imgs_loc for i in l]
        except:
            imgs_loc = []

        # Divide into priorities
        imgs[obj] = divide_priorities(vals, imgs_obj, imgs_attr, imgs_loc)
    
    return imgs


def load_vg_obj_info():
    """Load dictionary of images per object in the Visual Genome dataset.

    Returns
    -------
    Dict
        Entry represents the images IDs per object name.
    """
    try:
        with open((ANNOT_PATH / 'vg' / 'object_info.json'), 'r') as f:
            obj_dict = json.load(f)
    except FileNotFoundError:
        attr_file = ANNOT_PATH / 'vg' / f'attributes.json'
        with open(attr_file, 'r') as f:
            attr_info = json.load(f)
        obj_dict = {}
        for img_info in attr_info:
            img_id = img_info['image_id']
            for obj in img_info['attributes']:
                obj_name = obj['names'][0]
                try:
                    obj_dict[obj_name] += [img_id]
                except KeyError:
                    obj_dict[obj_name] = [img_id]
        for obj_name, obj_vals in obj_dict.items():
            obj_dict[obj_name] = list(set(obj_vals))
        with open((ANNOT_PATH / 'vg' / 'object_info.json'), 'w') as f:
            json.dump(obj_dict, f)
    return obj_dict


def divide_priorities(vals, imgs_obj, imgs_attr, imgs_loc):
    """Divide images into priorities.

    Parameters
    ----------
    vals : dict
        Containing a "vis_attr", "loc" information.
    imgs_obj : list
        Image IDs related to object.
    imgs_attr : list
        Image IDs related to object with visual attribute.
    imgs_loc : list
        Image IDs related to location.

    Returns
    -------
    Dict
        Images divided into priorties.
    """
    imgs = {}
    if (vals['vis_attr'] != ['']) and (vals['loc'] != ['']):
        imgs['p1'] = [i for i in imgs_attr if i in imgs_loc]
        imgs['p2'] = [i for i in imgs_attr if i not in imgs['p1']]
        imgs['p3'] = list(set([
            i for i in (imgs_obj + imgs_loc)
            if (i not in imgs['p1']) & (i not in imgs['p2'])
        ]))
    elif (vals['vis_attr'] != ['']) and (vals['loc'] == ['']):
        imgs['p1'] = [i for i in imgs_attr]
        imgs['p2'] = [i for i in imgs_obj if i not in imgs['p1']]
        imgs['p3'] = []
    elif (vals['vis_attr'] == ['']) and (vals['loc'] != ['']):
        imgs['p1'] = [i for i in imgs_loc if i in imgs_obj]
        imgs['p2'] = [i for i in imgs_obj if i not in imgs['p1']]
        imgs['p3'] = [i for i in imgs_loc if i not in imgs['p1']]
    else:
        imgs['p1'] = imgs_obj
        imgs['p2'] = []
        imgs['p3'] = []
    return imgs


def search_cc(inputs):
    """Search Conceptual Captions dataset for input specification.

    Parameters
    ----------
    inputs : dict
        Containing input specifications obtained from website form.

    Returns
    -------
    dict
        Each entry represents an object and its related images IDs divided by
        priorities.
    """
    # Load label information
    labels = pd.read_csv(
        ANNOT_PATH / 'cc/classification_data.csv'
    )[['file', 'tags']]
    labels = labels.dropna()
    
    # Search inputs
    imgs = {}
    for obj, vals in inputs.items():

        # Search object
        obj_name = vals['obj']
        cc_info = get_cc_object_info(obj_name, labels)
        cc_info['file'] = cc_info['file'].apply(lambda x: x.split('.jpg')[0])
        imgs_obj = cc_info['file'].tolist()
        
        # Search visual attribute
        if vals['vis_attr'] != ['']:
            imgs_attr = [
                cc_info.loc[
                    cc_info['caption'].str.contains(vals['obj_attr'][i])
                ]['file'].tolist() for i in range(len(vals['obj_attr']))
            ]
            imgs_attr = [i for a in imgs_attr for i in a]
        else:
            imgs_attr = []

        # Search location
        if vals['loc'] != ['']:
            imgs_loc = [
                cc_info.loc[
                    cc_info['caption'].str.contains(vals['loc'][i])
                ]['file'].tolist() for i in range(len(vals['loc']))
            ]
            imgs_loc = [i for l in imgs_loc for i in l]
        else:
            imgs_loc = []

        # Divide into priorities
        imgs[obj] = divide_priorities(vals, imgs_obj, imgs_attr, imgs_loc)

    return imgs


def get_cc_object_info(obj, labels):
    """Get images of Conceptual Captions related to object, searching in the
    labels and captions information.

    Parameters
    ----------
    obj : str
        Name of object to look for.
    labels : pandas DataFrame
        Labels of each image in Conceptual Captions.

    Returns
    -------
    pandas DataFrame
       Image information related to object.
    """
    # Load captions
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