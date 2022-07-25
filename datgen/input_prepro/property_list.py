from pathlib import Path


def create_property_list(inputs):
    for obj, obj_vals in inputs.items():
        inputs[obj]['obj'] = obj_vals['obj'].lower()
        inputs[obj]['vis_attr'] = [a.lower() for a in obj_vals['vis_attr']]
        inputs[obj]['loc'] = [l.lower() for l in obj_vals['loc']]
        inputs[obj]['obj_attr'] = [
            f'{a} {inputs[obj]["obj"]}' for a in inputs[obj]['vis_attr']
        ]
    return inputs
