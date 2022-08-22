import streamlit as st
from zipfile import ZipFile
import os
from os.path import basename, exists
import math
import random


def show_images(imgs, n_imgs_to_show=9, n_per_col=3):
    if len(imgs) >= n_imgs_to_show:
        imgs_chosen = random.sample(imgs, n_imgs_to_show)
    else:
        imgs_chosen = imgs
    imgs_resized = [img.resize((128, 128)) for img in imgs_chosen]
    n_col = math.ceil(len(imgs_resized) / n_per_col)
    cols = st.columns(n_col)
    count = 0
    for col in cols:
        with col:
            for _ in range(n_per_col):
                if count < len(imgs_resized):
                    st.image(imgs_resized[count])
                    count += 1


def create_download_button():
    if exists('dataset.zip'):
        os.remove('dataset.zip')
    with ZipFile('dataset.zip', 'w') as zipped_data:
        for folderName, subfolders, filenames in os.walk('datgen/temp'):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipped_data.write(filePath, basename(filePath))
    zipped_data.close()
    file_size = os.path.getsize('dataset.zip') / 1e6
    with open('dataset.zip', 'rb') as f:
        dataset = f.read()
    st.download_button(f'Download Dataset! Dataset Size:{file_size:>8.4f}', dataset,
                       file_name='dataset.zip', mime='application/zip')
