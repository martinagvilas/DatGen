
def get_inputs():
    ## IMPORTANT: empty should be of the form [""]
    n_objs = 4
    input_info = {i: {} for i in range(n_objs)}
    
    input_info[0]['obj'] = 'armadillo'
    input_info[0]['size_min'] = 0.1
    input_info[0]['vis_attr'] = ''.split(';')
    input_info[0]['loc'] = ''.split(';')
    input_info[0]['n_images'] = 100

    input_info[1]['obj'] = 'apple'
    input_info[1]['size_min'] = 0.1
    input_info[1]['vis_attr'] = 'Red'.split(';')
    input_info[1]['loc'] = ''.split(';')
    input_info[1]['n_images'] = 100

    input_info[2]['obj'] = 'Guitar'
    input_info[2]['size_min'] = 0.1
    input_info[2]['vis_attr'] = ''.split(';')
    input_info[2]['loc'] = 'store'.split(';')
    input_info[2]['n_images'] = 100

    input_info[3]['obj'] = 'pizza'
    input_info[3]['size_min'] = 0.1
    input_info[3]['vis_attr'] = 'Greasy;round'.split(';')
    input_info[3]['loc'] = 'kitchen;plate'.split(';')
    input_info[3]['n_images'] = 100

    return input_info