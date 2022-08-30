import torch
from min_dalle import MinDalle
import os

model = MinDalle(
    models_root='../data/datgen_data/pretrained',
    dtype=torch.float32,
    device='cuda',
    is_mega=False,
    is_reusable=True
) if os.path.exists('../data/datgen_data/pretrained') else None


def generate_image(prompt: str):
    if prompt.strip() == '':
        raise ValueError('Empty Input')
    if model is None:
        raise EnvironmentError('Not a worker environment.')
    image = model.generate_image(text=prompt, seed=-1, grid_size=1, is_seamless=False,
                                 temperature=1, top_k=256, supercondition_factor=32, is_verbose=False)
    return image
