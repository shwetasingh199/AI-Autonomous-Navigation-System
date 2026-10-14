"""Matplotlib rendering for the occupancy grid and planned route."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from .world import Cell

def render_map_figure(result):
    size = result.grid_size
    # 0 free, 1 obstacle, 2 explored, 3 route, 4 start, 5 goal
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for x, y in result.obstacles:
        grid[y][x] = 1
    for x, y in result.explored:
        if grid[y][x] == 0:
            grid[y][x] = 2
    for x, y in result.path:
        grid[y][x] = 3
    sx, sy = result.start
    gx, gy = result.goal
    grid[sy][sx] = 4
    grid[gy][gx] = 5

    cmap = ListedColormap(["#f2f5f9", "#202938", "#f6d365", "#2784d8", "#2ca66f", "#e04f5f"])
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=5, origin="upper")
    ax.set_title(f"{result.algorithm.upper()} navigation — {'SUCCESS' if result.success else 'NO PATH'}")
    ax.set_xlabel("X cell")
    ax.set_ylabel("Y cell")
    ax.set_xticks(range(0, size, max(1, size // 12)))
    ax.set_yticks(range(0, size, max(1, size // 12)))
    ax.set_xticks([x - 0.5 for x in range(1, size)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, size)], minor=True)
    ax.grid(which="minor", color="#d8dee8", linewidth=0.35)
    ax.tick_params(which="minor", bottom=False, left=False)
    fig.tight_layout()
    return fig

def save_map_figure(result, path):
    fig = render_map_figure(result)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
