from collections import defaultdict
from copy import deepcopy

from utils import file_path

with open(file_path(day=4), "r") as f:
    grid = defaultdict(str) | {
        complex(r, c): char
        for r, line in enumerate(f.readlines())
        for c, char in enumerate(line.strip())
    }

dirs = {complex(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if (dr, dc) != (0, 0)}


def remove_accessible(grid: defaultdict[complex, str]) -> defaultdict[complex, str]:
    new_grid = deepcopy(grid)
    for pos in list(grid.keys()):
        if grid[pos] != "@":
            continue
        n_adjacent = sum(grid[pos + d] == "@" for d in dirs)
        if n_adjacent < 4:
            new_grid[pos] = "."
    return new_grid


first = True
result = 0
while True:
    n_before = sum(grid[pos] == "." for pos in list(grid.keys()))
    grid = remove_accessible(grid)
    n_after = sum(grid[pos] == "." for pos in list(grid.keys()))
    n_removed = n_after - n_before
    if first:
        print("p1", n_removed)
        first = False
    result += n_removed
    if n_removed == 0:
        break

print("p2", result)
