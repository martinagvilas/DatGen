
def get_inputs():
    n_objs = 2
    input_info = {i: {} for i in range(n_objs)}
    
    input_info[0]['obj'] = 'armadillo'
    input_info[0]['size_min'] = 0.1
    input_info[0]['vis_attr'] = 'red'.split(';')
    input_info[0]['loc'] = ''.split(';')
    input_info[0]['n_images'] = 100

    input_info[1]['obj'] = 'pizza'
    input_info[1]['size_min'] = 0.1
    input_info[1]['vis_attr'] = 'Greasy;round'.split(';')
    input_info[1]['loc'] = 'kitchen;plate'.split(';')
    input_info[1]['n_images'] = 100

    return input_info