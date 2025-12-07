from enum import StrEnum

from utils import file_path

with open(file_path(day=7), "r") as f:
    lines = f.readlines()
    splitters = [
        int(line.strip().replace(".", "0").replace("^", "1").replace("S", "1"), 2)
        for line in lines[2::2]
    ]
    width = len(lines[0].strip())


beams = splitters[0]
result = 0
for split in splitters:
    hits = beams & split
    result += hits.bit_count()
    beams -= hits
    beams |= (hits >> 1) | (hits << 1)

print("p1", result)

counts = [int(b) for b in f"{splitters[0]:0{width}b}"]
for split in splitters:
    new_counts = counts.copy()
    for i, count in enumerate(counts):
        collision = split & (1 << i)
        if not collision:
            continue
        new_counts[i] = 0
        new_counts[i - 1] += counts[i]
        new_counts[i + 1] += counts[i]
    counts = new_counts
print("p2", sum(counts))
