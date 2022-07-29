from pathlib import Path
from pycocotools.coco import COCO


ANNOT_PATH = Path('/Users/m_vilas/projects/multimodal-ck/dataset/annotations')


def search_captions(inputs):
    coco_captions = load_coco_captions()
    print('done')

    return imgs_ids


def load_coco_captions():
    # TODO: both for training and testing data
    captions_path = ANNOT_PATH / f'coco_train2017_captions.json'
    coco_caps = COCO(captions_path)
    ann_ids = coco_caps.getAnnIds(imgIds=[], iscrowd=None)
    captions = []
    for ann_id in ann_ids:
        caption = coco_caps.loadAnns(ann_id)[0]['caption']
        captions.append(caption)
    return captions