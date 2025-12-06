from functools import reduce
from pathlib import Path


def solve(input: str) -> int:
    numbers = input.split("\n")
    operations = numbers.pop().split()
    result = 0
    calc_number = 0
    current_numbers = []
    max_len = max([len(number) for number in numbers])
    for i in range(max_len):
        current_number = ""
        for number in numbers:
            if i < len(number):
                current_number += number[i]

        if current_number.strip() == "" or i == (max_len - 1):
            if i == (max_len - 1):
                current_numbers.append(int(current_number))
            if operations[calc_number] == "*":
                intermediate = reduce(lambda a, b: a * b, current_numbers)
            elif operations[calc_number] == "+":
                intermediate = reduce(lambda a, b: a + b, current_numbers)
            else:
                ValueError(f"Invalid {operations[calc_number]=}")
            result += intermediate
            current_numbers.clear()
            calc_number += 1
        else:
            current_numbers.append(int(current_number))
    return result


example_input = Path(__file__).parent.joinpath("example.txt").read_text()
result = solve(example_input)


expected_value = 3263827
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text()
result = solve(actual_input)
print(result)
