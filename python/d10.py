from collections import deque

from ortools.linear_solver import pywraplp
from utils import file_path

type Machine = tuple[int, list[int], list[int]]
solver = pywraplp.Solver.CreateSolver("CP_SAT")


def parse_button(button: str, width: int) -> int:
    idx = {int(p) for p in button[1:-1].split(",")}
    bitstring = "".join("1" if i in idx else "0" for i in range(width))
    return int(bitstring, 2)


def parse_machine(line: str) -> Machine:
    target, *buttons, joltage = line.strip().split(" ")
    width = len(target) - 2
    target = int(target[1:-1].replace(".", "0").replace("#", "1"), 2)
    buttons = [parse_button(b, width) for b in buttons]
    joltage = [int(j) for j in joltage[1:-1].split(",")]
    return target, buttons, joltage


with open(file_path(day=10), "r") as file:
    machines = [parse_machine(line) for line in file.readlines()]


def shortest_path_xor(machine: Machine) -> int:
    target, buttons, _ = machine
    queue = deque([(b, 1) for b in buttons])
    seen = set()
    while queue:
        state, n_moves = queue.popleft()
        if state in seen:
            continue
        seen.add(state)
        if state == target:
            return n_moves
        queue.extend((state ^ b, n_moves + 1) for b in buttons)
    return 0


print("p1", sum(shortest_path_xor(m) for m in machines))


def shortest_path_joltage(machine: Machine) -> int:
    _, buttons, target = machine
    T = len(target)
    # convert from buttons to masks, e.g. (1,3) => [0,1,0,1]
    masks = [[int(c) for c in f"{b:0{T}b}"] for b in buttons]  # shape is (M, T)
    M = len(masks)
    # c_i => number of times we use mask i
    c = {m: solver.IntVar(0, solver.infinity(), f"c_{m}") for m in range(M)}
    # add an equality constraint for each position in the target
    for t in range(T):
        solver.Add(solver.Sum(c[m] * masks[m][t] for m in range(M)) == target[t])
    # objective is to minimize the number of masks used
    solver.Minimize(solver.Sum(c[m] for m in range(M)))
    solver.Solve()
    return int(solver.Objective().Value())


print("p2", sum(shortest_path_joltage(m) for m in machines))
