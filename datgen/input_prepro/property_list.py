from pathlib import Path


from datgen.input_prepro.utils import get_inputs


def create_property_list():
    inputs = get_inputs()

    for obj, obj_vals in inputs.items():
        obj_name = obj_vals['obj_name'].lower()
        vis_att = [a.lower() for a in obj_vals['vis_att']]
        loc = [l.lower() for l in obj_vals['loc']]

        inputs[obj]['obj_name'] = obj_name
        print('done')

    return p_list
