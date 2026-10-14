"""Grid path planners: A*, Dijkstra, and breadth-first search."""
import heapq
from collections import deque
from typing import Dict, List, Tuple, Set
from .world import GridWorld, Cell

def heuristic(a: Cell, b: Cell) -> float:
    """Manhattan distance for four-connected movement."""
    return float(abs(a[0] - b[0]) + abs(a[1] - b[1]))

def reconstruct_path(came_from: Dict[Cell, Cell], current: Cell) -> List[Cell]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def plan_path(world: GridWorld, algorithm: str = "astar"):
    """Return (path, explored_cells, expanded_node_count, collision_checks)."""
    algorithm = algorithm.lower()
    if algorithm not in {"astar", "dijkstra", "bfs"}:
        raise ValueError("algorithm must be 'astar', 'dijkstra', or 'bfs'")
    start, goal = world.start, world.goal
    if start == goal:
        return [start], [start], 0, 0

    came_from: Dict[Cell, Cell] = {}
    explored: List[Cell] = []
    visited: Set[Cell] = set()
    collision_checks = 0
    expanded = 0

    if algorithm == "bfs":
        queue = deque([start])
        visited.add(start)
        while queue:
            current = queue.popleft()
            explored.append(current)
            expanded += 1
            if current == goal:
                return reconstruct_path(came_from, goal), explored, expanded, collision_checks
            for nxt in world.neighbors_unfiltered(current):
                collision_checks += 1
                if not world.in_bounds(nxt) or world.is_blocked(nxt) or nxt in visited:
                    continue
                visited.add(nxt)
                came_from[nxt] = current
                queue.append(nxt)
        return [], explored, expanded, collision_checks

    open_heap = []
    g_score = {start: 0.0}
    priority = heuristic(start, goal) if algorithm == "astar" else 0.0
    heapq.heappush(open_heap, (priority, 0.0, start))
    closed: Set[Cell] = set()
    while open_heap:
        _, current_cost, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)
        explored.append(current)
        expanded += 1
        if current == goal:
            return reconstruct_path(came_from, goal), explored, expanded, collision_checks
        x, y = current
        for nxt in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            collision_checks += 1
            if not world.in_bounds(nxt) or world.is_blocked(nxt) or nxt in closed:
                continue
            tentative = current_cost + 1.0
            if tentative < g_score.get(nxt, float("inf")):
                g_score[nxt] = tentative
                came_from[nxt] = current
                h = heuristic(nxt, goal) if algorithm == "astar" else 0.0
                heapq.heappush(open_heap, (tentative + h, tentative, nxt))
    return [], explored, expanded, collision_checks
