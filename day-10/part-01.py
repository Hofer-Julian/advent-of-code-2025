from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


@dataclass(frozen=True)
class Machine:
    goal: list[bool]
    buttons: list[list[int]]
    joltage: list[int]

    def parse(line: str) -> Machine:
        segments = line.split(" ")

        goal = []
        for c in segments.pop(0)[1:-1]:
            if c == ".":
                goal.append(False)
            elif c == "#":
                goal.append(True)

        joltage = []
        for value in segments.pop()[1:-1].split(","):
            joltage.append(int(value))

        buttons = []
        for seg in segments:
            button = []
            for value in seg[1:-1].split(","):
                button.append(int(value))
            buttons.append(button)

        return Machine(goal, buttons, joltage)


def solve(input: str) -> int:
    machines = [Machine.parse(row) for row in input.split("\n")]
    print(machines)

    return 0


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 7
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
