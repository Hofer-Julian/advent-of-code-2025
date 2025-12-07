from pathlib import Path

import numpy as np

SPLITTER = -1


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
                raise ValueError(entry)
            matrix[r, c] = value

    for r, row in enumerate(matrix):
        for c, entry in enumerate(row):
            value_above = matrix[r - 1, c]
            if r >= 1 and value_above >= 1:
                if entry == SPLITTER:
                    if c != 0 and row[c - 1] != SPLITTER:
                        row[c - 1] += value_above
                    if c != len(row) - 1 and row[c + 1] != SPLITTER:
                        row[c + 1] += value_above
                else:
                    row[c] += value_above

    return matrix[-1, :].sum()


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 40
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
