import streamlit as st
import pandas as pd

## TODO: add help in each input


def reset_values():
    st.session_state['i'] = 1
    st.session_state['obj'] = ''
    st.session_state['size_min'] = 50
    st.session_state['vis_attr'] = ''
    st.session_state['loc'] = ''


def store_info():
    res_info = {}
    res_info['Object name'] = st.session_state['obj'] 
    res_info['Object size'] = st.session_state['size_min']
    res_info['Visual attributes'] = st.session_state['vis_att'].split(';')
    res_info['Location'] = st.session_state['loc'].split(';')
    st.session_state['results']['i'] = res_info

    # TODO: store results to be picked up by other modules

    return


def get_object_info(i):
    st.subheader(f'Object {i}')

    # Define object_name
    st.session_state['obj_name'] = st.text_input(
        'Name of object', value=st.session_state['obj_name'], 
        key=f'{i}_obj_name',
        help='(...). Example:'
    )

    # Define size
    st.session_state['size_min'] = st.number_input(
        'Minimum occupancy of object (%)', min_value=0, max_value=100, 
        value=st.session_state['size_min'], step=5, key=f'{i}_min_size',
        help='(...). Example:'
    )

    # Define visual attributes
    st.session_state['vis_att'] = st.text_input(
        label='Visual attributes of the object (separated by ";")', 
        value=st.session_state['vis_att'] , key=f'{i}_vis_att',
        help='(...). Example:'
    )

    # Define location
    st.session_state['loc'] = st.text_input(
        label='Location/s of the object (separated by ";")', 
        value=st.session_state['loc'], key=f'{i}_loc',
        help='(...). Example:'
    )

    # Submit
    submitted = st.button(label="Submit")
    if submitted:
        store_info()
        reset_values()
        st.session_state['i'] += 1
        st.write(st.session_state['i'])
        #get_object_info(st.session_state['i'])
        submitted = False


if __name__ == '__main__':    
    st.title('DatGen')
    st.markdown('_Build your own Image Datasets._')

    if 'i' not in st.session_state:
        st.session_state['i'] = 1
        st.session_state['results'] = {}
        reset_values()
    
    get_object_info(st.session_state['i'])


## TODO: contrast and luminance should be matched outside of loop
    # # Define global visual attributes
    # yes_no_dict = {'No': 0, 'Yes': 1}

    # st.markdown('__Global attributes__')
    # cols_ga = st.columns(2)
    # st.session_state['contr'] = cols_ga[0].radio(
    #     label='Match Contrast', options=['No', 'Yes'], 
    #     index=yes_no_dict[st.session_state['contr']], key=f'{i}_contrast'
    # )
    # st.session_state['lum'] = cols_ga[1].radio(
    #     label='Match luminance', options=['No', 'Yes'],
    #     index=yes_no_dict[st.session_state['lum']], key=f'{i}_luminance'
    # )