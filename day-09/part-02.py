from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class VerticalEdge:
    """A vertical edge of the polygon (constant x)."""

    x: int
    y_min: int
    y_max: int


@dataclass
class HorizontalEdge:
    """A horizontal edge of the polygon (constant y)."""

    y: int
    x_min: int
    x_max: int


class Polygon:
    """A polygon defined by its corner points, with ray casting for inside checks."""

    def __init__(self, corners: list[Point]) -> None:
        self.corners = corners
        self.vertical_edges: list[VerticalEdge] = []
        self.horizontal_edges: list[HorizontalEdge] = []
        self._build_edges()

    def _build_edges(self) -> None:
        """Build edge lists from consecutive corner pairs."""
        for i in range(len(self.corners)):
            p1 = self.corners[i]
            p2 = self.corners[(i + 1) % len(self.corners)]

            if p1.x == p2.x:
                y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)
                self.vertical_edges.append(VerticalEdge(p1.x, y_min, y_max))
            else:
                x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
                self.horizontal_edges.append(HorizontalEdge(p1.y, x_min, x_max))

    def is_point_inside(self, px: float, py: float) -> bool:
        """Check if point is inside using ray casting.

        Cast a horizontal ray to the right from (px, py).
        Count intersections with vertical edges.
        Odd count = inside, even count = outside.
        """
        intersections = 0

        for edge in self.vertical_edges:
            # Edge must be to the right of the point
            if edge.x <= px:
                continue

            # Ray's y must intersect the edge's y range
            # Use min <= py < max to avoid double-counting vertices
            if edge.y_min <= py < edge.y_max:
                intersections += 1

        return intersections % 2 == 1

    def edge_crosses_rectangle_interior(
        self, x_min: int, y_min: int, x_max: int, y_max: int
    ) -> bool:
        """Check if any polygon edge passes through the rectangle's interior."""
        for edge in self.vertical_edges:
            # Edge x must be strictly inside rectangle
            if not (x_min < edge.x < x_max):
                continue

            # Check if edge y-range overlaps with rectangle y-range
            if edge.y_min < y_max and edge.y_max > y_min:
                return True

        for edge in self.horizontal_edges:
            # Edge y must be strictly inside rectangle
            if not (y_min < edge.y < y_max):
                continue

            # Check if edge x-range overlaps with rectangle x-range
            if edge.x_min < x_max and edge.x_max > x_min:
                return True

        return False


def solve(input: str) -> int:
    corners = parse_points(input)
    polygon = Polygon(corners)

    max_area = 0

    for p1, p2 in combinations(corners, 2):
        area = (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)

        # Skip if this rectangle can't beat the current best
        if area <= max_area:
            continue

        if rectangle_inside_polygon(p1, p2, polygon):
            max_area = area

    return max_area


def parse_points(input: str) -> list[Point]:
    points = []
    for line in input.split("\n"):
        x, y = line.split(",")
        points.append(Point(int(x), int(y)))
    return points


def rectangle_inside_polygon(p1: Point, p2: Point, polygon: Polygon) -> bool:
    """Check if rectangle with corners p1 and p2 is entirely inside the polygon."""
    x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
    y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)

    # Test a point slightly inside the rectangle (avoids boundary ambiguity)
    test_x = x_min + 0.5
    test_y = y_min + 0.5

    if not polygon.is_point_inside(test_x, test_y):
        return False

    # Make sure no polygon edge cuts through the rectangle
    if polygon.edge_crosses_rectangle_interior(x_min, y_min, x_max, y_max):
        return False

    return True


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 24
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
