"""Typed data models shared by the navigation pipeline."""
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict, Any

Cell = Tuple[int, int]

@dataclass
class SimulationResult:
    scenario: str
    algorithm: str
    seed: int
    grid_size: int
    obstacle_density: float
    start: Cell
    goal: Cell
    obstacles: List[Cell]
    path: List[Cell]
    explored: List[Cell]
    success: bool
    message: str
    planning_time_ms: float
    nodes_expanded: int
    collision_checks: int

    @property
    def path_length(self) -> float:
        if len(self.path) < 2:
            return 0.0
        # Four-connected grid: each movement is one unit.
        return float(len(self.path) - 1)

    @property
    def obstacle_count(self) -> int:
        return len(self.obstacles)

    def summary(self) -> Dict[str, Any]:
        return {
            "scenario": self.scenario,
            "algorithm": self.algorithm,
            "success": self.success,
            "message": self.message,
            "path_length": self.path_length if self.success else None,
            "planning_time_ms": round(self.planning_time_ms, 3),
            "nodes_expanded": self.nodes_expanded,
            "collision_checks": self.collision_checks,
            "obstacle_count": self.obstacle_count,
            "grid_size": self.grid_size,
            "seed": self.seed,
        }

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["path_length"] = self.path_length
        data["obstacle_count"] = self.obstacle_count
        return data
