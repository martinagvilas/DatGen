import streamlit as st
import argparse
from datgen.utils.utils import get_client_socket, read_img_from_socket

# initial specification formula
init_spec = {
    'name': '',
    'size': 50,
    'visual attributes': [''],
    'location': ['']
}

global_state = ['spec_config', 'img_match', 'img_gen', 'data_assem']


# convert chosen spec name to index
def get_chosen_spec_index():
    return int(st.session_state['chosen_spec'][7:])


# callback for button "Add"
def add_spec():
    st.session_state['specs'].append(init_spec)
    st.session_state['chosen_spec'] = 'Object ' + str(len(st.session_state['specs']) - 1)


# callback for button "Remove"
def remove_spec():
    if len(st.session_state['specs']) > 1:
        st.session_state['specs'].pop(get_chosen_spec_index())
        st.session_state['chosen_spec'] = 'Object 0'
    else:
        st.session_state['specs'] = [init_spec]


# callback for button "DatGen!"
def generate_images():
    st.session_state['global_state'] = global_state[2]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_n_spec', default=20, choices=range(50), type=int)
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

    # Connect to worker client
    if 'client_socket' not in st.session_state:
        st.session_state['client_socket'] = get_client_socket()

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
                 options=[f'Object {i}' for i in range(len(st.session_state['specs']))])
        st.button('DatGen!', on_click=generate_images)

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

        # print the specs for debugging
        st.write(st.session_state['specs'])

    elif st.session_state['global_state'] == global_state[2]:
        st.session_state['client_socket'].send('Retrieve:../data/conceptual_captions/1'.encode())
        img_retrieved = read_img_from_socket(st.session_state['client_socket'])
        st.image(img_retrieved, caption='Test retrieved img')

        st.session_state['client_socket'].send(
            'Generate:The sidewalk near the corner of streets has one of the few vending machines'.encode())
        img_generated = read_img_from_socket(st.session_state['client_socket'])
        st.image(img_generated, caption='Test generated img')
