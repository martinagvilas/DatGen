from itertools import product


TEMPLATES = [
    '',
    'a photo of',
    'itap of',
    'a bad photo of',
    'a good photo of',
    'a low resolution photo of',
    'a cropped photo of',
    'a close-up photo of',
    'a pixelated photo of',
    'a blurry photo of',
]
CONNECTORS = ['the', 'my', 'one']


def generate_captions(inputs):

    for obj, obj_vals in inputs.items():
        # Object + attribute
        ps = _generate_obj_attr_phrase(obj_vals)
        cps = [_generate_captions(p) for p in ps]
        inputs[obj]['captions_obj_attr'] = [c for p in cps for c in p]

        # Location
        ps = _generate_loc_phrase(obj_vals)
        cps = [_generate_captions(p) for p in ps]
        inputs[obj]['captions_loc'] = [c for p in cps for c in p]
        
        # Object
        inputs[obj]['captions_obj'] = _generate_captions(obj_vals['obj'])

    return inputs


def _generate_obj_attr_phrase(obj_vals):
    obj_attr = obj_vals['vis_attr']
    if obj_attr == ['']:
        return []
    else:
        phrases = [f"{obj_vals['obj']} that is {a}" for a in obj_attr]
        phrases = phrases + obj_vals['obj_attr']
        return phrases


def _generate_loc_phrase(obj_vals):
    locs = obj_vals['loc']
    if locs == ['']:
        return []
    else:
        # c = {l:('an'if l.startswith(('a','e','i','o','u')) else 'a') for l in locs}
        # ps_obj = [f"{obj_vals['obj']} in {c[l]} {l}" for l in locs]
        # ps_obj_attr = [
        #     f"{o} in {c[l]} {l}" for o, l in product(obj_vals['obj_attr'], locs)
        # ]
        # phrases = ps_obj + ps_obj_attr + obj_vals['loc']
        phrases = obj_vals['loc']
        return phrases


def _generate_captions(phrase):
    if phrase.startswith(('a', 'e', 'i', 'o', 'u')):
        connectors = CONNECTORS + ['an'] 
    else:
        connectors = CONNECTORS + ['a']
    captions = [
        f'{template} {connector} {phrase}' 
        for template, connector in product(TEMPLATES, connectors)
    ]
    captions = [clean_caption(c) for c in captions]
    return captions


def clean_caption(caption):
    caption = caption[1:] if caption.startswith(' ') else caption
    caption = caption.capitalize() + '.'
    return caption