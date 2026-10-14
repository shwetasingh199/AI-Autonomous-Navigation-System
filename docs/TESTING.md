# Testing and evaluation

Run the automated checks with:

```bash
python -m unittest discover -s tests -v
```

The tests check deterministic map generation, route validity, and successful execution of A*, Dijkstra, and BFS on a seeded test environment.

For a fair algorithm comparison, keep the scenario, grid size, obstacle density, and random seed identical. Compare:
- `planning_time_ms`: wall-clock planner time (machine-dependent)
- `nodes_expanded`: number of popped/visited search nodes
- `path_length`: number of four-connected moves
- `collision_checks`: attempted neighbor-cell checks
- success/failure status

Do not compare a single runtime sample as a scientific benchmark. Run multiple seeds and report mean/median and failures for a more robust evaluation.
