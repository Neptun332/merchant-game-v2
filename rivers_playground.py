from matplotlib import pyplot as plt
from map import GameMap
import numpy as np
    
np.random.seed(2137)
game_map = GameMap()
flow_accumulation = game_map.get_water_acumulation()

plt.figure(figsize=(15, 5))

# plt.subplot(131)
# plt.imshow(perlin_noise, cmap='terrain')
# plt.colorbar(label="Elevation")
# plt.title("Original Terrain")

plt.subplot(132)

# plt.quiver(np.flip(dA_dy,0), np.flip(dA_dx, 0))

plt.title("Gradient (downsampled)")

plt.subplot(133)
plt.imshow(flow_accumulation, cmap='Blues')
plt.colorbar(label="Log Flow Accumulation")
plt.title("Flow Accumulation")

plt.tight_layout()
plt.show()
pass