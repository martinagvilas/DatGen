import argparse
from pathlib import Path
from this import d
from PIL import Image

import clip
import torch


def compute_clip_image_embeddings(dataset, images_path, res_path, batch_idx):
    
    device='cpu'
    model, prepro = clip.load('ViT-B/32', device)
    model.to(device)
    
    res_path = Path(res_path) / 'clip_image_embeddings' / dataset
    res_path.mkdir(parents=True, exist_ok=True)
    imgs_paths = get_img_paths(Path(images_path), batch_idx)
    
    for img_path in imgs_paths:
        img_ft_file = res_path / f'{img_path.stem}.pt'
        if img_ft_file.is_file():
            continue
        else:
            try:
                img_ft = compute_img_emb(img_path, model, prepro)
                torch.save(img_ft, img_ft_file)
            except:
                continue
    return


def get_img_paths(img_path, batch_idx):
    imgs_paths = list(img_path.glob("*.jpg"))
    if batch_idx != None:
        imgs_paths = get_batch_imgs(imgs_paths, batch_idx)
    return imgs_paths


def get_batch_imgs(imgs_ids, batch_id):
    batch_size = int(len(imgs_ids) / 280)
    batch_id = int(batch_id)
    batch_start = batch_id * batch_size
    batch_end = batch_start + batch_size
    if len(imgs_ids) < batch_end:
        batch_end = len(imgs_ids)
    imgs_ids = imgs_ids[batch_start:batch_end]
    return imgs_ids


def compute_img_emb(img_path, model, prepro):
    img = Image.open(img_path).convert('RGB')
    img_prepro = torch.unsqueeze(prepro(img), dim=0)
    with torch.no_grad():
        img_ft = model.encode_image(img_prepro)
    return img_ft


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store', required=True)
    parser.add_argument('-ip', action='store', required=True)
    parser.add_argument('-rp', action='store', required=True)
    parser.add_argument('-idx', action='store', required=False)
    dataset = parser.parse_args().d
    images_path = Path(parser.parse_args().ip)
    results_path = Path(parser.parse_args().rp)
    batch_idx = parser.parse_args().idx

    compute_clip_image_embeddings(dataset, images_path, results_path, batch_idx)