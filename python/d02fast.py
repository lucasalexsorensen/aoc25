import bisect

from utils import file_path

with open(file_path(day=2), "r") as file:
    ranges = [
        range(int(p.split("-")[0]), int(p.split("-")[1]))
        for p in file.read().strip().split(",")
    ]


def generate_repeated_patterns(seq_len: int, force_twice: bool = False):
    pattern_len_range = [seq_len // 2] if force_twice else range(1, (seq_len // 2) + 1)
    for pattern_len in pattern_len_range:
        if seq_len % pattern_len != 0:
            continue
        # geometric series for repetition masks
        factor = (10**seq_len - 1) // (10**pattern_len - 1)
        start_n = 10 ** (pattern_len - 1)
        stop_n = 10**pattern_len
        for n in range(start_n, stop_n):
            yield n * factor


twice_sequences = [
    s for i in range(2, 11, 2) for s in generate_repeated_patterns(i, force_twice=True)
]
twice_sequences = sorted(set(twice_sequences))


all_sequences = [s for i in range(2, 11) for s in generate_repeated_patterns(i)]
all_sequences = sorted(set(all_sequences))


result_p1 = 0
result_p2 = 0
for r in ranges:
    smallest_idx = bisect.bisect_left(twice_sequences, r.start)
    biggest_idx = bisect.bisect_right(twice_sequences, r.stop) - 1
    result_p1 += sum(twice_sequences[smallest_idx : biggest_idx + 1])

    smallest_idx = bisect.bisect_left(all_sequences, r.start)
    biggest_idx = bisect.bisect_right(all_sequences, r.stop) - 1
    result_p2 += sum(all_sequences[smallest_idx : biggest_idx + 1])

print("p1", result_p1)
print("p2", result_p2)
