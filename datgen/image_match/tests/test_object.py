import pytest

from datgen.image_match.object import MatchedObject


@pytest.mark.parametrize(
    "vis_attr, loc, obj_attr, p1, p2, p3", [
        ("", "", "", [1, 2, 4, 5, 7], [], []),
        ("red", "", "red apple", [4, 5], [1, 2, 7], []),
        ("", "store", "", [5, 7], [1, 2, 4], [6]),
        ("red", "store", "red apple", [5], [4], [1, 2, 6, 7])
    ]
)
def test_divide_priorities(vis_attr, loc, obj_attr, p1, p2, p3):
    # Fake data
    vals = {}
    vals['obj'] = 'apple'
    vals['vis_attr'] = [vis_attr]
    vals['loc'] = [loc]
    vals['obj_attr'] = [obj_attr]
    vals['n_images'] = 100
    vals['size_min'] = 0.1

    obj = MatchedObject(vals)
    
    ## Imgs IDs
    imgs_obj = [1, 2, 4, 5, 7]
    imgs_attr = [4, 5]
    imgs_loc = [5, 6, 7]
    
    imgs = obj.divide_priorities(imgs_obj, imgs_attr, imgs_loc)

    assert imgs['p1'] == p1
    assert imgs['p2'] == p2
    assert imgs['p3'] == p3


def test_search_vg():
    # Fake data
    vg_obj = {'apple': [1, 2, 5, 6], 'store': [2, 3]}
    vg_attr = [
        {'image_id': 1, 'attributes': [{'names': ['apple'], 'attributes': ['red']}]},
        {'image_id': 2, 'attributes': [{'names': ['apple'], 'attributes': ['red']}]},
        {'image_id': 5, 'attributes': [{'names': ['apple'], 'attributes': ['blue']}]},
        {'image_id': 7, 'attributes': [{'names': ['truck'], 'attributes': ['red']}]},
    ]

    vals = {}
    vals['obj'] = 'apple'
    vals['vis_attr'] = ['red']
    vals['loc'] = ['store']
    vals['obj_attr'] = ['red apple']
    vals['n_images'] = 100
    vals['size_min'] = 0.1

    obj = MatchedObject(vals)
    obj.search_vg(vg_obj, vg_attr)

    # Evaluate
    assert obj.annot_ids['vg']['p1'] == [2]
    assert obj.annot_ids['vg']['p2'] == [1]
    assert obj.annot_ids['vg']['p3'] == [3, 5, 6]
