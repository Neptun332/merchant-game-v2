from matplotlib import pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from path_finding import astar, find_closest_point, find_edges, select_evenly_spaced_points
from perlin_noise import generate_fractal_noise_2d
from resources import ResourceName, Resource
from local_market import LocalMarket
from city import City
from scipy.stats import qmc



class GameMap:
    def __init__(self, seed=2137):
        np.random.seed(seed)
        self.seed = seed
        self.cities: dict[str, City] = {}
        #self.terrain_noise = generate_fractal_noise_2d((64, 64), (2, 2), 3)
        self.terrain_noise = generate_fractal_noise_2d((512, 512), (4, 4), 5)

        # 0 - DEEP_WATER
        # 1 - SHALLOW_WATER
        # 2 - SAND
        # 3 - PLAINS
        # 4 - HIGHLAND
        # 5 - MOUNTAIN
        # 6 - MOUNTAIN_PEAK

        # 7 - RIVER
        self.sea_level = -0.2
        self.mointain_peak = 0.9

        self.rivers_density = 0.1
        self.terrain_type_map = self.get_terrain_type_map()
        self.water_map = self.get_water_map()
        self.water_acumulation_map = self.get_water_acumulation()
        self.river_map = self.get_rivers_map()
        self.terrain_type_map = np.where(self.river_map == 0, self.terrain_type_map, self.river_map)

        dA_dx, dA_dy = np.gradient(self.terrain_noise)
        self.magnitude = np.sqrt(dA_dx**2 + dA_dy**2)

    def add_city(self, city: City):
        self.cities[city.name] = city 

    def get_city(self, name: str) -> City | None:
        return self.cities.get(name, None)
    
    def get_terrain_type_map(self): 
        return np.digitize(
            self.terrain_noise,
            [-1.1, -0.6, self.sea_level, -0.1, 0.3, 0.7, self.mointain_peak, 1.1]
        ) - 1
    
    def get_water_map(self):
        return np.where(self.terrain_noise < self.sea_level, 1, 0)
    
    def get_mountain_peak_map(self):
        return np.where(self.terrain_noise > self.mointain_peak, 1, 0)

    def get_water_acumulation(self):
        dA_dx, dA_dy = np.gradient(self.terrain_noise)

        height, width = dA_dx.shape
        accumulation = np.ones_like(dA_dx)

        magnitude = np.sqrt(dA_dx**2 + dA_dy**2)

        directions = np.zeros((height, width), dtype=int)
        angles = np.arctan2(dA_dx, dA_dy) + np.pi

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
        # forces water to flow from high ground even if there is flat ground
        magnitude = np.where(self.terrain_noise > self.sea_level, magnitude, 1) 
        magnitude= np.stack([magnitude, magnitude], axis=-1)

        zeros = np.full(index_shifts.shape, np.array([0, 0]))
        index_shifts = np.where(magnitude < 0.35, index_shifts, zeros)

        for _ in range(30):
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
    
    def get_random_locations_in_mointain_peaks(self, radius, n_points):
        mountain_peak_map = self.get_mountain_peak_map()
        point_on_the_whole_map = self.uniformly_spcaed_points(mountain_peak_map.shape[0]-1, radius, n_points)
        valid_position =  mountain_peak_map[tuple(point_on_the_whole_map.T)] == 1
        return point_on_the_whole_map[valid_position]
    
    def get_rivers_map(self):
        number_of_rivers = int(self.rivers_density * self.terrain_noise.shape[0])  # Round down to ensure feasibility
        mountain_peak_edges = find_edges(self.get_mountain_peak_map())
        rivers_source_location = select_evenly_spaced_points(mountain_peak_edges, number_of_rivers)
        print(f"Genereted {rivers_source_location.shape[0]} rivers")
        rivers_map = np.zeros_like(self.terrain_noise)
        for river_source in rivers_source_location:
            river_delta = tuple(find_closest_point(self.water_map, river_source))
            river_course = astar(self.water_acumulation_map, tuple(river_source), river_delta, speed_based=True)
            rivers_map[tuple(np.array(river_course).T)] = 7
        return rivers_map.astype(np.int8)
    
    def uniformly_spcaed_points(self, max_size, radius, n_points, min_size=0):
        scaled_radius = radius/max_size

        engine = qmc.PoissonDisk(d=2, radius=scaled_radius, seed=self.seed)
        generated_points = engine.random(n_points)
        scaler = MinMaxScaler(feature_range=(min_size, max_size))
        scaled_points = scaler.fit_transform(generated_points).astype(np.int64)
        if scaled_points.shape[0] < n_points:
            print(f"[Warning] Could only generate {scaled_points.shape[0]} points")
        return scaled_points
    

