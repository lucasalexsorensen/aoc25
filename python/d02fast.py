import bisect
import sys

with open(f"../{"test-" if "-t" in sys.argv else ""}data/d02.txt", "r") as file:
    ranges = [
        range(int(p.split("-")[0]), int(p.split("-")[1]))
        for p in file.read().strip().split(",")
    ]


sequences = []


def sequences_of_length(n: int) -> list[int]:
    mid = n // 2
    start = 10 ** (mid - 1)
    end = 10**mid
    t = end + 1
    return [t * i for i in range(start, end)]


sequences = [s for i in range(2, 11) for s in sequences_of_length(i)]
sequences = sorted(set(sequences))

result_p1 = 0
invalid_p2 = []
for r in ranges:
    smallest_idx = bisect.bisect_left(sequences, r.start)
    biggest_idx = bisect.bisect_right(sequences, r.stop) - 1
    result_p1 += sum(sequences[smallest_idx : biggest_idx + 1])

print("p1", result_p1)
print("p2", sum(invalid_p2))
