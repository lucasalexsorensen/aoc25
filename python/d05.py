from copy import deepcopy

from utils import file_path

with open(file_path(day=5), "r") as f:
    ranges_part, ingredients_part = f.read().split("\n\n")
    ranges = [
        range(int(line.split("-")[0]), int(line.split("-")[1]) + 1)
        for line in ranges_part.splitlines()
    ]
    ingredients = [int(line) for line in ingredients_part.splitlines()]

print("p1", sum(any(x in r for r in ranges) for x in ingredients))


sorted_ranges = sorted(ranges, key=lambda x: x.start)
merged_ranges = [sorted_ranges[0]]
for r in sorted_ranges[1:]:
    last_range = merged_ranges[-1]
    if last_range.stop >= r.start:
        merged_ranges[-1] = range(last_range.start, max(last_range.stop, r.stop))
    else:
        merged_ranges.append(r)

print("p2", sum(len(r) for r in merged_ranges))
