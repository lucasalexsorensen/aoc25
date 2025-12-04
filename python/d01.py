from utils import file_path

with open(file_path(day=1), "r") as file:
    lines = [line.strip() for line in file.readlines()]

pos = 50
result = 0
for line in lines:
    dir, steps = line[0], int(line[1:])
    if dir == "L":
        pos -= steps
    else:
        pos += steps
    pos = pos % 100
    if pos == 0:
        result += 1

print("p1", result)

pos = 50
prev_pos = pos
result = 0
for line in lines:
    prev_pos = pos
    dir, steps = line[0], int(line[1:])
    step = -steps if dir == "L" else steps
    fixed_pos = pos if step >= 0 else (100 - pos) % 100
    result += (fixed_pos + abs(step)) // 100

    pos += step
    pos %= 100


print("p2", result)
