from matplotlib import pyplot as plt
from perlin_noise import generate_fractal_noise_2d
import numpy as np

np.random.seed(2137)
perlin_noise = generate_fractal_noise_2d((64, 64), (2, 2), 3)
dA_dx, dA_dy = np.gradient(perlin_noise)

def calculate_flow_accumulation_v2(dA_dx, dA_dy):
    height, width = dA_dx.shape
    accumulation = np.ones_like(dA_dx)
    magnitude = np.sqrt(dA_dx**2 + dA_dy**2)
    with np.errstate(divide='ignore', invalid='ignore'):
        flow_x = np.where(magnitude > 0, -dA_dx/magnitude, 0)
        flow_y = np.where(magnitude > 0, -dA_dy/magnitude, 0)
    directions = np.zeros((height, width), dtype=int)
    angles = np.arctan2(flow_y, flow_x)
    directions = ((angles + np.pi) * 4 / np.pi).astype(int) % 8
    for _ in range(5):
        new_accumulation = np.ones_like(accumulation)
        for dir_idx in range(8):
            if dir_idx == 0:
                shifted = np.roll(accumulation * (directions == dir_idx), -1, axis=1)
            elif dir_idx == 1:
                shifted = np.roll(np.roll(accumulation * (directions == dir_idx), -1, axis=0), -1, axis=1)
            elif dir_idx == 2:
                shifted = np.roll(accumulation * (directions == dir_idx), -1, axis=0)
            elif dir_idx == 3:
                shifted = np.roll(np.roll(accumulation * (directions == dir_idx), -1, axis=0), 1, axis=1)
            elif dir_idx == 4:
                shifted = np.roll(accumulation * (directions == dir_idx), 1, axis=1)
            elif dir_idx == 5:
                shifted = np.roll(np.roll(accumulation * (directions == dir_idx), 1, axis=0), 1, axis=1)
            elif dir_idx == 6:
                shifted = np.roll(accumulation * (directions == dir_idx), 1, axis=0)
            elif dir_idx == 7:
                shifted = np.roll(np.roll(accumulation * (directions == dir_idx), 1, axis=0), -1, axis=1)
            new_accumulation += shifted
        accumulation = new_accumulation
        accumulation[0, :] = 1
        accumulation[-1, :] = 1
        accumulation[:, 0] = 1
        accumulation[:, -1] = 1
    return accumulation

flow_accumulation = calculate_flow_accumulation_v2(dA_dx, dA_dy)

plt.figure(figsize=(15, 5))

plt.subplot(131)
plt.imshow(perlin_noise, cmap='terrain')
plt.colorbar(label="Elevation")
plt.title("Original Terrain")

plt.subplot(132)
plt.quiver(np.flip(dA_dx, 0), np.flip(dA_dy,0))
plt.title("Gradient (downsampled)")

plt.subplot(133)
plt.imshow(np.log1p(flow_accumulation), cmap='Blues')
plt.colorbar(label="Log Flow Accumulation")
plt.title("Flow Accumulation")

plt.tight_layout()
plt.show()