import clip

from datgen.image_match.annot_search import search_annotations


## how to threshold??


def compute_match(inputs):

    device='cpu'
    model, _ = clip.load('ViT-B/32', device)
    model.to(device)

    imgs_ids = search_annotations(inputs)
    
    for dataset in imgs_ids.keys():
        p1_imgs = imgs_ids[dataset]
        for i in p1_imgs:
            # load image tensor
            # get input 
            # compute match
            pass
    # call search annotations
    return


# def clip_match(imgs_ids, ):

#     return