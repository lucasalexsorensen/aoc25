from collections import defaultdict, deque
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


def dfs(node: str, seen: set[str]) -> int:
    if node in seen:
        return 0
    if node == "out":
        return 1
    return sum(dfs(n, seen | {node}) for n in connections[node])


print("p1", dfs("you", set()))


def topo_sort() -> list[str]:
    L = deque([])
    nodes = set(connections.keys())
    marked = set()

    def visit(node: str):
        if node in marked:
            return
        for n in connections.get(node, []):
            visit(n)
        marked.add(node)
        L.appendleft(node)

    while nodes - marked:
        node = (nodes - marked).pop()
        visit(node)

    return list(L)


def count_paths_dag(order, from_node, to_node):
    dp = defaultdict(int)
    dp[from_node] = 1
    for node in order:
        for n in connections.get(node, []):
            dp[n] += dp[node]
    return dp[to_node]


order = topo_sort()

print(
    "p2",
    sum(
        prod(count_paths_dag(order, s, t) for s, t in pairwise(path))
        for path in [
            ("svr", "fft", "dac", "out"),
            ("svr", "dac", "fft", "out"),
        ]
    ),
)
