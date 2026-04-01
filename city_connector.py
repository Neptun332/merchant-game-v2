import numpy as np
from scipy.ndimage import label
from sklearn.neighbors import kneighbors_graph
from path_finding import astar


class CityConnector:
    def __init__(self, city_water_distance: int = 3):
        self._next_region_id = 1
        self.city_water_distance = city_water_distance

    def detect_terrain_regions(
        self,
        terrain_type_map: np.ndarray,
        terrain_types: list[int],
    ) -> dict[int, np.ndarray]:
        binary_mask = np.isin(terrain_type_map, terrain_types)
        connectivity = np.ones((3, 3), dtype=int)
        labeled_array, num_features = label(binary_mask, structure=connectivity)

        regions: dict[int, np.ndarray] = {}
        for local_region_id in range(1, num_features + 1):
            regions[self._next_region_id] = labeled_array == local_region_id
            self._next_region_id += 1

        return regions

    def create_path_between_cities(
        self,
        city_positions: np.ndarray,
        region_to_cities: dict[int, list[int]],
        terrain_movement_time: np.ndarray,
    ) -> np.ndarray:
        all_edges: list[np.ndarray] = []

        for region_id, city_indices in region_to_cities.items():
            if len(city_indices) < 2:
                continue

            region_city_positions = city_positions[city_indices]

            k = min(3, len(city_indices) - 1)
            knn_graph = kneighbors_graph(
                region_city_positions,
                n_neighbors=k,
                mode="distance",
                include_self=False,
            )

            knn_coo = knn_graph.tocoo()
            edges_raw = np.column_stack([knn_coo.row, knn_coo.col])

            edges_global = np.array(
                [[city_indices[i], city_indices[j]] for i, j in edges_raw]
            )

            edges_sorted = np.sort(edges_global, axis=1)
            edges_unique = np.unique(edges_sorted, axis=0)

            all_edges.extend(edges_unique)

        if all_edges:
            all_edges_arr = np.array(all_edges)
            edges = np.unique(all_edges_arr, axis=0)
        else:
            edges = np.array([])

        connections_map = np.zeros_like(terrain_movement_time)

        print(f"Drawing {len(edges)} connections on the map...")
        for i, j in edges:
            start_position = city_positions[i]
            end_position = city_positions[j]
            connection_path = astar(
                terrain_movement_time,
                tuple(start_position),
                tuple(end_position),
                speed_based=True,
            )

            connections_map[tuple(np.array(connection_path).T)] = 8

        return connections_map.astype(np.int8)

    def generate_cities_connections_land_regions(
        self,
        city_positions: np.ndarray,
        terrain_type_map: np.ndarray,
        land_travel_speed_mapping: np.ndarray,
    ) -> np.ndarray:
        n_cities = len(city_positions)
        if n_cities < 2:
            return np.zeros_like(terrain_movement_time).astype(np.int8)

        land_regions = self.detect_terrain_regions(terrain_type_map, [2, 3, 4, 5, 6, 7])

        city_to_region: dict[int, int] = {}
        for city_idx in range(n_cities):
            city_pos = tuple(city_positions[city_idx].astype(int))
            if (
                city_pos[0] < terrain_type_map.shape[0]
                and city_pos[1] < terrain_type_map.shape[1]
            ):
                for region_id, region_mask in land_regions.items():
                    if region_mask[city_pos]:
                        city_to_region[city_idx] = region_id
                        break

        region_to_cities = self._asign_region_to_city(city_to_region)

        print(f"Found {len(region_to_cities)} land regions with cities")
        print(
            f"Cities per land region: {[len(cities) for cities in region_to_cities.values()]}"
        )
        land_travel_speed = land_travel_speed_mapping[terrain_type_map]
        return self.create_path_between_cities(
            city_positions,
            region_to_cities,
            land_travel_speed
        )

    def generate_cities_connections_water_regions(
        self,
        city_positions: np.ndarray,
        terrain_type_map: np.ndarray,
        water_travel_speed_mapping: np.ndarray,
    ) -> np.ndarray:
        n_cities = len(city_positions)
        if n_cities < 2:
            return np.zeros_like(terrain_type_map).astype(np.int8)

        water_regions = self.detect_terrain_regions(terrain_type_map, [0, 1])

        city_to_region: dict[int, int] = {}
        cities_near_water = 0
        for city_idx in range(n_cities):
            city_pos = tuple(city_positions[city_idx].astype(int))
            if (
                city_pos[0] < terrain_type_map.shape[0]
                and city_pos[1] < terrain_type_map.shape[1]
            ):
                for region_id, region_mask in water_regions.items():
                    if self._city_is_near_water(
                        region_mask, terrain_type_map, city_pos, max_distance=self.city_water_distance
                    ):
                        cities_near_water += 1
                        city_to_region[city_idx] = region_id
                        break

        region_to_cities = self._asign_region_to_city(city_to_region)

        print(f"Cities within {self.city_water_distance} tiles of water: {cities_near_water}/{n_cities}")
        print(
            f"Cities per water region: {[len(cities) for cities in region_to_cities.values()]}"
        )

        water_travel_speed = water_travel_speed_mapping[terrain_type_map]
        return self.create_path_between_cities(
            city_positions,
            region_to_cities,
            water_travel_speed,
        )

    @staticmethod
    def _city_is_near_water(
        water_region_mask: np.ndarray,
        terrain_type_map: np.ndarray,
        city_pos: tuple[int, int],
        max_distance: int,
    ) -> bool:
        min_row = max(0, city_pos[0] - max_distance)
        max_row = min(terrain_type_map.shape[0], city_pos[0] + max_distance + 1)
        min_col = max(0, city_pos[1] - max_distance)
        max_col = min(terrain_type_map.shape[1], city_pos[1] + max_distance + 1)

        nearby_water = np.argwhere(water_region_mask[min_row:max_row, min_col:max_col])
        if nearby_water.size == 0:
            return False

        nearby_water[:, 0] += min_row
        nearby_water[:, 1] += min_col
        distances = np.sqrt(
            (nearby_water[:, 0] - city_pos[0]) ** 2
            + (nearby_water[:, 1] - city_pos[1]) ** 2
        )
        return bool(np.any(distances <= max_distance))

    @staticmethod
    def _asign_region_to_city(city_to_region: dict[int, int]) -> dict[int, list[int]]:
        region_to_cities: dict[int, list[int]] = {}
        for city_idx, region_id in city_to_region.items():
            if region_id not in region_to_cities:
                region_to_cities[region_id] = []
            region_to_cities[region_id].append(city_idx)
        return region_to_cities
