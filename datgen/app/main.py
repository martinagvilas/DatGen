import streamlit as st
import pandas as pd

## TODO: add help in each input

# def update_objects():
#     for i in range(1, st.session_state['i']):
#         create_object_form(i)
#     st.session_state['new_object'] = st.button(
#         'Add object', key=f'{st.session_state["i"]}_button'
#     )

def create_object_form(i):
    st.subheader(f'Object {i}')
    form = st.form(key=f'{i}_obj_form', clear_on_submit=True)
    with form:
        # Define object
        obj_name = st.text_input('Name of object', value='', key=f'{i}_obj_name')

        # Define size
        st.markdown('__Size__')
        cols_s = st.columns(3)
        size_random = cols_s[0].checkbox("Random", key=f'{i}_rand_size')
        size_min = cols_s[1].number_input(
            'Min occupancy (%)', min_value=0, max_value=100, value=50, step=5,
            key=f'{i}_min_size'
        )
        st.session_state['size_min'] = size_min
        size_max = cols_s[2].number_input(
            'Max occupancy (%)', min_value=st.session_state['size_min'], 
            max_value=100, value=st.session_state['size_min'], 
            step=5, key=f'{i}_max_size'
        )

        # Define visual attributes
        st.markdown('__Visual Attributes__')
        vis_att = st.text_input(
            label='List of attributes separated by ";"', value='',
            key=f'{i}_vis_att'
        )

        # Define location
        st.markdown('__Location__')
        cols_l = st.columns(2)
        loc_random = cols_l[0].checkbox("Random", key=f'{i}_rand_loc')
        loc = cols_l[1].text_input(
            label='List of attributes for location separated by ";"', value='',
            key=f'{i}_loc'
        )

        # Define global visual attributes
        st.markdown('__Global attributes__')
        cols_ga = st.columns(2)
        contr = cols_ga[0].radio(
            label='Match Contrast', options=['No', 'Yes'], key=f'{i}_contrast'
        )
        lum = cols_ga[1].radio(
            label='Match luminance', options=['No', 'Yes'], key=f'{i}_luminance'
        )
        submitted = st.form_submit_button(label="Submit")
        
        if submitted:
            res_info = {}
            res_info['Object name'] = obj_name
            
            if size_random:
                res_info['Object size'] = 'Random'
            else:
                res_info['Object size'] = [size_min, size_max]

            res_info['Visual attributes'] = vis_att.split(';')

            if loc_random:
                res_info['Location'] = 'Random'
            else:
                res_info['Location'] = loc.split(';')

            res_info['Match contrast'] = contr
            res_info['Match luminance'] = lum

            st.session_state[f'results_{i}'] = res_info
            st.session_state['i'] += 1


if __name__ == '__main__':    
    st.title('DatGen')
    st.markdown('_Build your own Image Datasets._')

    if 'i' not in st.session_state:
        st.session_state['i'] = 1
        #st.session_state['new_object'] = True
    st.session_state.size_min = 50

    create_object_form(st.session_state['i'])

    for i in range(1, st.session_state['i']):
        df = pd.DataFrame.from_dict(st.session_state[f'results_{i}'])
        df = df.rename(index={0: f'Object {i}'})
        st.dataframe(df)
