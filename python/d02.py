import re
import sys

with open(f"../{"test-" if "-t" in sys.argv else ""}data/d02.txt", "r") as file:
    ranges = [
        range(int(p.split("-")[0]), int(p.split("-")[1]) + 1)
        for p in file.read().strip().split(",")
    ]

invalid_p1 = []
invalid_p2 = []
pattern_p1 = re.compile(r"^([0-9]+)\1$")
pattern_p2 = re.compile(r"^([0-9]+)\1{1,}$")
for r in ranges:
    for i in r:
        if pattern_p1.match(str(i)):
            invalid_p1.append(i)
        if pattern_p2.match(str(i)):
            invalid_p2.append(i)

print("p1", sum(invalid_p1))
print("p2", sum(invalid_p2))
