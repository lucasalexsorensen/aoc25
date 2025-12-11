from collections import defaultdict, deque
from functools import cache
from itertools import pairwise
from math import prod

from utils import file_path

with open(file_path(day=11), "r") as file:
    connections = {
        from_node[:-1]: to_nodes
        for from_node, *to_nodes in [
            line.strip().split(" ") for line in file.readlines()
        ]
    }


@cache
def dfs(node: str, target: str) -> int:
    if node == target:
        return 1
    return sum(dfs(n, target) for n in connections.get(node, []))


print("p1", dfs("you", "out"))

print(
    "p2",
    sum(
        prod(dfs(s, t) for s, t in pairwise(path))
        for path in [
            ("svr", "fft", "dac", "out"),
            ("svr", "dac", "fft", "out"),
        ]
    ),
)
