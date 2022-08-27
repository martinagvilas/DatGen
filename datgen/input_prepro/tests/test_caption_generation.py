import pytest

from datgen.input_prepro.caption_generation import (
    generate_captions, add_article, clean_captions
)


def test_generate_captions_single_attributes():
    # Fake data
    n_objs = 4
    input_info = {i: {} for i in range(n_objs)}
    ## Input without attribute or location
    input_info[0]['obj'] = 'armadillo'
    input_info[0]['vis_attr'] = ['']
    input_info[0]['obj_attr'] = ['']
    input_info[0]['loc'] = ['']
    ## Input without location
    input_info[1]['obj'] = 'apple'
    input_info[1]['vis_attr'] = ['red']
    input_info[1]['obj_attr'] = ['red apple']
    input_info[1]['loc'] = ['']
    ## Input without attribute
    input_info[2]['obj'] = 'guitar'
    input_info[2]['vis_attr'] = ['']
    input_info[2]['obj_attr'] = ['']
    input_info[2]['loc'] = ['store']
    # Input with location and attribute
    input_info[3]['obj'] = 'pizza'
    input_info[3]['vis_attr'] = ['round']
    input_info[3]['obj_attr'] = ['round pizza']
    input_info[3]['loc'] = ['plate']

    # Generate
    input_info = generate_captions(input_info)
    
    # Evaluate
    assert len(input_info[0]['captions']) == 1
    assert input_info[0]['captions'][0] == [
        'An armadillo.', 'A photo of an armadillo.'
    ]

    assert len(input_info[1]['captions']) == 2
    assert input_info[1]['captions'][1] == [
        'A red apple.', 'A photo of a red apple.'
    ]

    assert len(input_info[2]['captions']) == 2
    assert input_info[2]['captions'][1] == ['A store.', 'A photo of a store.']

    assert len(input_info[3]['captions']) == 4
    assert input_info[3]['captions'][3] == [
        'A round pizza in a plate.', 'A photo of a round pizza in a plate.'
    ]


def test_generate_double_single_attributes():
    input_info = {0: {}}
    input_info[0]['obj'] = 'pizza'
    input_info[0]['vis_attr'] = ['greasy', 'round']
    input_info[0]['obj_attr'] = ['greasy pizza', 'round pizza']
    input_info[0]['loc'] = ['kitchen', 'plate']

    # Generate
    input_info = generate_captions(input_info)
    
    # Evaluate
    assert input_info[0]['captions'][0] == ['A pizza.', 'A photo of a pizza.']
    assert input_info[0]['captions'][1] == [
        'A greasy pizza.', 'A photo of a greasy pizza.', 'A round pizza.',
        'A photo of a round pizza.'
    ]
    assert input_info[0]['captions'][2] == [
        'A kitchen.', 'A photo of a kitchen.', 'A plate.', 'A photo of a plate.'
    ]
    assert input_info[0]['captions'][3] == [
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
    phrase = add_article([input])
    assert phrase[0] == articled_input


@pytest.mark.parametrize(
    "caption", ["a red rabbit", "a Red rabbit", " a red rabbit"]
)
def test_clean_captions(caption):
    clean_caption = clean_captions([caption])
    assert clean_caption[0] == "A red rabbit."