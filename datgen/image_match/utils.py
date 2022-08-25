from pathlib import Path
import json


ANNOT_PATH = Path('/Users/m_vilas/uni/software_engineering/DatGen/datasets/annot')


def compute_vg_occupancy():
    with open(ANNOT_PATH/'vg'/'image_data.json', 'r') as f:
        img_info = json.load(f)
    with open(ANNOT_PATH/'vg'/'objects.json', 'r') as f:
        obj_info = json.load(f)
    
    vg_occ = {}
    for img in obj_info:
        img_id = img['image_id']
        try:
            img_w = img_info[img_id]['width']
            img_h = img_info[img_id]['height']
        except:
            continue
        vg_occ[img_id] = {}
        for obj in img['objects']:
            obj_name = obj['names'][0]
            h = obj['h']
            w = obj['w']
            vg_occ[img_id][obj_name] = (h * w) / (img_h * img_w)
    
    with open(ANNOT_PATH/'occ_vg.json', 'r') as f:
        json.dump(vg_occ, f)
    
    return vg_occ