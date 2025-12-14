from __future__ import annotations

from pathlib import Path
from typing import Generator

END_NODE = "out"


def find_all_paths(
    graph: dict[str, list[str]], current_node: str, path: list[str] | None = None
) -> Generator[list[str], None, None]:
    # Initialize path on first call
    if path is None:
        path = []

    # Add current node to the path
    path = path + [current_node]

    # BASE CASE: We reached the destination
    if current_node == END_NODE:
        yield path
        return

    for output in graph[current_node]:
        yield from find_all_paths(graph, output, path)


def solve(input: str) -> int:
    result = 0
    graph = {}
    for line in input.split("\n"):
        node, others = line.split(": ")
        outputs = others.split(" ")
        graph[node] = outputs
    path_generator = find_all_paths(graph, "you")

    # Iterate through the generator
    for p in path_generator:
        result += 1

    return result


example_input = Path(__file__).parent.joinpath("example.txt").read_text().strip()
result = solve(example_input)
expected_value = 5
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
