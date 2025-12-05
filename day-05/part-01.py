from pathlib import Path


def solve(input: str) -> int:
    ranges, ids = input.split("\n\n")
    ids = set(ids.split("\n"))
    count = 0
    for range in ranges.split("\n"):
        start, end = range.split("-")
        ids_to_remove = set()
        for id in ids:
            if int(start) <= int(id) <= int(end):
                ids_to_remove.add(id)
                count += 1

        ids.difference_update(ids_to_remove)

    return count


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 3
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
