import streamlit as st
import argparse

# initial specification formula
init_spec = {
    'name': '',
    'size': 50,
    'visual attributes': '',
    'location': ''
}


# callback for button "Add"
def add_spec():
    st.session_state['specs'].append(init_spec)
    st.session_state['chosen_spec_i'] = len(st.session_state['specs']) - 1


# callback for button "Remove"
def remove_spec():
    if len(st.session_state['specs']) > 0:
        st.session_state['specs'].pop(st.session_state['chosen_spec_i'])
        st.session_state['chosen_spec_i'] = 0


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

    # Session states initialization
    if 'specs' not in st.session_state:
        st.session_state['specs'] = []
        st.session_state['chosen_spec_i'] = 0

    # sidebar initialization
    with st.sidebar:
        st.markdown('<p class="big-font">DatGen</p>', unsafe_allow_html=True)
        st.title('Specifications')
        col1, col2, _, _, _ = st.columns(5, gap='small')
        col1.button('Add', on_click=add_spec)
        col2.button('Remove', on_click=remove_spec)
        spec_choice = st.radio(label='📌 your objects here',
                               index=st.session_state['chosen_spec_i'],
                               options=[f'Object {i}' for i in range(len(st.session_state['specs']))])

    if spec_choice is None:
        st.markdown('<p class="medium-font">Please specify your objects!</p>', unsafe_allow_html=True)
    else:
        i = int(spec_choice[7:])
        st.session_state['chosen_spec_i'] = i
        current_spec = st.session_state['specs'][i]
        st.subheader(f'Object {i}')
        form = st.form(key=f'{i}_obj_form', clear_on_submit=True)
        with form:
            # Define object
            name = st.text_input('Name of object', key=f'{i}_obj_name',
                                 value=current_spec['name'])

            # Define size
            size = st.number_input('Minimum occupancy of object (%)', min_value=0,
                                   max_value=100, step=5, key=f'{i}_min_size',
                                   value=current_spec['size'], help='(...). Example:')
            # Define visual attributes
            vis_att = st.text_input('Visual attributes of the object (separated by ";")', key=f'{i}_vis_att',
                                    value=current_spec['visual attributes'], help='(...). Example:')

            # Define location
            loc = st.text_input('Location/s of the object (separated by ";")', key=f'{i}_loc',
                                value=current_spec['location'], help='(...). Example:')

            submitted = st.form_submit_button(label="Submit")
            if submitted:
                spec = {'name': name,
                        'size': size,
                        'visual attributes': vis_att,
                        'location': loc}
                st.session_state['specs'][i] = spec
                st.experimental_rerun()

    # print the specs for debugging
    st.write(st.session_state['specs'])
