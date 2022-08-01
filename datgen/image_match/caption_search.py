from pathlib import Path

import pandas as pd


ANNOT_PATH = Path('/Users/m_vilas/uni/software_engineering/DatGen/datasets/')


def search_captions(inputs):
    cc_labels = pd.read_csv(ANNOT_PATH/'classification_data.csv')[['file', 'tags']]
    cc_labels = cc_labels.dropna()
    for obj, obj_vals in inputs.items():
        obj_name = obj_vals['obj']
        imgs = get_cc_object_info(obj_name, cc_labels)
    print('done')

    return imgs_ids


def get_cc_object_info(obj, labels):
    captions_file = ANNOT_PATH / f'cc_training_captions.csv'
    captions = pd.read_csv(captions_file, sep=',')

    # Look by tag
    imgs_ids_tag = labels.loc[labels['tags'].str.contains(obj)]['file']
    # Look by word
    imgs_ids_captions = captions.loc[captions['caption'].str.contains(obj)]['file']
    # Get unique values
    imgs_ids = list(set(imgs_ids_tag.tolist() + imgs_ids_captions.tolist()))
    # Get object info
    object_info = captions.loc[captions['file'].isin(imgs_ids)]

    return object_info