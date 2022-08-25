from pathlib import Path
import json
import random

import clip
import torch

from datgen.image_match.annot_search import search_annotations

IMGS_PATH = Path('/Users/m_vilas/uni/software_engineering/DatGen/datasets/images')

CAPTIONS_TYPE = ['all', 'obj', 'loc']

PRIORITY_IMGS = ['p1', 'p2', 'p3']


# TODO: save highly matching images

def compute_match(inputs):
    device = 'cpu'
    model, _ = clip.load('ViT-B/32', device)
    model.to(device)

    # Get matching images by annotations
    imgs_ids = search_annotations(inputs)

    # Check images in annotations
    imgs = {o: {d: [] for d in imgs_ids.keys()} for o in inputs.keys()}
    for obj in inputs.keys():
        # Get text features
        txt_fts = []
        for c in CAPTIONS_TYPE:
            captions = inputs[obj][f'captions_{c}']
            txt_ft = clip.tokenize(captions)
            with torch.no_grad():
                txt_ft = model.encode_text(txt_ft)
            txt_ft /= txt_ft.norm(dim=-1, keepdim=True)
            txt_fts.append(txt_ft)
        # Get image information
        n_imgs = inputs[obj]['n_images']
        # Get images per priority
        for prio in PRIORITY_IMGS:
            # Get images per dataset
            for dataset in imgs_ids.keys():
                # Get image information from dataset and priority
                dataset_imgs = imgs_ids[dataset][obj]
                p_imgs = dataset_imgs[prio]
                if p_imgs == []:
                    continue
                else:
                    all_imgs = [i for p in dataset_imgs.values() for i in p]
                    random_imgs = get_random_cc_imgs(all_imgs)
                    # Get embeddings of random images
                    random_ft = []
                    for i in random_imgs:
                        random_ft.append(torch.load(i))
                    random_ft = torch.squeeze(torch.stack(random_ft))
                    random_ft /= random_ft.norm(dim=-1, keepdim=True)
                    # Compute match
                    for i in p_imgs:
                        # Load image tensor
                        img_ft = torch.load(IMGS_PATH / f'{dataset}' / f'{i}.pt')
                        img_ft /= img_ft.norm(dim=-1, keepdim=True)
                        # Append image tensor with random images
                        img_ft = torch.vstack([img_ft, random_ft])
                        # Compute match
                        topk_res = []
                        for txt_ft in txt_fts:
                            match = torch.squeeze((img_ft @ txt_ft.T), dim=0)
                            match = torch.mean(match, dim=1)
                            topk_res.append(match.topk(15)[1])
                        # Break if all images have been found
                        if all(0 in m for m in topk_res):
                            imgs[obj][dataset].append(i)
                            if sum(len(v) for v in imgs[obj].values()) >= n_imgs:
                                break
                    else:
                        continue
                    break
            else:
                continue
            break
    return imgs


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
