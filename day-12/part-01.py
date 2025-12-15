from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Shape:
    """A shape represented as a set of (row, col) coordinates relative to origin."""

    cells: frozenset[tuple[int, int]]

    def rotate_90(self) -> Shape:
        """Rotate shape 90 degrees clockwise: (r, c) -> (c, -r)"""
        return Shape(frozenset((c, -r) for r, c in self.cells))

    def flip_horizontal(self) -> Shape:
        """Flip shape horizontally: (r, c) -> (r, -c)"""
        return Shape(frozenset((r, -c) for r, c in self.cells))

    def normalize(self) -> Shape:
        """Translate shape so minimum row and column are both 0."""
        min_r = min(r for r, c in self.cells)
        min_c = min(c for r, c in self.cells)
        return Shape(frozenset((r - min_r, c - min_c) for r, c in self.cells))

    def all_orientations(self) -> list[Shape]:
        """Get all unique orientations (rotations + flips)."""
        result: list[Shape] = []

        current = self
        for _ in range(4):  # 4 rotations
            normalized = current.normalize()
            if normalized not in result:
                result.append(normalized)

            flipped = current.flip_horizontal().normalize()
            if flipped not in result:
                result.append(flipped)

            current = current.rotate_90()

        return result


@dataclass(frozen=True)
class Region:
    """A region with dimensions and required presents."""

    width: int
    height: int
    shape_counts: list[int]  # How many of each shape index needed


def parse_input(input_text: str) -> tuple[list[list[Shape]], list[Region]]:
    """
    Parse the input into shapes and regions.

    Returns:
        - List of shapes, where each shape is a list of all its unique orientations
        - List of regions to check
    """
    sections = input_text.strip().split("\n\n")

    # Find where shapes end and regions begin
    shape_sections: list[str] = []
    region_lines: list[str] = []

    for section in sections:
        lines = section.strip().split("\n")
        first_line = lines[0]
        # Shape sections start with "N:" pattern
        if first_line.rstrip(":").isdigit():
            shape_sections.append(section)
        else:
            # This section contains region definitions
            region_lines.extend(lines)

    # Parse shapes
    all_shapes: list[list[Shape]] = []
    for section in shape_sections:
        lines = section.strip().split("\n")
        # Skip the "N:" header line
        grid_lines = lines[1:]

        cells: set[tuple[int, int]] = set()
        for row, line in enumerate(grid_lines):
            for col, char in enumerate(line):
                if char == "#":
                    cells.add((row, col))

        shape = Shape(frozenset(cells))
        all_shapes.append(shape.all_orientations())

    # Parse regions
    regions: list[Region] = []
    for line in region_lines:
        # Format: "WxH: n0 n1 n2 ..."
        dims_part, counts_part = line.split(":")
        width, height = map(int, dims_part.split("x"))
        shape_counts = list(map(int, counts_part.split()))
        regions.append(Region(width, height, shape_counts))

    return all_shapes, regions


def solve(input: str) -> int:
    shapes, regions = parse_input(input)

    result = 0
    for region in regions:
        if can_fit_presents(shapes, region):
            result += 1

    return result


def find_first_empty_cell(
    occupied_cells: set[tuple[int, int]], region: Region
) -> tuple[int, int] | None:
    """Find the first empty cell scanning top-to-bottom, left-to-right."""
    for r in range(region.height):
        for c in range(region.width):
            if (r, c) not in occupied_cells:
                return (r, c)
    return None


def find_placement(
    presents_to_place: list[list[Shape]],
    occupied_cells: set[tuple[int, int]],
    skipped_cells: set[tuple[int, int]],
    region: Region,
) -> bool:
    number_presents = len(presents_to_place)
    if number_presents == 0:
        return True  # Great success!

    current_present = presents_to_place[0]
    remaining_presents = presents_to_place[1:]

    target = find_first_empty_cell(occupied_cells | skipped_cells, region)
    if target is None:
        # Grid is full but we still have presents to place
        return False

    target_r, target_c = target

    # TODO(human): Handle the case where no shape can cover the target cell.
    #
    # Hint: After trying all orientations and positions, if none worked,
    # we have two possibilities:
    # 1. A shape was placed but recursion failed -> we already backtrack
    # 2. No shape could cover target at all -> this cell must stay empty
    #
    # For case 2: add target to skipped_cells, recurse with SAME presents,
    # then remove from skipped_cells when backtracking.

    for orientation in current_present:
        for dr, dc in orientation.cells:
            r = target_r - dr
            c = target_c - dc

            cells = {(r + dr2, c + dc2) for (dr2, dc2) in orientation.cells}
            if all(
                cell not in occupied_cells
                and cell not in skipped_cells
                and 0 <= cell[0] < region.height
                and 0 <= cell[1] < region.width
                for cell in cells
            ):
                occupied_cells.update(cells)

                if find_placement(remaining_presents, occupied_cells, skipped_cells, region):
                    return True

                occupied_cells.difference_update(cells)

    # No shape placement worked - try skipping this cell (leave it empty)
    skipped_cells.add((target_r, target_c))

    if find_placement(presents_to_place, occupied_cells, skipped_cells, region):
        return True

    skipped_cells.remove((target_r, target_c))

    return False


def can_fit_presents(shapes: list[list[Shape]], region: Region) -> bool:
    """
    Check if all required presents can fit in the region.

    TODO(human): Implement the backtracking algorithm to place presents.

    Hints:
    - Build a list of all presents to place (respecting region.shape_counts)
      e.g., if shape_counts = [0, 0, 0, 0, 2, 0], you need 2 presents of shape index 4
    - Track which grid cells are occupied (a set of (row, col) tuples works well)
    - For each present, try each orientation at each valid position (row, col)
    - A shape at position (r, c) occupies cells: {(r + dr, c + dc) for (dr, dc) in shape.cells}
    - Check bounds: all cells must have 0 <= row < region.height and 0 <= col < region.width
    - Check no overlap: none of the cells are already in the occupied set
    - Recursively try to place remaining presents; backtrack (remove cells) if stuck
    - Optimization: find the first empty cell and only try placements that cover it
    """
    presents_to_place: list[list[Shape]] = []
    for i, count in enumerate(region.shape_counts):
        for _ in range(count):
            presents_to_place.append(shapes[i])

    occupied_cells: set[tuple[int, int]] = set()
    skipped_cells: set[tuple[int, int]] = set()

    return find_placement(presents_to_place, occupied_cells, skipped_cells, region)


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 2
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
