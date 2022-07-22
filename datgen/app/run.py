import streamlit as st
import pandas as pd

## TODO: add help in each input


def reset_values():
    st.session_state['i'] = 1
    st.session_state['obj_name'] = ''
    st.session_state['size_random'] = True
    st.session_state['size_min'] = 50
    st.session_state['size_max'] = 50
    st.session_state['vis_att'] = ''
    st.session_state['loc_random'] = True
    st.session_state['loc'] = ''
    st.session_state['contr'] = 'Yes'
    st.session_state['lum'] = 'Yes'


def store_info():
    res_info = {}
    res_info['Object name'] = st.session_state['obj_name'] 
    
    if st.session_state['size_random']:
        res_info['Object size'] = 'Random'
    else:
        res_info['Object size'] = [
            st.session_state['size_min'], st.session_state['size_max']
        ]

    res_info['Visual attributes'] = st.session_state['vis_att'].split(';')

    if st.session_state['loc_random']:
        res_info['Location'] = 'Random'
    else:
        res_info['Location'] = st.session_state['loc'].split(';')

    res_info['Match contrast'] = st.session_state['contr']
    res_info['Match luminance'] = st.session_state['lum']

    st.session_state[f'results_{st.session_state["i"]}'] = res_info

    # TODO: temporaly store results to be picked up by other modules

    return


def get_object_info(i):
    st.subheader(f'Object {i}')

    # Define object_name
    st.session_state['obj_name'] = st.text_input(
        'Name of object', value=st.session_state['obj_name'], 
        key=f'{i}_obj_name'
    )

    # Define size
    st.markdown('__Size__')
    cols_s = st.columns(3)
    st.session_state['size_random'] = cols_s[0].checkbox(
        "Random", value=st.session_state['size_random'], key=f'{i}_rand_size'
    )
    st.session_state['size_min'] = cols_s[1].number_input(
        'Min occupancy (%)', min_value=0, max_value=100, 
        value=st.session_state['size_min'], step=5, key=f'{i}_min_size'
    )
    st.session_state['size_max'] = cols_s[2].number_input(
        'Max occupancy (%)', min_value=st.session_state['size_min'], 
        max_value=100, value=st.session_state['size_max'], 
        step=5, key=f'{i}_max_size'
    )

    # Define visual attributes
    st.markdown('__Visual Attributes__')
    st.session_state['vis_att'] = st.text_input(
        label='List of attributes separated by ";"', 
        value=st.session_state['vis_att'] , key=f'{i}_vis_att'
    )

    # Define location
    st.markdown('__Location__')
    cols_l = st.columns(2)
    st.session_state['loc_random'] = cols_l[0].checkbox(
        "Random", value=st.session_state['loc_random'], key=f'{i}_rand_loc'
    )
    st.session_state['loc'] = cols_l[1].text_input(
        label='List of attributes for location separated by ";"', 
        value=st.session_state['loc'], key=f'{i}_loc'
    )

    # Define global visual attributes
    yes_no_dict = {'No': 0, 'Yes': 1}

    st.markdown('__Global attributes__')
    cols_ga = st.columns(2)
    st.session_state['contr'] = cols_ga[0].radio(
        label='Match Contrast', options=['No', 'Yes'], 
        index=yes_no_dict[st.session_state['contr']], key=f'{i}_contrast'
    )
    st.session_state['lum'] = cols_ga[1].radio(
        label='Match luminance', options=['No', 'Yes'],
        index=yes_no_dict[st.session_state['lum']], key=f'{i}_luminance'
    )

    # Submit
    st.write(st.session_state['i'])
    submitted = st.button(label="Submit")
    if submitted:
        store_info()
        for i in range(1, st.session_state['i']):
            df = pd.DataFrame.from_dict(st.session_state[f'results_{i}'])
            df = df.rename(index={0: f'Object {i}'})
            st.dataframe(df)
        st.session_state['i'] += 1
        st.write(st.session_state['i'])
        reset_values()
        get_object_info(st.session_state['i'])


if __name__ == '__main__':    
    st.title('DatGen')
    st.markdown('_Build your own Image Datasets._')

    if 'i' not in st.session_state:
        st.session_state['i'] = 1
        reset_values()
    
    get_object_info(st.session_state['i'])


## TODO: contrast and luminance should be matched outside of loop