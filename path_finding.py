import numpy as np
import heapq
from scipy.spatial.distance import cdist
from scipy.ndimage import binary_dilation
from scipy.stats import qmc
from sklearn.preprocessing import MinMaxScaler
from scipy.ndimage import convolve


def astar(grid, start, goal, speed_based=True):
    rows, cols = grid.shape
    
    def heuristic(a, b):
        return np.linalg.norm(np.array(a) - np.array(b))
    
    def get_neighbors(pos):
        r, c = pos
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for neighbor in get_neighbors(current):
            grid_val = max(grid[neighbor], 0.000001)  # Avoid division by zero
            cost = (1 / grid_val) if speed_based else grid_val
            tentative_g_score = g_score[current] + cost
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None  # No path found

def find_closest_point(arr, point, region2=1):
    points_r2 = np.column_stack(np.where(arr == region2))
    
    if len(points_r2) == 0:
        return None, None  # If no points exist in region
    
    distances = cdist([point], points_r2)
    closest_idx = np.argmin(distances)
    closest_p2 = points_r2[closest_idx]
    
    return tuple(closest_p2)

def find_edges(array):
    # Create a binary mask of 1s
    binary_mask = array.astype(bool)

    # Perform binary dilation (expands 1s)
    dilated = binary_dilation(binary_mask)

    # Edge pixels are where dilation added new 1s (i.e., difference between dilated and original)
    edges = dilated & ~binary_mask

    # Get the indices of edge pixels
    edge_indices = np.argwhere(edges)
    
    return edge_indices
    
def select_evenly_spaced_points(edge_indices, num_points):
    """
    Selects evenly spaced points from the given edge indices.
    
    Parameters:
    - edge_indices: np.array of shape (N, 2), containing (row, col) indices of edge points.
    - num_points: int, the number of points to select.

    Returns:
    - np.array of shape (num_points, 2) with selected edge points.
    """
    if len(edge_indices) == 0:
        return np.array([])  # Return empty array if no edges exist
    
    if len(edge_indices) <= num_points:
        return edge_indices  # If we have fewer points than needed, return all

    # Compute step size to get approximately evenly spaced indices
    step = len(edge_indices) / num_points

    # Select indices at even intervals
    selected_indices = [edge_indices[int(i * step)] for i in range(num_points)]

    return np.array(selected_indices)

def uniformly_spaced_points(max_size, radius, n_points, seed, min_size=0):
    scaled_radius = radius/max_size

    engine = qmc.PoissonDisk(d=2, radius=scaled_radius, seed=seed)
    generated_points = engine.random(n_points)
    scaler = MinMaxScaler(feature_range=(min_size, max_size))
    scaled_points = scaler.fit_transform(generated_points).astype(np.int64)
    if scaled_points.shape[0] < n_points:
        print(f"[Warning] Could only generate {scaled_points.shape[0]} points")
    return scaled_points

def sum_neighbours(array, neighbour_range=1):
    # Define the convolution kernel
    size = 2 * neighbour_range + 1  # Kernel size based on the neighbour range
    kernel = np.ones((size, size))
    kernel[neighbour_range, neighbour_range] = 0  # Exclude the center cell

    # Perform convolution
    neighbour_sums = convolve(array, kernel, mode='constant', cval=0)

    return array + neighbour_sums