from pathlib import Path

import numpy as np


def solve(input: str) -> int:
    rows = input.split("\n")
    r_len = len(rows)
    c_len = len(rows[0])
    matrix = np.zeros((r_len, c_len), dtype=int)
    for r, row in enumerate(rows):
        for c, entry in enumerate(row):
            if entry == ".":
                value = 0
            elif entry == "S":
                value = 1
            elif entry == "^":
                value = -1
            else:
                ValueError(entry)
            matrix[r, c] = value

    for r, row in enumerate(matrix):
        for c, entry in enumerate(row):
            if r >= 1 and matrix[r - 1, c] >= 1:
                if entry == -1:
                    if c != 0 and row[c - 1] != -1:
                        row[c - 1] += matrix[r - 1, c]
                    if c != len(row) - 1 and row[c + 1] != -1:
                        row[c + 1] += matrix[r - 1, c]
                else:
                    row[c] += matrix[r - 1, c]

    return matrix[-1, :].sum()


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 40
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
