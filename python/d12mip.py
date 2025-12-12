from ortools.sat.python import cp_model
from tqdm import tqdm
from utils import file_path

*shapes, regions = file_path(day=12).read_text().split("\n\n")

SHAPES = {
    int(shape.splitlines()[0].split(":")[0]): shape.splitlines()[1:] for shape in shapes
}

type Shape = frozenset[tuple[int, int]]


def parse_shape(shape_lines: list[str]) -> Shape:
    return frozenset(
        {
            (x, y)
            for y, row in enumerate(shape_lines)
            for x, ch in enumerate(row)
            if ch == "#"
        }
    )


def normalize(shape: Shape) -> Shape:
    minx = min(x for x, _ in shape)
    miny = min(y for _, y in shape)
    return frozenset((x - minx, y - miny) for x, y in shape)


def rot90(shape: Shape) -> Shape:
    return frozenset((y, -x) for x, y in shape)


def flip_h(shape: Shape) -> Shape:
    return frozenset((-x, y) for x, y in shape)


def flip_v(shape: Shape) -> Shape:
    return frozenset((x, -y) for x, y in shape)


def all_unique_augmentations(shape: Shape) -> list[Shape]:
    variants = set()
    cur = shape
    for _ in range(4):
        variants.add(normalize(cur))
        variants.add(normalize(flip_h(cur)))
        variants.add(normalize(flip_v(cur)))
        cur = rot90(cur)
    return list(variants)


result = 0
for region in tqdm(regions.splitlines()):
    dims, counts = region.split(": ")
    W, H = map(int, dims.split("x"))
    S = {i: int(count) for i, count in enumerate(counts.split(" "))}

    def cell_index(x, y):
        return y * W + x

    # placements[i] = list of all possible placements for shape i
    placements = {i: [] for i in SHAPES}
    for i, bmp in SHAPES.items():
        base = parse_shape(bmp)
        variants = all_unique_augmentations(base)

        for var in variants:
            var_cells = list(var)
            maxx = max(x for x, _ in var_cells)
            maxy = max(y for _, y in var_cells)
            # anchor (ox, oy) is top-left of the normalized variant footprint
            for ox in range(W - maxx):
                for oy in range(H - maxy):
                    covered = tuple(
                        sorted(cell_index(ox + dx, oy + dy) for dx, dy in var_cells)
                    )
                    placements[i].append(covered)
        # dedup (symmetries can create same covered-set)
        placements[i] = sorted(set(placements[i]))

    total_occupied = sum(S[i] * 9 for i in SHAPES)
    if total_occupied > W * H:
        continue
    model = cp_model.CpModel()

    # Variable:
    # x[i, p] = true if shape i is placed at position p, false otherwise
    x = {}
    for i in SHAPES:
        for p_idx in range(len(placements[i])):
            x[(i, p_idx)] = model.NewBoolVar(f"x_{i}_{p_idx}")

    # Constraint: use each type i exactly S[i] times
    for i in SHAPES:
        model.Add(sum(x[(i, p)] for p in range(len(placements[i]))) == S[i])

    # Constraint: each cell covered by at most 1 chosen placement
    covers = [[] for _ in range(W * H)]
    for i in SHAPES:
        for p_idx, covered in enumerate(placements[i]):
            var = x[(i, p_idx)]
            for c in covered:
                covers[c].append(var)

    # Constraint: each cell is covered by at most 1 shape
    for c in range(W * H):
        model.Add(sum(covers[c]) <= 1)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)
    result += status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
print("p1", result)
