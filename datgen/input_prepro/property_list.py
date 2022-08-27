from pathlib import Path


def create_property_list(inputs):
    for obj, vals in inputs.items():
        inputs[obj]['obj'] = vals['obj'].lower()
        inputs[obj]['vis_attr'] = [a.lower() for a in vals['vis_attr']]
        inputs[obj]['loc'] = [l.lower() for l in vals['loc']]
        if vals['vis_attr'] != ['']:
            inputs[obj]['obj_attr'] = [
                f'{a} {inputs[obj]["obj"]}' for a in inputs[obj]['vis_attr']
            ]
        else:
            inputs[obj]['obj_attr'] = ['']
    return inputs
