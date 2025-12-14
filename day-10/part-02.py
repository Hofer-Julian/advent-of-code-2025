from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import Bounds, LinearConstraint, milp


@dataclass(frozen=True)
class Machine:
    buttons: NDArray[np.int32]
    joltage: NDArray[np.int32]

    def parse(line: str) -> Machine:
        segments = line.split(" ")

        segments.pop(0)

        joltage_seg = segments.pop()[1:-1].split(",")
        joltage = np.zeros(len(joltage_seg), dtype=np.int32)
        for i, value in enumerate(joltage_seg):
            joltage[i] = int(value)

        buttons = np.zeros((len(joltage_seg), len(segments)), dtype=np.int32)
        for c, seg in enumerate(segments):
            for value in seg[1:-1].split(","):
                buttons[int(value), c] = 1

        return Machine(buttons, joltage)

    def lowest_button_combination(self) -> int:
        num_buttons = self.buttons.shape[1]

        # Objective: minimize sum(x), i.e., total button presses
        # c @ x = 1*x0 + 1*x1 + ... + 1*xn = sum(x)
        c = np.ones(num_buttons)

        # Constraint: A @ x = b (exact equality)
        # LinearConstraint(A, lb, ub) enforces: lb <= A @ x <= ub
        # For equality, set lb = ub = target
        constraints = LinearConstraint(self.buttons, self.joltage, self.joltage)

        bounds = Bounds(0, np.inf)

        # Integrality: 1 means "must be integer" for each variable
        integrality = np.ones(num_buttons, dtype=int)

        # Solve and return total presses
        result = milp(
            c, constraints=constraints, integrality=integrality, bounds=bounds
        )
        # Result is returned as floats, even with integer constraints.
        # Due to floating point precision, 5 might be 4.99999999.
        # Casting directly to int() would floor it to 4 (wrong).
        return np.round(result.fun).astype(int)


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
