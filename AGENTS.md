# AGENTS.md

## Overview
This project is a simulation game focused on resource production, trading, and city development, with a strong emphasis on economic modeling and map-based visualization. The codebase is organized around several core components that interact to simulate a dynamic world.

## Architecture & Major Components
- **game.py**: Entry point and main loop. Orchestrates setup, simulation ticks, and UI updates. Instantiates the map, cities, markets, NPCs, and display.
- **map.py (GameMap)**: Generates the world map using Perlin/fractal noise, places cities, computes terrain types, rivers, and city connections. Cities are stored in a dict by name. Map generation is deterministic via a fixed seed.
- **city.py (City)**: Represents a city with a local market and production buildings. Handles resource consumption and production per tick.
- **production_buildings.py**: Abstracts resource production logic. Each building (e.g., Farm, IronMine, ToolsSmithy) defines what it produces, required inputs, and production worth logic.
- **resources.py**: Defines resource types (enum) and the Resource class (name, amount).
- **global_market.py**: Tracks all cities and NPCs, manages global resource prices, aggregates production/consumption, and synchronizes local markets. Price history and market share are tracked for analytics.
- **local_market.py**: Each city has a local market. Handles local resource prices, production/consumption history, and gold. Local prices are influenced by the global market.
- **npc.py (NPC)**: Represents non-player traders. Contains basic trading logic (buy/sell with cities based on price and inventory).
- **display.py**: Uses pygame for visualization. Renders the map, cities, and price charts. Handles user input for map navigation and zoom.
- **events.py**: Simple event system for extensibility (currently minimal usage).
- **path_finding.py**: Implements A* and utility functions for map navigation and city connection generation.
- **perlin_noise.py**: Utilities for generating Perlin and fractal noise for terrain.

## Data Flow & Simulation
- The main loop (game.py) updates global prices, processes city production/consumption, and triggers NPC trading each tick.
- Local markets update their prices based on global market signals and local supply/demand.
- Map and city positions are generated procedurally and deterministically.
- Visualization is updated every tick, showing both map and economic data.

## Developer Workflows
- **Run the game**: `python game.py` (requires pygame, numpy, matplotlib, sklearn, scipy)
- **Run tests**: `pytest tests/` (uses pytest)
- **Debug map generation**: Use `rivers_playground.py` for visualizing map features and flow accumulation.
- **Add new resources/buildings**: Update `ResourceName` in resources.py and add new building classes in production_buildings.py.

## Project-Specific Conventions
- All resource and price histories are tracked as lists for analytics and charting.
- Cities are referenced by name (string) and stored in a dict in GameMap.
- Local and global markets are tightly coupled: each LocalMarket registers itself with the GlobalMarket on creation.
- Map generation and city placement are deterministic for reproducibility (seeded RNG).
- Visualization assets (e.g., castle sprite) are loaded from the `resources/` directory.

## Integration Points & Patterns
- **Visualization**: All rendering is handled in display.py using pygame. Map and city overlays are composited each frame.
- **Testing**: Unit tests for core simulation logic are in `tests/`. Fixtures are used for market/city setup.
- **Procedural Generation**: Map, rivers, and city positions are generated using Perlin/fractal noise and Delaunay triangulation.
- **Event System**: events.py provides a basic event manager for future extensibility (currently not heavily used).

## Key Files & Directories
- `game.py`: Main entry point and simulation loop
- `map.py`: World generation and city placement
- `global_market.py`, `local_market.py`: Economic simulation
- `production_buildings.py`: Resource production logic
- `display.py`: Visualization and UI
- `tests/`: Unit tests for core logic
- `resources/`: Game assets (e.g., sprites)

## Example: Adding a New Resource
1. Add to `ResourceName` enum in resources.py
2. Update relevant market and production logic in local_market.py, global_market.py, and production_buildings.py
3. Add to city setup in game.py
4. Update tests if needed

## Example: Adding a New Building
1. Subclass `ProductionBuilding` in production_buildings.py
2. Define produced resource, required inputs, and production logic
3. Add to city setup in game.py
4. Add/modify tests in `tests/`

---
For more, see code comments in each file. This guide is auto-generated for AI agent productivity.

