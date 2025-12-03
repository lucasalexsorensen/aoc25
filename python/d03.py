import sys

with open(f"../{"test-" if "-t" in sys.argv else ""}data/d03.txt", "r") as file:
    banks = [[int(c) for c in line.strip()] for line in file.readlines()]

result = sum(
    max(
        int(f"{bank[i]}{bank[j]}")
        for i in range(len(bank))
        for j in range(i + 1, len(bank))
    )
    for bank in banks
)
print("p1", result)


def greedy(s: list[int], start_idx: int, n: int) -> int:
    # Find a slice of s such that we can pick one, and still have n-1 left to pick
    # Pick the maximum value in this slice, and denote the index
    # We can now only search FROM THIS INDEX + 1 and forwards
    # Repeat until n is 0
    if n == 0:
        return 0
    elif n == 1:
        seq = s[start_idx:]
    else:
        seq = s[start_idx : -(n - 1)]
    max_idx = start_idx + max(enumerate(seq), key=lambda x: x[1])[0]
    max_val = s[max_idx]
    return max_val * 10 ** (n - 1) + greedy(s, max_idx + 1, n - 1)


print("p2", sum(greedy(bank, 0, 12) for bank in banks))
