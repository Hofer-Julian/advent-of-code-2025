from pathlib import Path


def solve(input: str) -> int:
    ranges = input.split(",")
    result = 0
    for r in ranges:
        lower, upper = r.split("-")
        for number in range(int(lower), int(upper) + 1):
            number_str = str(number)
            length = len(number_str)
            if length % 2 != 0:
                continue

            first = number_str[0 : length // 2]
            second = number_str[length // 2 : length]

            if first == second:
                result += int(number_str)
    return result


example_input = Path("day-02/example.txt").read_text().strip()
result = solve(example_input)
assert result == 1227775554

actual_input = Path("day-02/input.txt").read_text().strip()
result = solve(actual_input)
print(result)
