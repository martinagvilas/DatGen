
def get_inputs():
    n_objs = 2
    input_info = {i: {} for i in range(n_objs)}
    
    input_info[0]['obj_name'] = 'Apple'
    input_info[0]['size_min'] = 50
    input_info[0]['vis_attr'] = 'red'
    input_info[0]['loc'] = ''
    input_info[0]['n_images'] = 100

    input_info[1]['obj_name'] = 'pizza'
    input_info[1]['size_min'] = 50
    input_info[1]['vis_attr'] = 'Greasy;round'
    input_info[1]['loc'] = 'table'
    input_info[1]['n_images'] = 100

    return input_info