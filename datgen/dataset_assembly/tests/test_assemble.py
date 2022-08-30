import pytest
from datgen.dataset_assembly.assemble import show_images, create_download_button, equalize_contrast
from skimage import data
from PIL import Image

images = [Image.fromarray(data.astronaut()), Image.fromarray(data.moon())]


@pytest.mark.parametrize('imgs, n_imgs_to_show, n_per_col', [
    (images, 9, 3),
    (images[:1], 5, 2),
    ([], 5, 2),
    (images, -3, 2),
    (images, 3, -2),
    (images, -3, -2),
])
def test_show_images(imgs, n_imgs_to_show, n_per_col):
    assert show_images(imgs, n_imgs_to_show, n_per_col) is None


@pytest.mark.xfail(raises=FileNotFoundError)
@pytest.mark.parametrize('temp_dir, imgs_dir, specs_dir', [
    ('images', 'temp', 'temp/specs.json'),
    ('image_match', 'images', 'temp/specs.json'),
    ('images', 'images', 'temp/specs.json'),
])
def test_create_download_button(temp_dir, imgs_dir, specs_dir):
    assert create_download_button(temp_dir, imgs_dir, specs_dir) is None


@pytest.mark.parametrize('img', [
    images[0],
    images[1]
])
def test_equalize_contrast(img):
    assert isinstance(img, Image.Image)
