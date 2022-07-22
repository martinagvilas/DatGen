import streamlit as st
import argparse

# initial specification formula
init_spec = {
    'Object name': '',
    'Object size': [50, 50],
    'Visual attributes': [''],
    'Location': [''],
    'Match contrast': 'No',
    'Match luminance': 'No',
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
            obj_name = st.text_input('Name of object', key=f'{i}_obj_name',
                                     value=current_spec['Object name'])

            # Define size
            st.markdown('__Size__')
            cols_s = st.columns(3)
            size_random = cols_s[0].checkbox("Random", key=f'{i}_rand_size',
                                             value=True if current_spec['Object size'] == 'Random' else False)
            size_min = cols_s[1].number_input(
                'Min occupancy (%)', min_value=0, max_value=100, step=5, key=f'{i}_min_size',
                value=current_spec['Object size'][0] if current_spec['Object size'] != 'Random' else 50)
            size_max = cols_s[2].number_input(
                'Max occupancy (%)', min_value=0, max_value=100, step=5, key=f'{i}_max_size',
                value=current_spec['Object size'][1] if current_spec['Object size'] != 'Random' else 50)

            # Define visual attributes
            st.markdown('__Visual Attributes__')
            vis_att = st.text_input(
                label='List of attributes separated by ";"', key=f'{i}_vis_att',
                value='' if current_spec['Visual attributes'] == 'Random' else ';'.join(
                    current_spec['Visual attributes']))

            # Define location
            st.markdown('__Location__')
            cols_l = st.columns(2)
            loc_random = cols_l[0].checkbox("Random", key=f'{i}_rand_loc',
                                            value=True if current_spec['Location'] == 'Random' else False)
            loc = cols_l[1].text_input(
                label='List of attributes for location separated by ";"', key=f'{i}_loc',
                value='' if current_spec['Location'] == 'Random' else ';'.join(current_spec['Location']))

            # Define global visual attributes
            st.markdown('__Global attributes__')
            cols_ga = st.columns(2)
            contr = cols_ga[0].radio(label='Match Contrast', options=['No', 'Yes'], key=f'{i}_contrast',
                                     index=0 if current_spec['Match contrast'] == 'No' else 1)
            lum = cols_ga[1].radio(label='Match luminance', options=['No', 'Yes'], key=f'{i}_luminance',
                                   index=0 if current_spec['Match luminance'] == 'No' else 1)

            submitted = st.form_submit_button(label="Submit")
            if submitted:
                spec = {'Object name': obj_name}

                if size_random:
                    spec['Object size'] = 'Random'
                else:
                    spec['Object size'] = [size_min, size_max]

                spec['Visual attributes'] = vis_att.split(';')

                if loc_random:
                    spec['Location'] = 'Random'
                else:
                    spec['Location'] = loc.split(';')

                spec['Match contrast'] = contr
                spec['Match luminance'] = lum

                st.session_state['specs'][i] = spec
                st.experimental_rerun()
    # print the specs for debugging
    st.write(st.session_state['specs'])

