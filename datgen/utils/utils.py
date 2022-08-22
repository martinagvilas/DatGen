import io
from PIL import Image
import requests
import math
import streamlit as st
import random


def retrieve_img(path):
    response = requests.get('http://128.0.145.146:60666/' + path)
    if response.ok:
        img = Image.open(io.BytesIO(response.content))
        return img
    else:
        return None


def get_generated_img(prompt):
    response = requests.post('http://128.0.145.146:60666/', data=prompt)
    if response.ok:
        img = Image.open(io.BytesIO(response.content))
        return img
    else:
        return None


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
