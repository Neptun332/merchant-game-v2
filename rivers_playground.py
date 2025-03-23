from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from perlin_noise import generate_fractal_noise_2d
import numpy as np

np.random.seed(2137)
perlin_noise = generate_fractal_noise_2d((64, 64), (2, 2), 3)
dA_dx, dA_dy = np.gradient(perlin_noise)

def calculate_flow_accumulation_v2(dA_dx, dA_dy):
    # scaler = MinMaxScaler(feature_range=(-1, 1))
    # dA_dx = scaler.fit_transform(dA_dx)
    # dA_dy = scaler.fit_transform(dA_dy)

    height, width = dA_dx.shape
    accumulation = np.ones_like(dA_dx)

    magnitude = np.sqrt(dA_dx**2 + dA_dy**2)

    directions = np.zeros((height, width), dtype=int)
    angles = np.arctan2(dA_dx, dA_dy) + np.pi
    ##angles = np.arctan2(dA_dx, dA_dy) + (np.pi/2)

    # Define angle ranges (pi/4 = 45° per section)
    angle_bins = np.linspace(0, 2 * np.pi, 9)  # 8 segments

    # Digitize angles to find corresponding direction
    angle_indices = np.digitize(angles, angle_bins) - 1  # Get bin indices

    # Ensure values wrap correctly
    angle_indices = np.mod(angle_indices, 8)  # Ensure valid indices

    directions = [
        (1, 0),    # Down
        (1, -1),   # Down-Left
        (0, -1),   # Left
        (-1, -1),   # Up-Left
        (-1, 0),   # Up
        (-1, 1),   # Up-Right
        (0, 1),    # Right
        (1, 1),    # Down-Right
    ]

    # Map angle indices to direction vectors (apply to each element)
    index_shifts = np.array([directions[i] for i in angle_indices.flatten()]).reshape(angle_indices.shape + (2,))

    magnitude =  np.sqrt(dA_dx**2 + dA_dy**2)
    magnitude = np.where(perlin_noise < 0.5, magnitude, 1) # forces water to flow from high ground
    magnitude= np.stack([magnitude, magnitude], axis=-1)

    zeros = np.full(index_shifts.shape, np.array([0, 0]))
    index_shifts = np.where(magnitude > 0.05, index_shifts, zeros)

    for _ in range(20):
        rain = np.ones_like(accumulation)
        current_water = accumulation + rain
        rain_movement = np.zeros_like(accumulation)
        for i in range(rain_movement.shape[0]):
            for j in range(rain_movement.shape[1]):
                rain_shift = index_shifts[i, j]
                next_rain_postion_i = min(rain_movement.shape[0] - 1, max(0, i + rain_shift[0]))
                next_rain_postion_j = min(rain_movement.shape[1] - 1, max(0, j + rain_shift[1]))
                rain_movement[next_rain_postion_i, next_rain_postion_j] = current_water[i, j]

        accumulation = rain_movement

    return accumulation
    
magnitude = np.sqrt(dA_dx**2 + dA_dy**2)
dA_dx = np.where(magnitude > 0.05, dA_dx, 0)
dA_dy = np.where(magnitude > 0.05, dA_dy, 0)
flow_accumulation = calculate_flow_accumulation_v2(dA_dx, dA_dy)

plt.figure(figsize=(15, 5))

plt.subplot(131)
plt.imshow(perlin_noise, cmap='terrain')
plt.colorbar(label="Elevation")
plt.title("Original Terrain")

plt.subplot(132)

plt.quiver(np.flip(dA_dy,0), np.flip(dA_dx, 0))

plt.title("Gradient (downsampled)")

plt.subplot(133)
plt.imshow(np.log1p(flow_accumulation), cmap='Blues')
plt.colorbar(label="Log Flow Accumulation")
plt.title("Flow Accumulation")

plt.tight_layout()
plt.show()
pass