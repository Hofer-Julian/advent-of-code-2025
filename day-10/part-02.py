from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class Machine:
    buttons: list[NDArray[np.int32]]
    joltage: NDArray[np.int32]

    def parse(line: str) -> Machine:
        segments = line.split(" ")

        segments.pop(0)

        joltage_seg = segments.pop()[1:-1].split(",")
        joltage = np.zeros(len(joltage_seg), dtype=np.int32)
        for i, value in enumerate(joltage_seg):
            joltage[i] = int(value)

        buttons = []
        for seg in segments:
            button = np.zeros(len(joltage_seg), dtype=np.int32)
            for value in seg[1:-1].split(","):
                button[int(value)] = 1
            buttons.append(button)

        return Machine(buttons, joltage)

    def lowest_button_combination(self) -> int:
        i = 1
        while True:
            for buttons in combinations_with_replacement(self.buttons, i):
                joltage_state = np.zeros_like(self.joltage, dtype=np.int32)
                for button in buttons:
                    joltage_state += button
                if np.array_equal(joltage_state, self.joltage):
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
expected_value = 33
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
