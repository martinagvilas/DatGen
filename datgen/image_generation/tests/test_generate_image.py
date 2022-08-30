import datgen.image_generation.generate_image as gi
import pytest
from PIL import Image


# @pytest.mark.skipif(gi.model is None, reason='not a worker')
@pytest.mark.skip(reason='turn on skipif and comment this if you test on worker.')
def test_generate_image():
    assert isinstance(gi.generate_image('A pink pikachu on a table.'), Image.Image)


@pytest.mark.parametrize('prompt', [
    '',
    '    '
])
# @pytest.mark.skipif(gi.model is None, reason='not a worker')
@pytest.mark.skip(reason='turn on skipif and comment this if you test on worker.')
@pytest.mark.xfail(raises=ValueError)
def test_xfail_generate_image(prompt):
    assert isinstance(gi.generate_image(prompt), Image.Image)
