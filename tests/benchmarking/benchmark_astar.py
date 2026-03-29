import numpy as np
import time
from path_finding import astar


def benchmark_astar():

    # Test with different grid conditions
    print("\n" + "=" * 70)
    print("TESTING DIFFERENT GRID CONDITIONS (512x512 grid)")
    print("=" * 70)
    
    test_grid_size = 1024
    conditions = {
        # "Uniform low cost": np.ones((test_grid_size, test_grid_size)) * 0.5,
        "Uniform high cost": np.ones((test_grid_size, test_grid_size)) * 2.0,
        "Random mixed": np.random.uniform(0.5, 2.0, (test_grid_size, test_grid_size)),
        "Noisy": np.random.uniform(0.1, 3.0, (test_grid_size, test_grid_size)),
    }
    
    start = (0, 0)
    goal = (test_grid_size - 1, test_grid_size - 1)
    
    for condition_name, grid in conditions.items():
        print(f"\nCondition: {condition_name}")
        print("-" * 70)
        
        total_time = 0
        for run in range(3):
            start_time = time.perf_counter()
            path = astar(grid, start, goal, speed_based=True)
            end_time = time.perf_counter()
            
            elapsed = end_time - start_time
            total_time += elapsed
            
            if path is not None:
                print(f"  Run {run + 1}: {elapsed*1000:.2f}ms")
            else:
                print(f"  Run {run + 1}: {elapsed*1000:.2f}ms (No path)")
        
        avg_time = total_time / 3
        print(f"  Average: {avg_time*1000:.2f}ms")
    
    print("\n" + "=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    benchmark_astar()

