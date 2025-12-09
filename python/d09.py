import math
from itertools import combinations

from shapely import Polygon, box
from utils import file_path

with open(file_path(day=9), "r") as f:
    points = [
        (int(line.split(",")[0]), int(line.split(",")[1])) for line in f.readlines()
    ]


def area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return math.prod(abs(a - b) + 1 for a, b in zip(p1, p2))


print("p1", max(int(area(p1, p2)) for p1, p2 in combinations(points, 2)))

polygon = Polygon(points)
print(
    "p2",
    max(
        int(area(p1, p2))
        for p1, p2 in combinations(points, 2)
        if polygon.covers(box(*p1, *p2))
    ),
)
