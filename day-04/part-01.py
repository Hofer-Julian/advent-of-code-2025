from pathlib import Path

import numpy as np


def solve(input: str) -> int:
    rows = input.split("\n")
    c_len = len(rows)
    r_len = len(rows[0])
    matrix = np.zeros((r_len + 2, c_len + 2))
    for r, row in enumerate(rows):
        for c, entry in enumerate(row):
            if entry == ".":
                value = 0
            elif entry == "@":
                value = 1
            else:
                ValueError(entry)
            matrix[r + 1][c + 1] = int(value)
    positions = []
    for c in range(1, c_len + 1):
        for r in range(1, r_len + 1):
            if matrix[r, c] == 1:
                adjacent = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if i == 0 and j == 0:
                            continue
                        position = (r + i, c + j)
                        if matrix[position] == 1:
                            adjacent += 1
                if adjacent < 4:
                    positions.append((r, c))

    temp_matrix = matrix.copy()
    for position in positions:
        temp_matrix[position] = 8
    return len(positions)


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 13
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
