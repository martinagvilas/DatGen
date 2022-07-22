from pathlib import Path

from pycocotools.coco import COCO

def load_coco_captions(annotations_path, partition='train'):
    captions_path = Path(annotations_path) / f'coco_{partition}2017_captions.json'
    coco_caps = COCO(captions_path)
    ann_ids = coco_caps.getAnnIds(imgIds=[], iscrowd=None)
    captions = []
    for ann_id in ann_ids:
        caption = coco_caps.loadAnns(ann_id)[0]['caption']
        captions.append(caption)
    return captions