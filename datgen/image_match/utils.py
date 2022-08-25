from pathlib import Path
import json


ANNOT_PATH = Path('/Users/m_vilas/uni/software_engineering/DatGen/datasets/annot')


def compute_vg_occupancy():
    """Computes the occupancy of objects per image.

    Returns
    -------
    dict
        Containing an entry for each image/object.
    """
    with open(ANNOT_PATH/'vg'/'image_data.json', 'r') as f:
        img_info = json.load(f)
    img_size = {}
    for i in img_info:
        img_size[i['image_id']] = [i['height'], i['width']]

    with open(ANNOT_PATH/'vg'/'objects.json', 'r') as f:
        obj_info = json.load(f)
    
    vg_occ = {}
    for img in obj_info:
        img_id = img['image_id']
        try:
            img_h = img_size[img_id][0]
            img_w = img_size[img_id][1]
        except:
            continue
        vg_occ[img_id] = {}
        for obj in img['objects']:
            obj_name = obj['names'][0]
            h = obj['h']
            w = obj['w']
            vg_occ[img_id][obj_name] = (h * w) / (img_h * img_w)
    
    with open(ANNOT_PATH/'occ_vg.json', 'w') as f:
        json.dump(vg_occ, f)
    
    return vg_occ


if __name__ == '__main__':
    compute_vg_occupancy()