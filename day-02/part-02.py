from pathlib import Path


def solve(input: str) -> int:
    ranges = input.split(",")
    result = 0
    for r in ranges:
        lower, upper = r.split("-")
        for number in range(int(lower), int(upper) + 1):
            number_str = str(number)
            if invalid_id := find_invalid_id(number_str):
                result += invalid_id

    return result


def find_invalid_id(number_str: str) -> int | None:
    length = len(number_str)
    for parts in range(2, length + 1):
        if length % parts != 0:
            continue

        pieces = {
            number_str[i : i + length // parts]
            for i in range(0, length, length // parts)
        }

        if len(pieces) == 1:
            return int(number_str)

    return None


example_input = Path("day-02/example.txt").read_text().strip()
result = solve(example_input)
assert result == 4174379265, f"{result=}"

actual_input = Path("day-02/input.txt").read_text().strip()
result = solve(actual_input)
print(result)
