import torch
from min_dalle import MinDalle

model = MinDalle(
    models_root='image_generation/pretrained',
    dtype=torch.float32,
    device='cuda',
    is_mega=False,
    is_reusable=True
)


def generate_image(prompt):
    image = model.generate_image(text=prompt, seed=-1, grid_size=1, is_seamless=False,
                                 temperature=1, top_k=256, supercondition_factor=32, is_verbose=False)
    return image
