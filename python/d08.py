import math

from utils import file_path

with open(file_path(day=8), "r") as f:
    numbers = [tuple(map(int, line.split(","))) for line in f.readlines()]


def distance(a: tuple[int, ...], b: tuple[int, ...]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(a, b)))


distances = {
    (i, j): distance(numbers[i], numbers[j])
    for i in range(len(numbers))
    for j in range(i + 1, len(numbers))
    if i != j
}


def cluster(n: int | None = None) -> list[set[int]]:
    clusters = [{i} for i in range(len(numbers))]
    for (i, j), _ in sorted(distances.items(), key=lambda x: x[1])[
        : n or len(distances)
    ]:
        i_cluster = next((cluster for cluster in clusters if i in cluster), None)
        j_cluster = next((cluster for cluster in clusters if j in cluster), None)

        if i_cluster and j_cluster and i_cluster != j_cluster:
            i_cluster.update(j_cluster)
            clusters.remove(j_cluster)
        elif i_cluster:
            i_cluster.add(j)
        elif j_cluster:
            j_cluster.add(i)
        else:
            clusters.append({i, j})

        if len(clusters) == 1:
            print("p2", numbers[i][0] * numbers[j][0])
            break

    return clusters


cluster_sizes = sorted(len(c) for c in cluster(n=1000))
print("p1", math.prod(cluster_sizes[-3:]))
cluster(n=None)
