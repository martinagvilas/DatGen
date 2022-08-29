import io
import pickle

from PIL import Image
import requests
from requests.auth import HTTPBasicAuth
from datgen.image_match.object import MatchedObject

def request_worker(action, content, username, password):
    response = requests.post('http://128.0.145.146:60666/', auth=HTTPBasicAuth(username, password),
                             data=pickle.dumps({'action': action, 'content': content}))
    if response.ok:
        if action == 'generate':
            img = Image.open(io.BytesIO(response.content))
            return img
        elif action == 'match':
            matched_objects = pickle.loads(response.content)
            for i, matched_object in enumerate(matched_objects):
                vg_paths = [f'visual_genome/{m[0]}.jpg' for m in matched_object.matched_imgs if m[1] == 'vg']
                cc_paths = [f'conceptual_captions/{m[0]}' for m in matched_object.matched_imgs if m[1] == 'cc']
                img_paths = vg_paths + cc_paths
                v = content[i]
                v['matched_img_paths'] = img_paths
                caption = 'A photo of '
                if v['vis_attr'] != ['']:
                    caption += ' and '.join(v['vis_attr'])
                caption += ' ' + v['obj']
                if v['loc'] != ['']:
                    caption += ' in a ' + ' and '.join(v['loc'])
                v['caption_gen'] = caption
            return content
        else:
            img = Image.open(io.BytesIO(response.content))
            return img

    else:
        return None
