from pathlib import Path

import pandas as pd


ANNOT_PATH = Path('/Users/m_vilas/uni/software_engineering/DatGen/datasets/')


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
    imgs_ids = {}

    # Search Conceptual Captions dataset
    imgs_ids['cc'] = search_cc(inputs)

    # TODO: Search Visual Genome dataset

    # TODO: Search Open Images dataset

    return imgs_ids


def search_cc(inputs):
    labels = pd.read_csv(ANNOT_PATH/'classification_data.csv')[['file','tags']]
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
            imgs_loc = [i for l in imgs_attr for i in l]
        match_imgs = imgs_attr + imgs_loc
        imgs[obj]['p1'] = [i for i in imgs_attr if i in imgs_loc]
        imgs[obj]['p2'] = [i for i in match_imgs if i not in imgs[obj]['p1']]
        imgs[obj]['p3'] = [
            i for i in cc_info['file'].tolist() 
            if (i not in imgs[obj]['p1']) & (i not in imgs[obj]['p2'])
        ]
    return imgs


def get_cc_object_info(obj, labels):
    captions_file = ANNOT_PATH / f'cc_training_captions.csv'
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