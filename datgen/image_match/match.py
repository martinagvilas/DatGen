import json

import clip

from datgen.config import ANNOT_PATH
from datgen.image_match.search import search_annot


def match(inputs):

    # Search annotations
    searched_objs = search_annot(inputs)

    # Load object occupancy
    occ = {}
    with open(ANNOT_PATH / 'occ_vg.json', 'r') as f:
        occ['vg'] = json.load(f)
    with open(ANNOT_PATH / 'occ_cc.json', 'r') as f:
        occ['cc'] = json.load(f)

    # Load model
    device = 'cpu'
    model, _ = clip.load('ViT-B/32', device)
    model.to(device)

    # Match objects
    for obj in searched_objs:
        obj.compute_match(model, occ)
    
    return searched_objs