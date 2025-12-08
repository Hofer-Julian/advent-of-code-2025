from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def distance(self, other: Point) -> float:
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        ) ** (1 / 2)


def solve(input: str) -> int:
    rows = input.split("\n")

    points: list[Point] = []
    for row in rows:
        x, y, z = row.split(",")
        points.append(Point(int(x), int(y), int(z)))

    perm = combinations(points, 2)
    shortest_distances = sorted(perm, key=lambda points: points[0].distance(points[1]))
    circuits: list[set[Point]] = []
    for p1, p2 in shortest_distances:
        circuit1 = None
        circuit2 = None
        for circuit in circuits:
            if p1 in circuit:
                circuit1 = circuit
            if p2 in circuit:
                circuit2 = circuit

        match circuit1, circuit2:
            case None, None:
                circuits.append({p1, p2})
            case c1, None:
                circuits[circuits.index(c1)].add(p2)
            case None, c2:
                circuits[circuits.index(c2)].add(p1)
            case c1, c2:
                if c1 != c2:
                    circuits.remove(c1)
                    circuits.remove(c2)
                    circuits.append(c1.union(c2))
        if len(circuits[0]) == len(points):
            break

    return p1.x * p2.x


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 25272
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
