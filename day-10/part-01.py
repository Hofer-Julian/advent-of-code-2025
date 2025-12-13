from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class Machine:
    goal: NDArray[np.bool_]
    buttons: list[NDArray[np.bool_]]
    joltage: list[int]

    def parse(line: str) -> Machine:
        segments = line.split(" ")

        goal_seg = segments.pop(0)[1:-1]
        goal = np.zeros(len(goal_seg), dtype=bool)
        for i, c in enumerate(goal_seg):
            if c == ".":
                goal[i] = False
            elif c == "#":
                goal[i] = True
            else:
                raise ValueError(c)

        joltage = []
        for value in segments.pop()[1:-1].split(","):
            joltage.append(int(value))

        buttons = []
        for seg in segments:
            button_seg = seg[1:-1].split(",")
            button = np.zeros(len(goal_seg), dtype=bool)
            for value in button_seg:
                button[int(value)] = True
            buttons.append(button)

        return Machine(goal, buttons, joltage)

    def lowest_button_combination(self) -> int:
        i = 1
        while True:
            for buttons in combinations_with_replacement(self.buttons, i):
                button_state = np.zeros_like(self.goal, dtype=bool)
                for button in buttons:
                    button_state ^= button

                if np.array_equal(button_state, self.goal):
                    return len(buttons)
            i += 1


def solve(input: str) -> int:
    machines: list[Machine] = [Machine.parse(row) for row in input.split("\n")]
    result = 0
    for machine in machines:
        result += machine.lowest_button_combination()

    return result


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 7
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
