from functools import reduce
from pathlib import Path


def solve(input: str) -> int:
    values = [line.split() for line in input.split("\n")]

    result = 0
    for column in zip(*values):
        column = list(column)
        operation = column.pop()
        numbers = [int(n) for n in column]
        if operation == "*":
            result += reduce(lambda a, b: a * b, numbers)
        elif operation == "+":
            result += reduce(lambda a, b: a + b, numbers)
        else:
            ValueError(f"Invalid {operation=}")

    return result


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 4277556
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
