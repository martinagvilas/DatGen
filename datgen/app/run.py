import argparse
import os
import shutil
import sys
import json
import time

import streamlit as st
from PIL import Image
import streamlit.elements.utils

sys.path.append(os.getcwd())
streamlit.elements.utils._shown_default_value_warning = True

from datgen.app.utils import request_worker
from datgen.dataset_assembly.assemble import show_images, create_download_button, equalize_contrast

# initial specification formula
init_spec = {
    'obj': '',
    'size_min': 0.1,
    'vis_attr': [''],
    'loc': [''],
    'n_images': 1
}

global_state = ['spec_config', 'img_match', 'img_gen', 'data_assem']


def change_session_state(state, to):
    st.session_state[state] = to


# convert chosen spec name to index
def get_chosen_spec_index():
    return int(st.session_state['chosen_spec'][7:]) - 1


# callback for button "Add"
def add_spec():
    st.session_state['specs'].append(init_spec)
    st.session_state['chosen_spec'] = 'Object ' + str(len(st.session_state['specs']) - 1)
    change_session_state('global_state', global_state[0])


# callback for button "Remove"
def remove_spec():
    if len(st.session_state['specs']) > 1:
        st.session_state['specs'].pop(get_chosen_spec_index())
        st.session_state['chosen_spec'] = 'Object 1'
    else:
        st.session_state['specs'] = [init_spec]
    change_session_state('global_state', global_state[0])


def set_spec(i, key, value):
    st.session_state['specs'][i][key] = value


def save_spec(i, obj, size_min, vis_attr, loc, n_images):
    spec = {'obj': obj,
            'size_min': size_min / 100,
            'vis_attr': vis_attr.split(';'),
            'loc': loc.split(';'),
            'n_images': int(n_images)}
    st.session_state['specs'][i] = spec


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_n_spec', default=20, choices=range(50), type=int)
    parser.add_argument('--max_n_objects_per_spec', default=20, choices=range(50), type=int)
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
        st.session_state['chosen_spec'] = 'Object 1'

    if 'matching_results' not in st.session_state:
        st.session_state['matching_results'] = {}

    if 'equalize_img' not in st.session_state:
        st.session_state['equalize_img'] = False

    if 'temp_dir' not in st.session_state:
        st.session_state['temp_dir'] = 'temp/temp_' + '_'.join(str(time.time()).split('.')) + '/'

    if 'ignore_blank' not in st.session_state:
        st.session_state['ignore_blank'] = False

    # sidebar initialization
    with st.sidebar:
        st.markdown('<p class="big-font">DatGen</p>', unsafe_allow_html=True)
        st.markdown('_Build your own Image Datasets._')
        st.title('Specifications')
        st.radio(label='📌 Choose your objects and properties', key='chosen_spec',
                 index=get_chosen_spec_index(),
                 options=[f'Object {i + 1}' for i in range(len(st.session_state['specs']))],
                 on_change=lambda: change_session_state('global_state', global_state[0]))
        col1, col2, _, _, _ = st.columns(5, gap='small')
        col1.button('Add', on_click=add_spec)
        col2.button('Remove', on_click=remove_spec)
        st.checkbox('Equalize contrast', key='equalize_img', help="Equalize contrast values between images in the final dataset or not.")
        st.button('DatGen!', on_click=lambda: change_session_state('global_state', global_state[1]))

    if st.session_state['global_state'] == global_state[0]:
        i = get_chosen_spec_index()
        current_spec = st.session_state['specs'][i]
        st.subheader(f'Object {i + 1}')

        # Define object
        help_obj = f"Name of object you want represented in the dataset. "\
            "Example: 'apple'. "\
            "Must be provided and should consist of a unique option. "\
            "If you want to add other objects, please press the button ADD "\
            "in the sidebar."
        obj = st.text_input('Name of object', key=f'{i}_obj',
                            value=current_spec['obj'], help=help_obj)

        # Define size
        help_occ = "Minimum occupancy of the object in the image. Expressed in percentage."
        size_min = st.number_input('Minimum occupancy of object (%)', key=f'{i}_size_min',
                                   min_value=10, max_value=100, step=5,
                                   value=int(current_spec['size_min'] * 100), help=help_occ,
                                   on_change=lambda: set_spec(i, 'size_min', st.session_state[f'{i}_size_min'] / 100))

        # Define visual attributes
        help_vis_attr = "Visual attributes of the object. Example: 'red'. "\
            "Can be multiple attributes separated by a ';' without space in-between. "\
            "Example:'red;shiny'. "\
            "If you provide more than one attribute, images will display "\
            "the object with either attribute, but not necessarily both."
        vis_attr = st.text_input('Visual attributes of the object (separated by ";")', key=f'{i}_vis_attr',
                                 value=';'.join(current_spec['vis_attr']), help=help_vis_attr)

        # Define location
        help_loc = "Object location. Example: 'kitchen'. "\
            "Can be multiple locations separated by a ';' without space in-between. "\
            "Example: 'kitchen;table'. "\
            "If you provide more than one location, images will display "\
            "the object in either location, but not necessarily both."
        loc = st.text_input('Location/s of the object (separated by ";")', key=f'{i}_loc',
                            value=';'.join(current_spec['loc']), help=help_loc)

        # Define number of images
        help_n_imgs = "Number of images to generate containing the input specifications."
        n_images = st.number_input('Number of objects', key=f'{i}_n_images',
                                   min_value=1, max_value=20, value=current_spec['n_images'], help=help_n_imgs,
                                   on_change=lambda: set_spec(i, 'n_images', st.session_state[f'{i}_n_images']))

        st.markdown('_If you want to read more about using DatGen, head to our [github repository](https://github.com/martinagvilas/DatGen)._')


        save_spec(i, obj, size_min, vis_attr, loc, n_images)
        change_session_state('ignore_blank', False)

    elif st.session_state['global_state'] == global_state[1]:
        specs = {i: spec for i, spec in enumerate(st.session_state['specs']) if spec['obj'].strip() != ''}
        specs_unspecified = [i + 1 for i, spec in enumerate(st.session_state['specs']) if spec['obj'].strip() == '']
        if len(specs_unspecified) > 0 and not st.session_state['ignore_blank']:
            st.warning(f'Objects {specs_unspecified} not specified!')
            st.warning(f'Do you want to ignore these objects and continue?')
            ignore = st.button('Ignore', on_click=lambda: change_session_state('ignore_blank', True))
        elif len(specs) == 0:
            st.warning('Please specify at least one object!')
            time.sleep(3)
            change_session_state('global_state', global_state[0])
            st.experimental_rerun()
        else:
            st.warning('Matching images...')
            matching_results = request_worker('match', specs, args.username, args.password)
            st.session_state['matching_results'] = matching_results
            st.success('Matching images done.')

            temp_dir = st.session_state['temp_dir']
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.mkdir(temp_dir)
            os.mkdir(temp_dir + 'images')
            os.mkdir(temp_dir + 'images_equalized')
            with open(temp_dir + 'specs.json', 'w') as f:
                json.dump(specs, f)

            st.warning('Retrieving images...')
            captions_remaining = []
            for obj_idx, obj_spec in matching_results.items():
                matched_img_paths = obj_spec['matched_img_paths']
                if len(matched_img_paths) > 0:
                    for i, img_path in enumerate(matched_img_paths):
                        img = request_worker('retrieve', img_path, args.username, args.password)
                        if img is None:
                            st.write(f'Failed to retrieve image {i}!')
                        else:
                            img.save(temp_dir + f'images/{obj_idx}_{i}.png')
                caption_remaining = (obj_idx, obj_spec['n_images'] - len(matched_img_paths), obj_spec['caption_gen'])
                captions_remaining.append(caption_remaining)
            st.session_state['captions_remaining'] = captions_remaining
            st.success('Retrieving images done.')

            total_n_images_remaining = sum([o[1] for o in captions_remaining])
            if total_n_images_remaining > 0:
                st.warning(f'Failed to find match for # {[o[0] for o in captions_remaining]} objects, '
                           f'total {total_n_images_remaining} images.')
                st.warning(f'Do you want to generate these images using the Deep generative module? '
                           f'Estimated time: {total_n_images_remaining * 4} seconds.')

                col1, col2 = st.columns(2)
                with col1:
                    st.button('Generate!', on_click=lambda: change_session_state('global_state', global_state[2]))
                with col2:
                    st.button('Cancel and download dataset',
                              on_click=lambda: change_session_state('global_state', global_state[3]))
            else:
                st.success('Matching all objects completed!')
                st.session_state['global_state'] = global_state[3]
                st.experimental_rerun()

    elif st.session_state['global_state'] == global_state[2]:
        matching_results = st.session_state['matching_results']
        captions_remaining = st.session_state['captions_remaining']
        total_n_images_remaining = sum([o[1] for o in captions_remaining])
        st.warning(f'Generating images... Estimated time: {total_n_images_remaining * 4} seconds.')
        temp_dir = st.session_state['temp_dir']
        for obj_idx, n_images, caption in captions_remaining:
            for i in range(n_images):
                img = request_worker('generate', caption, args.username, args.password)
                img.save(temp_dir + f'images/{obj_idx}_g_{i}.png')

        st.success('Generating images done!')
        st.session_state['global_state'] = global_state[3]
        st.experimental_rerun()

    elif st.session_state['global_state'] == global_state[3]:
        temp_dir = st.session_state['temp_dir']
        if st.session_state['equalize_img']:
            equalize_contrast(temp_dir + 'images/', temp_dir + 'images_equalized/')
            imgs_dir = temp_dir + 'images_equalized/'
        else:
            imgs_dir = temp_dir + 'images/'
        st.write('Examples of the dataset:')
        example_imgs = [Image.open(imgs_dir + path) for path in os.listdir(imgs_dir)]
        show_images(example_imgs)
        create_download_button(temp_dir, imgs_dir, temp_dir + 'specs.json')
