from pathlib import Path
import json
import random
from re import I

import clip
import torch

from datgen.image_match.annot_search import search_annotations


IMGS_PATH = Path('/Users/m_vilas/uni/software_engineering/DatGen/datasets/images')

# TODO: for loop should be by dataset
# TODO: define n images
# TODO: convert priority images into loop
# TODO: save hihgly matching images
## TODO: reduce number of captions

def compute_match(inputs, n_imgs):
    device='cpu'
    model, _ = clip.load('ViT-B/32', device)
    model.to(device)

    # Get matching images by annotations
    imgs_ids = search_annotations(inputs)
    
    # Check images in annotations
    for obj in inputs.keys():
        imgs = {}
        for dataset in imgs_ids.keys():
            dataset_imgs = imgs_ids[dataset][obj]
            imgs[dataset] = []
            # Compute caption features
            captions = inputs[obj]['captions_obj_attr']
            txt = clip.tokenize(captions)
            with torch.no_grad():
                txt_ft = model.encode_text(txt)
            txt_ft /= txt_ft.norm(dim=-1, keepdim=True)
                        # Get text embeddings
            # TODO: change to final captions
            txt_ft = clip.tokenize(inputs[obj]['captions_obj_attr'])
            with torch.no_grad():
                txt_ft = model.encode_text(txt_ft)
            txt_ft /= txt_ft.norm(dim=-1, keepdim=True)
            # Get images ids
            p1_imgs = dataset_imgs['p1']
            p2_imgs = dataset_imgs['p2']
            p3_imgs = dataset_imgs['p3']
            all_imgs = p1_imgs + p2_imgs + p3_imgs
            random_imgs = get_random_cc_imgs(all_imgs)
            # Get embeddings of random images
            random_ft = []
            for i in random_imgs:
                random_ft.append(torch.load(i))
            random_ft = torch.squeeze(torch.stack(random_ft))
            random_ft /= random_ft.norm(dim=-1, keepdim=True)

            # Compute priority 1 images match
            # TODO: convert this into for loop for all priorities
            for prio, imgs_ids in dataset_imgs.items():
                if imgs_ids == []:
                    continue
                else:
                    for i in imgs_ids:
                        # Load image tensor
                        img_ft = torch.load(IMGS_PATH/f'{dataset}' / f'{i}.pt')
                        img_ft /= img_ft.norm(dim=-1, keepdim=True)
                        # Append image tensor with random images
                        img_ft = torch.vstack([img_ft, random_ft])
                        # Compute match
                        match = torch.squeeze((img_ft @ txt_ft.T), dim=0)
                        match = torch.mean(match, dim=1)
                        if 0 in match.topk(10)[1]:
                            imgs[dataset].append(i)
                        if (len(imgs['cc']) + len(imgs['vg'])) >= n_imgs:
                            break # TODO: check this break works as intender
                        # TODO: save other topk for later inspection

    # Check other images if not annotations
    # get other topk for inspection
    return


def get_cc_imgs_paths():
    cc_imgs_file = IMGS_PATH / 'cc_imgs.json'
    if not cc_imgs_file.is_file():
        imgs_paths = list((IMGS_PATH / 'cc').iterdir())
        imgs_save = [str(p) for p in imgs_paths]
        with open(cc_imgs_file, 'w') as f:
            json.dump(imgs_save, f)
    else:
        with open(cc_imgs_file, 'r') as f:
            imgs_paths = json.load(f)
        imgs_paths = [Path(p) for p in imgs_paths]
    return imgs_paths


def get_random_cc_imgs(exclude_ids, n=300):
    imgs_paths = get_cc_imgs_paths()
    imgs = []
    while len(imgs) < n:
        random_img = imgs_paths.pop(random.randrange(len(imgs_paths)))
        if random_img.stem not in exclude_ids:
            imgs.append(random_img)
    return imgs