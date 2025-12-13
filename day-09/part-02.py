from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class PrefixSumArray:
    """2D prefix sum array for efficient rectangular region queries."""

    def __init__(self, grid: list[list[int]]) -> None:
        self._data = [[0] * len(row) for row in grid]

        for x in range(len(self._data)):
            for y in range(len(self._data[0])):
                left = self._data[x - 1][y] if x > 0 else 0
                top = self._data[x][y - 1] if y > 0 else 0
                topleft = self._data[x - 1][y - 1] if x > 0 and y > 0 else 0
                self._data[x][y] = left + top - topleft + grid[x][y]

    def query(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Return the sum of all values in the rectangle from (x1,y1) to (x2,y2)."""
        total = self._data[x2][y2]
        left = self._data[x1 - 1][y2] if x1 > 0 else 0
        top = self._data[x2][y1 - 1] if y1 > 0 else 0
        topleft = self._data[x1 - 1][y1 - 1] if x1 > 0 and y1 > 0 else 0

        return total - left - top + topleft


def solve(input: str) -> int:
    points = parse_points(input)

    # Coordinate compression: map original coordinates to a smaller grid
    # We multiply by 2 to leave space between points for the edges
    unique_xs = sorted({p.x for p in points})
    unique_ys = sorted({p.y for p in points})

    # Build a grid where polygon edges are marked as 1
    grid = build_grid(points, unique_xs, unique_ys)

    # Flood fill from outside to find interior cells, then mark them as 1
    fill_interior(grid)

    # Build prefix sums for efficient rectangle queries
    prefix_sums = PrefixSumArray(grid)

    # Find the largest rectangle where all cells are filled (inside the polygon)
    max_area = 0
    for i, p1 in enumerate(points):
        for p2 in points[:i]:
            if is_valid_rectangle(p1, p2, unique_xs, unique_ys, prefix_sums):
                area = (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)
                max_area = max(max_area, area)

    return max_area


def parse_points(input: str) -> list[Point]:
    points = []
    for line in input.split("\n"):
        x, y = line.split(",")
        points.append(Point(int(x), int(y)))
    return points


def compress_coord(value: int, unique_values: list[int]) -> int:
    """Map an original coordinate to its compressed grid position.

    Multiplied by 2 to leave gaps between points for edge cells.
    """
    return unique_values.index(value) * 2


def build_grid(
    points: list[Point], unique_xs: list[int], unique_ys: list[int]
) -> list[list[int]]:
    """Create a grid with polygon edges marked as 1."""
    grid = [[0] * (len(unique_ys) * 2 - 1) for _ in range(len(unique_xs) * 2 - 1)]

    # Connect consecutive points to form polygon edges
    polygon_edges = zip(points, points[1:] + points[:1])
    for p1, p2 in polygon_edges:
        cx1, cx2 = sorted([compress_coord(p1.x, unique_xs), compress_coord(p2.x, unique_xs)])
        cy1, cy2 = sorted([compress_coord(p1.y, unique_ys), compress_coord(p2.y, unique_ys)])
        for cx in range(cx1, cx2 + 1):
            for cy in range(cy1, cy2 + 1):
                grid[cx][cy] = 1

    return grid


def fill_interior(grid: list[list[int]]) -> None:
    """Mark all cells inside the polygon as 1 using flood fill."""
    outside = find_outside_cells(grid)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (x, y) not in outside:
                grid[x][y] = 1


def find_outside_cells(grid: list[list[int]]) -> set[tuple[int, int]]:
    """BFS flood fill from outside the grid to find all exterior cells."""
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
    """Check if position is too far outside the grid (beyond the 1-cell border)."""
    return x < -1 or y < -1 or x > len(grid) or y > len(grid[0])


def is_wall(x: int, y: int, grid: list[list[int]]) -> bool:
    """Check if position is a wall (polygon edge) that blocks flood fill."""
    in_grid = 0 <= x < len(grid) and 0 <= y < len(grid[0])
    return in_grid and grid[x][y] == 1


def is_valid_rectangle(
    p1: Point,
    p2: Point,
    unique_xs: list[int],
    unique_ys: list[int],
    prefix_sums: PrefixSumArray,
) -> bool:
    """Check if the rectangle between two points is entirely inside the polygon."""
    cx1, cx2 = sorted([compress_coord(p1.x, unique_xs), compress_coord(p2.x, unique_xs)])
    cy1, cy2 = sorted([compress_coord(p1.y, unique_ys), compress_coord(p2.y, unique_ys)])

    filled_cells = prefix_sums.query(cx1, cy1, cx2, cy2)
    total_cells = (cx2 - cx1 + 1) * (cy2 - cy1 + 1)

    # Rectangle is valid if all cells are filled (inside polygon)
    return filled_cells == total_cells


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 24
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
