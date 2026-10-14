"""Command-line entry point for a reproducible autonomous navigation demo."""
import argparse
import json
from pathlib import Path
from src.navigation.simulator import run_simulation
from src.navigation.visualization import save_map_figure

def main():
    parser = argparse.ArgumentParser(description="AI-Based Autonomous Navigation System")
    parser.add_argument("--scenario", choices=["easy", "moderate", "challenging"], default="moderate")
    parser.add_argument("--algorithm", choices=["astar", "dijkstra", "bfs"], default="astar")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--grid-size", type=int, default=24)
    parser.add_argument("--obstacle-density", type=float, default=0.20)
    args = parser.parse_args()

    result = run_simulation(
        scenario=args.scenario, algorithm=args.algorithm, seed=args.seed,
        grid_size=args.grid_size, obstacle_density=args.obstacle_density
    )
    Path("outputs").mkdir(exist_ok=True)
    report_path = Path("outputs/latest_run.json")
    report_path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
    save_map_figure(result, "outputs/latest_run.png")
    print(json.dumps(result.summary(), indent=2))
    print(f"\nSaved report: {report_path}")
    print("Saved map: outputs/latest_run.png")

if __name__ == "__main__":
    main()
