# GitHub Copilot Instructions for merchant-game-v2

## Project Architecture & File Responsibilities
- **game.py**: Main entry point and simulation loop. Handles setup, simulation ticks, and UI updates. Instantiates map, cities, markets, NPCs, and display.
- **map.py (GameMap)**: Handles world generation using Perlin/fractal noise, city placement, terrain, rivers, and city connections. Cities are stored in a dict by name. Map generation is deterministic (seeded RNG).
- **city.py (City)**: Represents a city with a local market and production buildings. Manages resource consumption and production per tick.
- **production_buildings.py**: Contains resource production logic. Each building (e.g., Farm, IronMine, ToolsSmithy) defines its outputs, required inputs, and production worth logic.
- **resources.py**: Defines resource types (enum) and the Resource class (name, amount).
- **global_market.py**: Tracks all cities and NPCs, manages global resource prices, aggregates production/consumption, and synchronizes local markets. Tracks price history and market share.
- **local_market.py**: Each city has a local market. Handles local resource prices, production/consumption history, and gold. Local prices are influenced by the global market.
- **npc.py (NPC)**: Represents non-player traders. Contains basic trading logic (buy/sell with cities based on price and inventory).
- **display.py**: Uses pygame for visualization. Renders the map, cities, and price charts. Handles user input for map navigation and zoom.
- **events.py**: Simple event system for extensibility.
- **path_finding.py**: Implements A* and utility functions for map navigation and city connection generation.
- **perlin_noise.py**: Utilities for generating Perlin and fractal noise for terrain.

## Project-Specific Conventions
- All resource and price histories are tracked as lists for analytics and charting.
- Cities are referenced by name (string) and stored in a dict in GameMap.
- Local and global markets are tightly coupled: each LocalMarket registers itself with the GlobalMarket on creation.
- Map generation and city placement are deterministic for reproducibility (seeded RNG).
- Visualization assets (e.g., castle sprite) are loaded from the `resources/` directory.

## Integration Points & Patterns
- All rendering is handled in display.py using pygame. Map and city overlays are composited each frame.
- Unit tests for core simulation logic are in `tests/`. Use fixtures for market/city setup.
- Map, rivers, and city positions are generated using Perlin/fractal noise and Delaunay triangulation.
- events.py provides a basic event manager for extensibility.

## NumPy in map.py
- **map.py heavily relies on NumPy** for efficient 2D array operations on large terrain grids (512x512).
- NumPy is used for:
  - **Terrain generation**: Using `np.digitize()` to classify elevation values into terrain types.
  - **Water flow simulation**: Using `np.gradient()`, `np.arctan2()`, and element-wise operations to calculate flow directions.
  - **River generation**: Using NumPy masking and indexing to overlay rivers on the terrain map.
  - **City placement**: Using NumPy random sampling, neighbor summing, and probabilistic filtering via `np.random.rand()` and `np.where()`.
  - **City connections**: Using `np.sort()`, `np.unique()`, and `np.column_stack()` for efficient k-NN edge deduplication.
  - **Terrain travel times**: Using NumPy array indexing to map terrain types to movement costs.
- All map generation must use `np.random.seed(seed)` at initialization to ensure deterministic and reproducible maps.
- NumPy's C-backed storage and broadcasting enable efficient handling of large grids without explicit loops where possible.

## Testing
- Place all unit tests in the `tests/` directory.
- Use pytest and fixtures for market/city setup.
- Ensure new resources/buildings are covered by tests.

## Determinism & Procedural Generation
- Always use seeded RNG for map and city generation to ensure reproducibility.
- Do not introduce non-deterministic behavior in map or city placement.

## Code Style
- Don't use docstrings.
- Follow PEP8 for Python code style.

## Logic and Visualization Separation
- **Keep game logic separate from visualization**: All simulation, market mechanics, resource production, and trading logic should reside in non-display modules (game.py, city.py, global_market.py, local_market.py, production_buildings.py, npc.py, etc.).
- **display.py is for rendering only**: The display module should only handle rendering of data and user input events. It should not contain business logic—instead, it queries the simulation state and renders it.
- **No pygame/visualization code in logic modules**: Game logic modules must remain agnostic to the visualization framework. This ensures the simulation can run without pygame and be tested independently.
- **Data flow**: Simulation logic → state updates → display reads state and renders. Never have display directly drive simulation logic.

---
For more details, see code comments in each file and AGENTS.md.

