import streamlit as st
from zipfile import ZipFile
import os
from os.path import exists
import math
import random
from PIL import Image
import numpy as np
from skimage import exposure
import time


def show_images(imgs, n_imgs_to_show=9, n_per_col=3):
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


def create_download_button(temp_dir, imgs_dir, specs_dir):
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


def equalize_contrast(path, path_save):
    for img_name in os.listdir(path):
        img_equalized = exposure.equalize_hist(np.asarray(Image.open(path + img_name)))
        Image.fromarray((img_equalized * 255).astype(np.uint8)).save(path_save + img_name, 'PNG')
