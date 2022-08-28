import json

import pandas as pd

from datgen.config import ANNOT_PATH
from datgen.image_match.object import MatchedObject


def search_annot(inputs):
    """Search Visual Genome and Conceptual Captions datasets for annotations
    that match user requirements.

    Parameters
    ----------
    inputs : dict
        Each entry contains the input specifications for each object.

    Returns
    -------
    list of classes
        Objects with imgs IDs from both datasets that meet the requirements.
    """
    objs = []
    for obj, obj_vals in inputs.items():
        objs.append(MatchedObject(obj_vals))

    # Search in Visual Genome
    vg_obj = load_vg_obj_info()
    vg_attr = load_vg_attr_info()
    for obj in objs:
        obj.search_vg(vg_obj, vg_attr)
    del vg_attr
    del vg_obj

    # Search in Conceptual Captions
    cc_captions = load_cc_captions()
    cc_labels = load_cc_labels()
    for obj in objs:
        obj.search_cc(cc_captions, cc_labels)
    del cc_captions
    del cc_labels

    return objs


def load_vg_attr_info():
    attr_file = ANNOT_PATH / 'vg' / 'attributes.json'
    with open(attr_file, 'r') as f:
        attr_info = json.load(f)
    return attr_info


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


def load_cc_labels():
    labels = pd.read_csv(ANNOT_PATH / 'cc/classification_data.csv')
    labels = labels[['file', 'tags']]
    labels = labels.dropna()
    return labels


def load_cc_captions():
    captions_file = ANNOT_PATH / 'cc' / f'cc_training_captions.csv'
    captions = pd.read_csv(captions_file, sep=',')
    return captions
