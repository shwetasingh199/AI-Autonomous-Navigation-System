# Architecture

```text
Scenario + seed + grid settings
             |
             v
    Grid-world generator
             |
             v
 Occupancy grid / simulated perception
             |
             v
  Path planner (A* / Dijkstra / BFS)
             |
             v
   Route validation and metrics
             |
       +-----+------+
       |            |
       v            v
 Streamlit UI   JSON / PNG / CSV exports
```

## Components
- `world.py`: creates the occupancy grid and exposes collision/neighbor queries.
- `planner.py`: runs A*, Dijkstra, or BFS and records explored nodes.
- `simulator.py`: coordinates the pipeline and validates the output route.
- `visualization.py`: renders the grid, explored cells, and route.
- `app.py`: frontend controls, metrics, map view, and downloadable results.

## Engineering boundaries
The current version simulates map perception by directly generating an occupancy grid. It does not use a camera, lidar, SLAM, ROS, or a physical robot. Those can be future adapters around the same planner interface.
