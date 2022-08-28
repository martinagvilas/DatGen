import streamlit as st
from zipfile import ZipFile
import os
from os.path import basename, exists
import math
import random
from PIL import Image
import numpy as np
from skimage import exposure


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


def create_download_button(imgs_dir, specs_dir):
    if exists('dataset.zip'):
        os.remove('dataset.zip')
    with ZipFile('dataset.zip', 'a') as zipped_data:
        for img_name in os.listdir(imgs_dir):
            zipped_data.write(imgs_dir + img_name, 'images/' + img_name)
        zipped_data.write(specs_dir, 'specs.json')
    file_size = os.path.getsize('dataset.zip') / 1e6
    with open('dataset.zip', 'rb') as f:
        dataset = f.read()
    st.write(f'Dataset Size:{file_size:>8.4f}MB.')
    st.download_button(f'Download Dataset! ', dataset, file_name='dataset.zip', mime='application/zip')

def equalize_contrast(path, path_save):
    for img_name in os.listdir(path):
        img_equalized = exposure.equalize_hist(np.asarray(Image.open(path + img_name)))
        Image.fromarray((img_equalized * 255).astype(np.uint8)).save(path_save + img_name, 'PNG')
