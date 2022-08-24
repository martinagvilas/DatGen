import io
from PIL import Image
import requests


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
