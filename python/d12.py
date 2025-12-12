from utils import file_path

*shapes_chunk, regions_chunk = file_path(day=12).read_text().split("\n\n")

result = 0
for region in regions_chunk.splitlines():
    dims, counts = region.split(": ")
    W, H = map(int, dims.split("x"))
    requirements = map(int, counts.split(" "))
    result += sum(r * 9 for r in requirements) <= W * H

print("p1", result)
