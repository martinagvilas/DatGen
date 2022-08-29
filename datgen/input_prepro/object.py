from itertools import product


PROMPTS = ['', 'a photo of']


class DGObject():
    """Preprocessed object specifications.
    """
    def __init__(self, vals):
        # Define object attributes
        self.obj_name = vals['obj'].lower()
        self.vis_attr = [a.lower() for a in vals['vis_attr']]
        self.loc = [l.lower() for l in vals['loc']]
        self.n_images = vals['n_images']
        self.size_min = vals['size_min']
        
        # Generate object-attribute combination
        if vals['vis_attr'] != ['']:
            self.obj_attr = [f'{a} {vals["obj"]}' for a in vals['vis_attr']]
        else:
           self.obj_attr = ['']
        
        # Generate captions
        self.captions = self.generate_captions()


    def generate_captions(self):
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
        # Add indefinite article to phrase
        obj_name = _add_article([self.obj_name])
        obj_attr = _add_article(self.obj_attr)
        loc = _add_article(self.loc)
        
        # Generate captions
        captions = []
        ## Object captions
        captions.append(_clean_captions(
            [f'{t} {o}' for o, t in product(obj_name, PROMPTS)]
        ))
        ## Attribute captions
        if self.vis_attr != ['']:
            captions.append(_clean_captions(
                [f'{t} {o}' for o, t in product(obj_attr, PROMPTS)]
            ))
        ## Location captions
        if self.loc != ['']:
            captions.append(_clean_captions(
                [f'{t} {l}' for l, t in product(loc, PROMPTS)]
            ))
        ## All captions
        if (self.vis_attr != ['']) & (self.loc != ['']):
            captions.append(_clean_captions([
                f'{t} {o} in {l}' for o, l, t in product(obj_attr, loc, PROMPTS)
            ]))

        return captions


def _add_article(inputs):
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


def _clean_captions(captions):
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
