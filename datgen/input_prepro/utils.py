
def get_inputs():
    n_objs = 2
    input_info = {i: {} for i in range(n_objs)}
    
    input_info[0]['obj_name'] = 'Apple'
    input_info[0]['size_random'] = False
    input_info[0]['size_min'] = 50
    input_info[0]['size_max'] = 80
    input_info[0]['vis_att'] = 'red'
    input_info[0]['loc_random'] = True
    input_info[0]['loc'] = ''

    input_info[1]['obj_name'] = 'pizza'
    input_info[1]['size_random'] = True
    input_info[1]['size_min'] = 50
    input_info[1]['size_max'] = 50
    input_info[1]['vis_att'] = 'Greasy;round'
    input_info[1]['loc_random'] = False
    input_info[1]['loc'] = 'table'

    return input_info