"""Orchestrates world generation, planning, route validation, and metrics."""
from time import perf_counter
from .models import SimulationResult
from .world import build_world
from .planner import plan_path

def validate_path(world, path):
    """Verify endpoints, adjacency, bounds, and obstacle avoidance."""
    if not path:
        return False, "No collision-free route found."
    if path[0] != world.start or path[-1] != world.goal:
        return False, "Route endpoints do not match start/goal."
    for cell in path:
        if not world.in_bounds(cell) or world.is_blocked(cell):
            return False, f"Route contains invalid or blocked cell: {cell}"
    for a, b in zip(path, path[1:]):
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
            return False, f"Non-adjacent waypoints: {a} -> {b}"
    return True, "Valid collision-free route found."

def run_simulation(scenario="moderate", algorithm="astar", seed=7,
                   grid_size=24, obstacle_density=0.20):
    world = build_world(size=grid_size, obstacle_density=obstacle_density,
                        seed=seed, scenario=scenario)
    started = perf_counter()
    path, explored, expanded, checks = plan_path(world, algorithm=algorithm)
    elapsed_ms = (perf_counter() - started) * 1000.0
    valid, message = validate_path(world, path)
    success = bool(path) and valid
    if path and not valid:
        path = []
    return SimulationResult(
        scenario=scenario, algorithm=algorithm, seed=seed, grid_size=grid_size,
        obstacle_density=obstacle_density, start=world.start, goal=world.goal,
        obstacles=sorted(world.obstacles), path=path, explored=explored,
        success=success, message=message, planning_time_ms=elapsed_ms,
        nodes_expanded=expanded, collision_checks=checks
    )
