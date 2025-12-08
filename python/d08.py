import math
from itertools import combinations

from utils import file_path

with open(file_path(day=8), "r") as f:
    numbers = [tuple(map(int, line.split(","))) for line in f.readlines()]


clusters = [{i} for i in range(len(numbers))]
for idx, (i, j) in enumerate(
    sorted(
        combinations(range(len(numbers)), 2),
        key=lambda x: math.dist(numbers[x[0]], numbers[x[1]]),
    )
):
    i_cluster = next((c for c in clusters if i in c), None)
    j_cluster = next((c for c in clusters if j in c), None)

    if i_cluster and j_cluster and i_cluster != j_cluster:
        i_cluster.update(j_cluster)
        clusters.remove(j_cluster)
    elif i_cluster:
        i_cluster.add(j)
    elif j_cluster:
        j_cluster.add(i)
    else:
        clusters.append({i, j})

    if idx == 1000:
        cluster_sizes = sorted(len(c) for c in clusters)
        print("p1", math.prod(cluster_sizes[-3:]))

    if len(clusters) == 1:
        print("p2", numbers[i][0] * numbers[j][0])
        break
