import pytest
from datgen.app.utils import request_worker
from PIL import Image


@pytest.mark.parametrize('action, content, username, password', [
    ('retrieve', 'visual_genome/2.jpg', 'datgen', '45678'),
    ('retrieve', 'visual_genome/2.jpg', 'dg', '12345'),
    ('abc', 'visual_genome/2.jpg', 'datgen', '12345')
])
@pytest.mark.xfail(raises=(ConnectionError, ValueError))
def test_xfail_request_worker(action, content, username, password):
    assert request_worker(action, content, username, password) is not None


@pytest.mark.parametrize('action, content, expected', [
    ('retrieve', 'visual_genome/2.jpg', Image.Image),
    ('generate', 'A person on the street.', Image.Image),
    ('match', {0: {'obj': 'person', 'size_min': 0.1, 'vis_attr': ['handsome'], 'loc': [''], 'n_images': 1}}, dict)
])
def test_request_worker(action, content, expected):
    assert isinstance(request_worker(action, content, 'datgen', '12345'), expected)
