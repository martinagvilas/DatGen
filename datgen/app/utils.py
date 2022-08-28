import io
import pickle

from PIL import Image
import requests
from requests.auth import HTTPBasicAuth


def request_worker(action, content, username, password):
    response = requests.post('http://128.0.145.146:60666/', auth=HTTPBasicAuth(username, password),
                             data=pickle.dumps({'action': action, 'content': content}))
    if response.ok:
        if action == 'generate':
            img = Image.open(io.BytesIO(response.content))
            return img
        elif action == 'match':
            matched, specs = pickle.loads(response.content)
            for k, v in specs.items():
                vg_paths = [f'visual_genome/{vg_path}.jpg' for vg_path in matched[k]['vg']]
                cc_paths = ['conceptual_captions/' + cc_path for cc_path in matched[k]['cc']]
                img_paths = vg_paths + cc_paths
                v['matched_img_paths'] = img_paths
                caption = 'A photo of '
                if v['vis_attr'] != ['']:
                    caption += ' and '.join(v['vis_attr'])
                caption += ' ' + v['obj']
                if v['loc'] != ['']:
                    caption += ' in a ' + ' and '.join(v['loc'])
                v['caption_gen'] = caption
            return specs
        else:
            img = Image.open(io.BytesIO(response.content))
            return img

    else:
        return None
