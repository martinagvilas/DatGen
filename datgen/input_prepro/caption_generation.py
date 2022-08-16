from itertools import product


TEMPLATES = [
    '',
    'a photo of',
    #'itap of',
    #'a bad photo of',
    #'a good photo of',
    #'a low resolution photo of',
    #'a cropped photo of',
    #'a close-up photo of',
    #'a pixelated photo of',
    #'a blurry photo of',
]
#CONNECTORS = ['the', 'my', 'one']


def generate_captions(inputs):
    for obj, obj_vals in inputs.items():
        obj_attr = _add_connector(obj_vals['obj_attr'])
        loc = _add_connector(obj_vals['loc'])
        inputs[obj]['captions_all'] = clean_captions([
            f'{t} {o} in {l}' for o, l, t in product(obj_attr, loc, TEMPLATES)
        ])
        inputs[obj]['captions_obj'] = clean_captions([
            f'{t} {o}' for o, t in product(obj_attr, TEMPLATES)
        ])
        inputs[obj]['captions_loc'] = clean_captions(
            [f'{t} {l}' for l, t in product(loc, TEMPLATES)]
        )
    return inputs


def _add_connector(inputs):
    phrases = [
        f'an {p}' if p.startswith(('a', 'e', 'i', 'o', 'u')) else f'a {p}'
        for p in inputs
    ]
    return phrases


def clean_captions(captions):
    clean_captions = []
    for caption in captions:
        caption = caption[1:] if caption.startswith(' ') else caption
        caption = caption.capitalize() + '.'
        clean_captions.append(caption)
    return clean_captions