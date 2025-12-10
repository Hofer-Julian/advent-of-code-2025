from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def area(a: Point, b: Point) -> int:
    return abs(a.x - b.x + 1) * abs(a.y - b.y + 1)


def solve(input: str) -> int:
    rows = input.split("\n")

    points: list[Point] = []
    for row in rows:
        x, y = row.split(",")
        points.append(Point(int(x), int(y)))

    perm = combinations(points, 2)
    biggest_area = sorted(
        perm, key=lambda points: area(points[0], points[1]), reverse=True
    )[0]
    return area(biggest_area[0], biggest_area[1])


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 50
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
