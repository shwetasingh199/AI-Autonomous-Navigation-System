"""Reproducible 2D occupancy-grid environment generation."""
from dataclasses import dataclass
import random
from typing import Set, Tuple, List

Cell = Tuple[int, int]

@dataclass
class GridWorld:
    size: int
    start: Cell
    goal: Cell
    obstacles: Set[Cell]

    def in_bounds(self, cell: Cell) -> bool:
        x, y = cell
        return 0 <= x < self.size and 0 <= y < self.size

    def is_blocked(self, cell: Cell) -> bool:
        return cell in self.obstacles

    def neighbors(self, cell: Cell) -> List[Cell]:
        return [c for c in self.neighbors_unfiltered(cell)
                if self.in_bounds(c) and not self.is_blocked(c)]

    def neighbors_unfiltered(self, cell: Cell) -> List[Cell]:
        x, y = cell
        # Four-connected movement keeps path length interpretation simple.
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

def build_world(size: int = 24, obstacle_density: float = 0.20,
                seed: int = 7, scenario: str = "moderate") -> GridWorld:
    if size < 8:
        raise ValueError("Grid size must be at least 8.")
    if not 0 <= obstacle_density < 0.45:
        raise ValueError("Obstacle density must be in [0, 0.45).")
    rng = random.Random(seed)
    start, goal = (0, 0), (size - 1, size - 1)
    density_adjustment = {"easy": 0.65, "moderate": 1.0, "challenging": 1.35}
    if scenario not in density_adjustment:
        raise ValueError(f"Unknown scenario: {scenario}")
    density = min(0.42, obstacle_density * density_adjustment[scenario])
    obstacles: Set[Cell] = set()
    protected = {start, goal}
    for x in range(size):
        for y in range(size):
            cell = (x, y)
            if cell not in protected and rng.random() < density:
                obstacles.add(cell)
    # Keep a guaranteed corridor near the main diagonal to make demos reliable.
    # This is a simulation convenience, not a claim about real-world maps.
    for i in range(size):
        for cell in [(i, i), (min(size - 1, i + 1), i), (i, min(size - 1, i + 1))]:
            obstacles.discard(cell)
    return GridWorld(size=size, start=start, goal=goal, obstacles=obstacles)
