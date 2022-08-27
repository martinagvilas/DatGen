from pathlib import Path

import pandas as pd


ANNOT_PATH = Path('/Users/m_vilas/uni/software_engineering/DatGen/datasets/annot')

def fake_data():
    n_objs = 2
    input_info = {i: {} for i in range(n_objs)}
    
    input_info[0]['obj'] = 'Apple'
    input_info[0]['size_min'] = 50
    input_info[0]['vis_attr'] = 'red'.split(';')
    input_info[0]['loc'] = 'table'.split(';')
    input_info[0]['n_images'] = 100

    input_info[1]['obj'] = 'pizza'
    input_info[1]['size_min'] = 50
    input_info[1]['vis_attr'] = 'Greasy;round'.split(';')
    input_info[1]['loc'] = 'kitchen;plate'.split(';')
    input_info[1]['n_images'] = 100

    return input_info


# def test_get_cc_object_info():
#     labels = pd.read_csv(ANNOT_PATH/'classification_data.csv')[['file','tags']]