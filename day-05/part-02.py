from pathlib import Path
from typing import Self


class Range:
    lower: int
    upper: int

    def __init__(self, input: str):
        lower, upper = input.split("-")
        self.lower = int(lower)
        self.upper = int(upper)

    def __repr__(self) -> str:
        return f"{self.lower}-{self.upper}"

    def combine(self, other: Self) -> bool:
        if self.lower <= other.lower <= self.upper <= other.upper:
            self.upper = other.upper
            return True
        if self.lower <= other.lower <= other.upper <= self.upper:
            return True
        if other.lower <= self.lower <= other.upper <= self.upper:
            self.lower = other.lower
            return True
        if other.lower <= self.lower <= self.upper <= other.upper:
            self.lower = other.lower
            self.upper = other.upper
            return True
        return False

    def numbers(self) -> int:
        return self.upper - self.lower + 1


def solve(input: str) -> int:
    ranges = {Range(r) for r in input.split("\n\n")[0].split("\n")}
    final_ranges = set()
    while True:
        if len(ranges) == 0:
            break

        range_to_combine = ranges.pop()
        for range in ranges:
            if range.combine(range_to_combine):
                break
        else:
            final_ranges.add(range_to_combine)

    return sum([range.numbers() for range in final_ranges])


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 14
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
