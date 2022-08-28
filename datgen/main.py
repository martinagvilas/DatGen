from datgen.image_match.match import match
from input_prepro.utils import get_inputs


if __name__ == '__main__':
    inputs = get_inputs()
    matched_imgs = match(inputs)
    print('done')