import streamlit as st
from zipfile import ZipFile
import os
from os.path import exists
import math
import random
from PIL import Image
import numpy as np
from skimage import exposure


def show_images(imgs: list[Image.Image], n_imgs_to_show: int = 9, n_per_col: int = 3):
    if len(imgs) == 0:
        return
    if n_imgs_to_show <= 0 or n_per_col <= 0:
        n_imgs_to_show = 9
        n_per_col = 3
    if len(imgs) >= n_imgs_to_show:
        imgs_chosen = random.sample(imgs, n_imgs_to_show)
    else:
        imgs_chosen = imgs
    imgs_resized = [img.resize((256, 256)) for img in imgs_chosen]
    n_col = math.ceil(len(imgs_resized) / n_per_col)
    cols = st.columns(n_col)
    count = 0
    for col in cols:
        with col:
            for _ in range(n_per_col):
                if count < len(imgs_resized):
                    st.image(imgs_resized[count])
                    count += 1
    return


def create_download_button(temp_dir: str, imgs_dir: str, specs_dir: str):
    if not os.path.isdir(temp_dir) or not os.path.isdir(imgs_dir):
        raise FileNotFoundError('Invalid temp directory')

    zip_dir = temp_dir + 'dataset.zip'
    if exists(zip_dir):
        os.remove(zip_dir)
    with ZipFile(zip_dir, 'w') as zipped_data:
        for img_name in os.listdir(imgs_dir):
            zipped_data.write(imgs_dir + img_name, 'images/' + img_name)
        zipped_data.write(specs_dir, 'specs.json')
    file_size = os.path.getsize(zip_dir) / 1e6
    with open(zip_dir, 'rb') as f:
        dataset = f.read()
    st.write(f'Dataset Size:{file_size:>8.4f}MB.')
    st.download_button(f'Download Dataset! ', dataset, file_name=zip_dir, mime='application/zip')
    return None


def equalize_contrast(img: Image.Image):
    img_equalized = exposure.equalize_hist(np.asarray(img))
    img_equalized = Image.fromarray((img_equalized * 255).astype(np.uint8))
    return img_equalized
