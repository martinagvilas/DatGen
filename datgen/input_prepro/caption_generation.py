from itertools import product


PROMPT = [
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
#ARTICLES = ['the', 'my', 'one']


def generate_captions(inputs):
    
    for obj, vals in inputs.items():    
        # Add indefinite article to phrase
        obj_name = add_article([vals['obj']])
        obj_attr = add_article(vals['obj_attr'])
        loc = add_article(vals['loc'])
        
        # Generate captions
        captions = []
        ## Object captions
        captions.append(clean_captions(obj_name))
        ## Attribute captions
        if vals['vis_attr'] != ['']:
            captions.append(clean_captions(
                [f'{t} {o}' for o, t in product(obj_attr, PROMPT)]
            ))
        ## Location captions
        if vals['loc'] != ['']:
            captions.append(clean_captions(
                [f'{t} {l}' for l, t in product(loc, PROMPT)]
            ))
        ## All captions
        if (vals['vis_attr'] != ['']) & (vals['loc'] != ['']):
            captions.append(clean_captions([
                f'{t} {o} in {l}' for o, l, t in product(obj_attr, loc, PROMPT)
            ]))
        
        inputs[obj]['captions'] = captions
    
    return inputs


def add_article(inputs):
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