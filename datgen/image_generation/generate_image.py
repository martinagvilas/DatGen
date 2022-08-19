import torch
from min_dalle import MinDalle
import time

model = MinDalle(
    models_root='./pretrained',
    dtype=torch.float32,
    device='cpu',
    is_mega=True,
    is_reusable=True
)

start_time = time.time()
image = model.generate_image(
    text='The sidewalk near the corner of streets has one of the few vending machines.',
    seed=-1,
    grid_size=1,
    is_seamless=False,
    temperature=1,
    top_k=256,
    supercondition_factor=32,
    is_verbose=False
)
end_time = time.time()
print(end_time - start_time)
