import io
from PIL import Image
import requests
from requests.auth import HTTPBasicAuth


def retrieve_img(path, username, password):
    response = requests.get('http://0.0.0.0:60666/' + path, auth=HTTPBasicAuth(username, password))
    if response.ok:
        img = Image.open(io.BytesIO(response.content))
        return img
    else:
        return None


def get_generated_img(prompt, username, password):
    response = requests.post('http://0.0.0.0:60666/', data=prompt, auth=HTTPBasicAuth(username, password))
    if response.ok:
        img = Image.open(io.BytesIO(response.content))
        return img
    else:
        return None
