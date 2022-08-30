import io
import pickle

from PIL import Image
import requests
from requests.auth import HTTPBasicAuth


def request_worker(action: str, content, username: str, password: str):
    """
        Request the worker
    Parameters
    ----------
    action: str
        The action for the worker to take. It should be either "generate", "retrieve" or "match"
    content:
        The request content. For "generate", this is the prompt; for "retrieve", this is the path of image;
        for "match", this is the specification dictionary.
    username: str
        The username for the HTTP authentication
    password: str
        The password for the HTTP authentication
    Returns
    -------
        The result of the request. For "generate", this is the generated image; for "retrieve",
        this is the retrieved image; for "match", this is the MatchedObject.

    """
    response = requests.post('http://128.0.145.146:60666/', auth=HTTPBasicAuth(username, password),
                             data=pickle.dumps({'action': action, 'content': content}))

    def set_caption_for_generation(v):
        caption = 'A photo of '
        if v['vis_attr'] != ['']:
            caption += ' and '.join(v['vis_attr'])
        caption += ' ' + v['obj']
        if v['loc'] != ['']:
            caption += ' in a ' + ' and '.join(v['loc'])
        v['caption_gen'] = caption

    if response.ok:
        if action == 'generate':
            img = Image.open(io.BytesIO(response.content))
            return img
        elif action == 'match':
            matched_objects = pickle.loads(response.content)
            if len(matched_objects) == 0:
                for k, v in content.items():
                    v['matched_img_paths'] = []
                    set_caption_for_generation(v)
            else:
                for i, matched_object in enumerate(matched_objects):
                    vg_paths = [f'visual_genome/{m[0]}.jpg' for m in matched_object.matched_imgs if m[1] == 'vg']
                    cc_paths = [f'conceptual_captions/{m[0]}' for m in matched_object.matched_imgs if m[1] == 'cc']
                    img_paths = vg_paths + cc_paths
                    v = content[i]
                    v['matched_img_paths'] = img_paths
                    set_caption_for_generation(v)
            return content
        elif action == 'retrieve':
            img = Image.open(io.BytesIO(response.content))
            return img
        else:
            raise ValueError('Action not recognized.')
    else:
        raise ConnectionError('Request failed.')
