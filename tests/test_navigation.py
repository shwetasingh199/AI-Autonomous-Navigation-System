import unittest
from src.navigation.simulator import run_simulation, validate_path
from src.navigation.world import build_world
from src.navigation.planner import plan_path

class NavigationTests(unittest.TestCase):
    def test_deterministic_world(self):
        a = build_world(size=18, obstacle_density=0.2, seed=10)
        b = build_world(size=18, obstacle_density=0.2, seed=10)
        self.assertEqual(a.obstacles, b.obstacles)

    def test_all_algorithms_find_valid_path(self):
        for algorithm in ("astar", "dijkstra", "bfs"):
            result = run_simulation(algorithm=algorithm, seed=7, grid_size=18)
            self.assertTrue(result.success, result.message)
            self.assertGreaterEqual(len(result.path), 2)

    def test_route_avoids_obstacles(self):
        world = build_world(size=20, obstacle_density=0.25, seed=11)
        path, _, _, _ = plan_path(world, "astar")
        valid, message = validate_path(world, path)
        self.assertTrue(valid, message)

if __name__ == "__main__":
    unittest.main()
