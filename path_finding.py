import numpy as np
import heapq
from scipy.spatial.distance import cdist


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
            cost = (1 / grid[neighbor]) if speed_based else grid[neighbor]
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