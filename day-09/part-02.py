from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations, islice
from pathlib import Path

import numpy as np
from alive_progress import alive_it


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def area(a: Point, b: Point) -> int:
    return abs(a.x - b.x + 1) * abs(a.y - b.y + 1)


def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def solve(input: str) -> int:
    rows = input.split("\n")

    points: list[Point] = []
    for row in rows:
        x, y = row.split(",")
        points.append(Point(int(x), int(y)))

    max_len = 0
    for point in points:
        max_len = max(point.x, point.y, max_len)

    floor = np.zeros((max_len + 1, max_len + 1), dtype=np.int8)
    points.append(points[0])
    first_tile = {}
    for point_1, point_2 in sliding_window(points, 2):
        floor[point_1.y, point_1.x] = 1
        if point_1.y not in first_tile or first_tile[point_1.y] > point_1.x:
            first_tile[point_1.y] = point_1.x
        if point_1.x == point_2.x:
            min_y = min(point_1.y, point_2.y)
            max_y = max(point_1.y, point_2.y)
            for y in range(min_y + 1, max_y):
                floor[y, point_1.x] = 2
                if y not in first_tile or first_tile[y] > point_1.x:
                    first_tile[y] = point_1.x
        if point_1.y == point_2.y:
            min_x = min(point_1.x, point_2.x)
            max_x = max(point_1.x, point_2.x)
            for x in range(min_x + 1, max_x):
                floor[point_1.y, x] = 2
                if point_1.y not in first_tile or first_tile[point_1.y] > x:
                    first_tile[point_1.y] = x

    for y, row in enumerate(alive_it(floor)):
        inside = False
        if y not in first_tile:
            continue

        for x in range(first_tile[y], len(row)):
            value = row[x]
            if inside:
                if value == 1 or value == 2:
                    inside = False
                elif value == 0:
                    floor[y, x] = 2
            else:
                if (value == 1 or value == 2) and x + 1 < len(row) and row[x + 1] == 0:
                    inside = True
    perm = combinations(points, 2)
    biggest_areas = sorted(
        perm, key=lambda points: area(points[0], points[1]), reverse=True
    )
    for point_1, point_2 in biggest_areas:
        min_y = min(point_1.y, point_2.y)
        max_y = max(point_1.y, point_2.y)
        min_x = min(point_1.x, point_2.x)
        max_x = max(point_1.x, point_2.x)

        def find_max_area():
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if floor[y, x] not in [1, 2]:
                        return False
            return True

        if find_max_area():
            return area(point_1, point_2)

    raise RuntimeError("Could not find solution")


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 24
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
