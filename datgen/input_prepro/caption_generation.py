from itertools import product


PROMPTS = [
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
    """Generate captions from input specifications.

    Parameters
    ----------
    inputs : Dict
        Containing input specifications obtained from website form.

    Returns
    -------
    Dict.
        Each entry contains a "captions" attribute with a list of groups of 
        captions for the mathing module.
    """
    
    for obj, vals in inputs.items():    
        # Add indefinite article to phrase
        obj_name = add_article([vals['obj']])
        obj_attr = add_article(vals['obj_attr'])
        loc = add_article(vals['loc'])
        
        # Generate captions
        captions = []
        ## Object captions
        captions.append(clean_captions(
            [f'{t} {o}' for o, t in product(obj_name, PROMPTS)]
        ))
        ## Attribute captions
        if vals['vis_attr'] != ['']:
            captions.append(clean_captions(
                [f'{t} {o}' for o, t in product(obj_attr, PROMPTS)]
            ))
        ## Location captions
        if vals['loc'] != ['']:
            captions.append(clean_captions(
                [f'{t} {l}' for l, t in product(loc, PROMPTS)]
            ))
        ## All captions
        if (vals['vis_attr'] != ['']) & (vals['loc'] != ['']):
            captions.append(clean_captions([
                f'{t} {o} in {l}' for o, l, t in product(obj_attr, loc, PROMPTS)
            ]))
        
        inputs[obj]['captions'] = captions
    
    return inputs


def add_article(inputs):
    """Add indefinite article to phrase.

    Parameters
    ----------
    inputs : list
        Input specified by user. Must be a noun or an adjetive + noun.

    Returns
    -------
    list
        Inputs with indefinite article.
    """
    vocals = ('a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U')
    phrases = [
        f'an {p}' if p.startswith(vocals) else f'a {p}'
        for p in inputs
    ]
    return phrases


def clean_captions(captions):
    """Capitalize, add punctuation and remove unnecesary spaces in caption.

    Parameters
    ----------
    captions : list
        Captions to clean.

    Returns
    -------
    list
        Cleaned captions.
    """
    clean_captions = []
    for caption in captions:
        caption = caption[1:] if caption.startswith(' ') else caption
        caption = caption.capitalize() + '.'
        clean_captions.append(caption)
    return clean_captions