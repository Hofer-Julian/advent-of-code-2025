from pathlib import Path


def solve(input: str) -> int:
    banks = input.split("\n")
    result = 0
    for bank in banks:
        last_index = -1
        bank_value = 0
        for exponent in range(11, -1, -1):
            for value in range(9, -1, -1):
                index = bank.find(str(value), last_index + 1, len(bank) - exponent)
                if index != -1:
                    bank_value += value * 10**exponent
                    last_index = index
                    break
        result += bank_value
    return result


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 3121910778619
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
