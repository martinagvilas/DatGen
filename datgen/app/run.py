import argparse
import os
import shutil
import sys

import streamlit as st
from PIL import Image
import streamlit.elements.utils

sys.path.append(os.getcwd())
streamlit.elements.utils._shown_default_value_warning = True

from datgen.utils.utils import retrieve_img, get_generated_img
from datgen.dataset_assembly.assemble import show_images, create_download_button

# initial specification formula
init_spec = {
    'name': '',
    'size': 50,
    'visual attributes': [''],
    'location': ['']
}

global_state = ['spec_config', 'img_match', 'img_gen', 'data_assem']


def change_global_state(to=0):
    st.session_state['global_state'] = global_state[to]


# convert chosen spec name to index
def get_chosen_spec_index():
    return int(st.session_state['chosen_spec'][7:])


# callback for button "Add"
def add_spec():
    st.session_state['specs'].append(init_spec)
    st.session_state['chosen_spec'] = 'Object ' + str(len(st.session_state['specs']) - 1)
    change_global_state(0)


# callback for button "Remove"
def remove_spec():
    if len(st.session_state['specs']) > 1:
        st.session_state['specs'].pop(get_chosen_spec_index())
        st.session_state['chosen_spec'] = 'Object 0'
    else:
        st.session_state['specs'] = [init_spec]
    change_global_state(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_n_spec', default=20, choices=range(50), type=int)
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    args = parser.parse_args()

    # define font size for later use
    st.markdown("""
                <style>
                .big-font {
                    font-size:80px;
                }
                .medium-font{
                    font-size:50px;
                }
                </style>
                """, unsafe_allow_html=True)

    # Global state
    if 'global_state' not in st.session_state:
        st.session_state['global_state'] = global_state[0]

    # Session states initialization
    if 'specs' not in st.session_state:
        st.session_state['specs'] = [init_spec]
        st.session_state['chosen_spec'] = 'Object 0'

    if 'matching_img_paths' not in st.session_state:
        st.session_state['matching_img_paths'] = []

    if 'captions_left' not in st.session_state:
        st.session_state['captions_left'] = []

    # sidebar initialization
    with st.sidebar:
        st.markdown('<p class="big-font">DatGen</p>', unsafe_allow_html=True)
        st.markdown('_Build your own Image Datasets._')
        st.title('Specifications')
        col1, col2, _, _, _ = st.columns(5, gap='small')
        col1.button('Add', on_click=add_spec)
        col2.button('Remove', on_click=remove_spec)
        st.radio(label='📌 your objects here', key='chosen_spec',
                 index=get_chosen_spec_index(),
                 options=[f'Object {i}' for i in range(len(st.session_state['specs']))],
                 on_change=lambda: change_global_state(0))
        st.button('DatGen!', on_click=lambda: change_global_state(1))

    if st.session_state['global_state'] == global_state[0]:
        i = get_chosen_spec_index()
        current_spec = st.session_state['specs'][i]
        st.subheader(f'Object {i}')

        # Define object
        name = st.text_input('Name of object', key=f'{i}_obj_name',
                             value=current_spec['name'])

        # Define size
        size = st.number_input('Minimum occupancy of object (%)', min_value=0,
                               max_value=100, step=5, key=f'{i}_min_size',
                               value=current_spec['size'], help='(...). Example:')
        # Define visual attributes
        vis_att = st.text_input('Visual attributes of the object (separated by ";")', key=f'{i}_vis_att',
                                value=';'.join(current_spec['visual attributes']), help='(...). Example:')

        # Define location
        loc = st.text_input('Location/s of the object (separated by ";")', key=f'{i}_loc',
                            value=';'.join(current_spec['location']), help='(...). Example:')

        saved = st.button(label="Save")
        if saved:
            spec = {'name': name,
                    'size': size,
                    'visual attributes': vis_att.split(';'),
                    'location': loc.split(';')}
            st.session_state['specs'][i] = spec

    elif st.session_state['global_state'] == global_state[1]:
        st.write('Matching images...')

        # captions = generate_captions(create_property_list(st.session_state['specs']))
        # matching_img_paths, captions_left = compute_match(captions)
        matching_img_paths = ['conceptual_captions/2']
        captions_left = ['The sidewalk near the corner of streets has one of the few vending machines.']

        st.session_state['matching_img_paths'] = matching_img_paths
        st.session_state['captions_left'] = captions_left

        if os.path.exists('temp'):
            shutil.rmtree('temp')
        os.mkdir('temp')

        if len(matching_img_paths) > 0:
            st.write('Retrieving images...')
            for i, img_path in enumerate(matching_img_paths):
                img = retrieve_img(img_path, args.username, args.password)
                if img is None:
                    st.write(f'Failed to retrieve image {i}!')
                else:
                    img.save(f'temp/{i}.png')

        if len(captions_left) > 0:
            st.warning(f'Failed to find match for {len(captions_left)} images.')
            st.warning(f'Do you want to generate these images using the Deep generative module? '
                       f'Estimated time: {len(captions_left) * 4} seconds.')

            col1, col2 = st.columns(2)
            with col1:
                st.button('Generate!', on_click=lambda: change_global_state(2))
            with col2:
                st.button('Cancel and download.', on_click=lambda: change_global_state(3))
        else:
            st.session_state['global_state'] = global_state[3]
            st.experimental_rerun()

    elif st.session_state['global_state'] == global_state[2]:
        captions_left = st.session_state['captions_left']
        matching_img_paths = st.session_state['matching_img_paths']
        st.write(f'Generating images... Estimated time: {len(captions_left) * 4} seconds.')
        for i, caption in enumerate(captions_left):
            img = get_generated_img(caption, args.username, args.password)
            img.save(f'temp/{len(matching_img_paths) + i}.png')
        st.session_state['global_state'] = global_state[3]
        st.experimental_rerun()

    elif st.session_state['global_state'] == global_state[3]:
        st.write('Examples of the dataset:')
        example_imgs = [Image.open('temp/' + path) for path in os.listdir('temp')]
        show_images(example_imgs)
        create_download_button()
