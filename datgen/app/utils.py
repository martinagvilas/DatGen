import io
import pickle

from PIL import Image
import requests
from requests.auth import HTTPBasicAuth


def retrieve_img(path, username, password):
    response = requests.get('http://128.0.145.146:60666/' + path, auth=HTTPBasicAuth(username, password))
    if response.ok:
        img = Image.open(io.BytesIO(response.content))
        return img
    else:
        return None


def request_worker(action, content, username, password):
    response = requests.post('http://128.0.145.146:60666/', auth=HTTPBasicAuth(username, password),
                             data=pickle.dumps({'action': action, 'content': content}))
    if response.ok:
        if action == 'generate':
            img = Image.open(io.BytesIO(response.content))
            return img
        else:
            return pickle.loads(response.content)
    else:
        return None
