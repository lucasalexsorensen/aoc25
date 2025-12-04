import sys

import numpy as np
from scipy.signal import convolve2d

with open(f"../{"test-" if "-t" in sys.argv else ""}data/d04.txt", "r") as f:
    grid = np.array([[*line.strip()] for line in f.readlines()]) == "@"

kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

diffs = []
while True:
    n_before = np.sum(grid)
    grid &= convolve2d(grid, kernel, mode="same") >= 4
    n_after = np.sum(grid)
    diff = n_before - n_after
    if diff == 0:
        break
    diffs.append(diff)
print("p1", diffs[0])
print("p2", sum(diffs))
