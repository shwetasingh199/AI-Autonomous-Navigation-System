# AI-Based Autonomous Navigation System

A laptop-friendly virtual navigation lab that generates a 2D occupancy grid, plans a collision-free route, validates it, visualizes the search process, and records measurable run metrics. It is designed as an educational portfolio project for robotics, autonomy, AI, and software engineering roles.

> **Scope note:** This is a grid-world simulation prototype. It is not a real vehicle controller, does not consume live camera/LiDAR data, and is not safety-certified.

## Features

- Interactive Streamlit frontend with scenario, grid-size, obstacle-density, algorithm, and random-seed controls
- Reproducible obstacle maps
- A*, Dijkstra, and breadth-first search (BFS) path planners
- Route validation: endpoint, adjacency, bounds, and obstacle checks
- Metrics: planning time, expanded nodes, collision checks, path length, and obstacle count
- Downloadable JSON run report and CSV waypoints
- CLI mode for repeatable runs and saved PNG/JSON outputs
- Unit tests for deterministic maps and route validity

## Problem statement

A mobile agent needs to reach a goal in an environment containing blocked cells. The system represents the environment as an occupancy grid, searches for a route, checks that route against obstacles, and reports the performance of the planning algorithm.

## Industry relevance

Occupancy grids and graph-search planners are useful building blocks in mobile robotics, warehouse automation, service robots, and autonomy research. Production systems add real sensors, localization, dynamic-obstacle handling, robust control, safety systems, and extensive validation.

## Architecture

```text
Controls -> World generator -> Occupancy grid -> A* / Dijkstra / BFS
                                              -> Route validation
                                              -> Metrics + visualization
                                              -> JSON / CSV / PNG exports
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for module details.

## Tech stack

- Python 3.10–3.12
- Streamlit (frontend)
- NumPy / pandas (data support and waypoint table)
- Matplotlib (map visualization)
- Python standard library (search algorithms, timing, JSON, testing)

No GPU, ROS installation, external dataset, or pretrained model is required.

## Folder structure

```text
AI-Autonomous-Navigation-System/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/navigation/
│   ├── models.py
│   ├── world.py
│   ├── planner.py
│   ├── simulator.py
│   └── visualization.py
├── tests/test_navigation.py
├── docs/ARCHITECTURE.md
├── docs/TESTING.md
└── outputs/.gitkeep
```

## Installation

### Windows PowerShell

```powershell
cd AI-Autonomous-Navigation-System
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
cd AI-Autonomous-Navigation-System
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the frontend

```bash
streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`. Open it in your browser and press **Run navigation** after changing the settings.

## Run from the command line

```bash
python main.py --scenario moderate --algorithm astar --seed 7 --grid-size 24 --obstacle-density 0.20
```

Generated files:
- `outputs/latest_run.json` — run metrics and route details
- `outputs/latest_run.png` — rendered environment and route

Available scenarios: `easy`, `moderate`, `challenging`. Available algorithms: `astar`, `dijkstra`, `bfs`.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Understanding the visualization

- Green: start
- Red: goal
- Dark: obstacle
- Blue: final planned route
- Yellow: cells explored by the planner
- Light: free cells

## Results and limitations

The app reports whether a route was found and route/search metrics. Planning time depends on your computer and should not be presented as a universal benchmark. Map perception is simulated; there is no camera object detection or dynamic obstacle avoidance in this baseline.

## Screenshots and demo assets

Save genuine screenshots from your own run under `docs/images/`, for example:
- `dashboard_overview.png`
- `route_planning_astar.png`
- `algorithm_comparison.png`
- `terminal_cli_run.png`

Add them here when captured:

```markdown
![Dashboard overview](docs/images/dashboard_overview.png)
```

## Future improvements

1. Run repeated seeds and add algorithm comparison charts.
2. Add user-defined start/goal points and map editing.
3. Add dynamic obstacles and replanning.
4. Integrate OpenCV camera-based perception using recorded test videos.
5. Add ROS 2 / Gazebo or Webots adapter.
6. Add CARLA for a road-driving scenario.
7. Explore SLAM, localization, model-predictive control, and reinforcement learning after validating simpler baselines.

## Learning outcomes

- Graph search and heuristic design
- Occupancy-grid representations
- Reproducible experiments and evaluation metrics
- Modular Python architecture and automated tests
- Streamlit dashboarding and Git-based documentation


## Resume bullet examples

Use these only after running and testing the project:
- Built a Python/Streamlit autonomous-navigation simulator using A*, Dijkstra, and BFS on reproducible occupancy grids.
- Implemented route validation and tracked planning time, expanded nodes, collision checks, and path length to evaluate planner behavior.
- Added CLI execution, downloadable JSON/CSV artifacts, map visualization, and unit tests for reproducible experiments.

## Author

SHWETA SINGH
