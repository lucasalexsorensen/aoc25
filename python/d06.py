import re
from functools import reduce
from itertools import accumulate, pairwise, starmap, zip_longest
from operator import add, mul
from typing import Callable

from utils import file_path

with open(file_path(day=6), "r") as f:
    lines = f.readlines()
    num_lines, op_line = lines[:-1], lines[-1]
    nums = [[int(num) for num in line.split()] for line in num_lines]
    nums_t = list(map(list, zip(*nums)))
    ops = [add if op == "+" else mul for op in op_line.split()]

print("p1", sum(reduce(op, col) for col, op in zip(nums_t, ops)))


# for part two, we use the last line (i.e. line of operators) to determine the spacing between entries
op_parts = re.findall(r"([+*]\s+)", op_line + " ")
op_part_indices = list(
    pairwise([0] + list(accumulate((len(p) for p in op_parts), add)))
)

nums_padded = [
    [num_line[i : (j - 1)][::-1] for i, j in op_part_indices] for num_line in num_lines
]
nums_padded_t = list(map(list, zip(*nums_padded)))


def compute(col: list[str], op: Callable) -> int:
    return reduce(op, (int("".join(seq)) for seq in zip_longest(*col, fillvalue=" ")))


print(
    "p2",
    sum(starmap(compute, zip(nums_padded_t, ops))),
)
