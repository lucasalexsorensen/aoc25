from collections import defaultdict, deque
from functools import cache
from itertools import pairwise
from math import prod

from utils import file_path

with open(file_path(day=11), "r") as file:
    connections = {
        from_node.rstrip(":"): to_nodes
        for from_node, *to_nodes in [
            line.strip().split(" ") for line in file.readlines()
        ]
    }


@cache
def n_paths(node: str, target: str) -> int:
    if node == target:
        return 1
    return sum(n_paths(n, target) for n in connections.get(node, []))


print("p1", n_paths("you", "out"))

print(
    "p2",
    sum(
        prod(n_paths(s, t) for s, t in pairwise(steps))
        for steps in [
            ("svr", "fft", "dac", "out"),
            ("svr", "dac", "fft", "out"),
        ]
    ),
)
