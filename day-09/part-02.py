from collections import deque
from pathlib import Path


def solve(input: str) -> int:
    points = parse_points(input)

    xs = sorted({x for x, _ in points})
    ys = sorted({y for _, y in points})

    grid = build_grid(points, xs, ys)
    fill_interior(grid)
    prefix_sums = build_prefix_sum_array(grid)

    max_area = 0
    for i, (x1, y1) in enumerate(points):
        for x2, y2 in points[:i]:
            if is_valid_rectangle(x1, y1, x2, y2, xs, ys, prefix_sums):
                area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
                max_area = max(max_area, area)

    return max_area


def parse_points(input: str) -> list[list[int]]:
    points = []
    for line in input.split("\n"):
        x, y = line.split(",")
        points.append([int(x), int(y)])
    return points


def build_grid(
    points: list[list[int]], xs: list[int], ys: list[int]
) -> list[list[int]]:
    grid = [[0] * (len(ys) * 2 - 1) for _ in range(len(xs) * 2 - 1)]

    polygon_edges = zip(points, points[1:] + points[:1])
    for (x1, y1), (x2, y2) in polygon_edges:
        cx1, cx2 = sorted([xs.index(x1) * 2, xs.index(x2) * 2])
        cy1, cy2 = sorted([ys.index(y1) * 2, ys.index(y2) * 2])
        for cx in range(cx1, cx2 + 1):
            for cy in range(cy1, cy2 + 1):
                grid[cx][cy] = 1

    return grid


def fill_interior(grid: list[list[int]]) -> None:
    outside = find_outside_cells(grid)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (x, y) not in outside:
                grid[x][y] = 1


def find_outside_cells(grid: list[list[int]]) -> set[tuple[int, int]]:
    outside: set[tuple[int, int]] = {(-1, -1)}
    queue: deque[tuple[int, int]] = deque(outside)

    while queue:
        tx, ty = queue.popleft()
        neighbors = [(tx - 1, ty), (tx + 1, ty), (tx, ty - 1), (tx, ty + 1)]

        for nx, ny in neighbors:
            if is_out_of_bounds(nx, ny, grid):
                continue
            if is_wall(nx, ny, grid):
                continue
            if (nx, ny) in outside:
                continue

            outside.add((nx, ny))
            queue.append((nx, ny))

    return outside


def is_out_of_bounds(x: int, y: int, grid: list[list[int]]) -> bool:
    return x < -1 or y < -1 or x > len(grid) or y > len(grid[0])


def is_wall(x: int, y: int, grid: list[list[int]]) -> bool:
    in_grid = 0 <= x < len(grid) and 0 <= y < len(grid[0])
    return in_grid and grid[x][y] == 1


def build_prefix_sum_array(grid: list[list[int]]) -> list[list[int]]:
    prefix_sums = [[0] * len(row) for row in grid]

    for x in range(len(prefix_sums)):
        for y in range(len(prefix_sums[0])):
            left = prefix_sums[x - 1][y] if x > 0 else 0
            top = prefix_sums[x][y - 1] if y > 0 else 0
            topleft = prefix_sums[x - 1][y - 1] if x > 0 and y > 0 else 0
            prefix_sums[x][y] = left + top - topleft + grid[x][y]

    return prefix_sums


def is_valid_rectangle(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    xs: list[int],
    ys: list[int],
    prefix_sums: list[list[int]],
) -> bool:
    cx1, cx2 = sorted([xs.index(x1) * 2, xs.index(x2) * 2])
    cy1, cy2 = sorted([ys.index(y1) * 2, ys.index(y2) * 2])

    filled_cells = query_prefix_sum(prefix_sums, cx1, cy1, cx2, cy2)
    total_cells = (cx2 - cx1 + 1) * (cy2 - cy1 + 1)

    return filled_cells == total_cells


def query_prefix_sum(
    prefix_sums: list[list[int]], x1: int, y1: int, x2: int, y2: int
) -> int:
    total = prefix_sums[x2][y2]
    left = prefix_sums[x1 - 1][y2] if x1 > 0 else 0
    top = prefix_sums[x2][y1 - 1] if y1 > 0 else 0
    topleft = prefix_sums[x1 - 1][y1 - 1] if x1 > 0 and y1 > 0 else 0

    return total - left - top + topleft


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 24
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
