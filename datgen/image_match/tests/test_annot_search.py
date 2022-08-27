import pytest

from datgen.image_match.annot_search import (
    divide_priorities
)


# def test_search_vg():


@pytest.mark.parametrize(
    "vis_attr, loc, p1, p2, p3", [
        ("", "", [1, 2, 4, 5, 7], [], []),
        ("red", "", [4, 5], [1, 2, 7], []),
        ("", "store", [5, 7], [1, 2, 4], [6]),
        ("red", "store", [5], [4], [1, 2, 6, 7])
    ]
)
def test_divide_priorities(vis_attr, loc, p1, p2, p3):
    # Fake data
    vals = {}
    vals['vis_attr'] = [vis_attr]
    vals['loc'] = [loc]
    ## Imgs IDs
    imgs_obj = [1, 2, 4, 5, 7]
    imgs_attr = [4, 5]
    imgs_loc = [5, 6, 7]
    
    imgs = divide_priorities(vals, imgs_obj, imgs_attr, imgs_loc)

    assert imgs['p1'] == p1
    assert imgs['p2'] == p2
    assert imgs['p3'] == p3
    


# def test_get_cc_object_info():
#     labels = pd.read_csv(ANNOT_PATH/'classification_data.csv')[['file','tags']]
