import pytest

from datgen.input_prepro.object import (
    DGObject, _add_article, _clean_captions
)


@pytest.mark.parametrize(
    "obj,vis_attr, obj_attr, loc, caption_id, caption", [
        ("armadillo", [''], [''], [''], 0, [
            'An armadillo.', 'A photo of an armadillo.'
        ]), 
        ("apple", ['red'], ['red apple'], [''], 1, [
            'A red apple.', 'A photo of a red apple.'
        ]),
        ("guitar", [''], [''], ["store"], 1, [
            'A store.', 'A photo of a store.'
        ]),
        ("pizza", ["round"], ["round pizza"], ["plate"], 3, [
            'A round pizza in a plate.', 'A photo of a round pizza in a plate.'
        ])
    ]
)
def test_object_single_spec(obj, vis_attr, obj_attr, loc, caption_id, caption):
    # Fake data
    vals = {}
    vals['obj'] = obj
    vals['vis_attr'] = vis_attr
    vals['obj_attr'] = obj_attr
    vals['loc'] = loc
    vals['n_images'] = 100
    vals['size_min'] = 0.1

    # Generate captions
    obj = DGObject(vals)
    obj.generate_captions()
    
    # Evaluate
    assert obj.captions[caption_id] == caption


def test_object_double_spec():
    # Fake data
    vals = {}
    vals['obj'] = 'pizza'
    vals['vis_attr'] = ['greasy', 'round']
    vals['obj_attr'] = ['greasy pizza', 'round pizza']
    vals['loc'] = ['kitchen', 'plate']
    vals['n_images'] = 100
    vals['size_min'] = 0.1

    # Generate captions
    obj = DGObject(vals)
    obj.generate_captions()
    
    # Evaluate
    assert obj.captions[0] == ['A pizza.', 'A photo of a pizza.']
    assert obj.captions[1] == [
        'A greasy pizza.', 'A photo of a greasy pizza.', 'A round pizza.',
        'A photo of a round pizza.'
    ]
    assert obj.captions[2] == [
        'A kitchen.', 'A photo of a kitchen.', 'A plate.', 'A photo of a plate.'
    ]
    assert obj.captions[3] == [
        'A greasy pizza in a kitchen.', 
        'A photo of a greasy pizza in a kitchen.', 
        'A greasy pizza in a plate.', 'A photo of a greasy pizza in a plate.',
        'A round pizza in a kitchen.', 
        'A photo of a round pizza in a kitchen.', 
        'A round pizza in a plate.', 'A photo of a round pizza in a plate.',
    ]
    

@pytest.mark.parametrize(
    "input, articled_input", 
    [("apple", "an apple"), ("Apple", "an Apple"), 
    ("plane", "a plane"), ("Plane", "a Plane")]
)
def test_add_article(input, articled_input):
    phrase = _add_article([input])
    assert phrase[0] == articled_input


@pytest.mark.parametrize(
    "caption", ["a red rabbit", "a Red rabbit", " a red rabbit"]
)
def test_clean_captions(caption):
    clean_caption = _clean_captions([caption])
    assert clean_caption[0] == "A red rabbit."