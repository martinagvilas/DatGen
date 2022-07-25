from datgen.input_prepro.property_list import create_property_list
from datgen.input_prepro.caption_generation import generate_captions
from datgen.input_prepro.utils import get_inputs


if __name__ == '__main__':
    # Generate inputs
    inputs = get_inputs()
    inputs = create_property_list(inputs)
    inputs = generate_captions(inputs)