from __future__ import annotations

from pathlib import Path
from typing import Generator

END_NODE = "out"


def find_all_paths(
    *,
    graph: dict[str, list[str]],
    current_node: str,
    goal_node: str,
    path: list[str] | None = None,
) -> Generator[list[str] | None, None, None]:
    # Initialize path on first call
    if path is None:
        path = []

    if current_node == goal_node:
        yield path
        return

    # Add current node to the path
    path = path + [current_node]

    if current_node == END_NODE:
        yield None
        return

    for output in graph[current_node]:
        yield from find_all_paths(
            graph=graph, current_node=output, goal_node=goal_node, path=path
        )


def solve(input: str) -> int:
    number_paths = 1
    graph = {}
    for line in input.split("\n"):
        node, others = line.split(": ")
        outputs = others.split(" ")
        graph[node] = outputs

    # Second segment
    for second in ["dac", "fft"]:
        third = "dac" if second == "fft" else "fft"
        paths = find_all_paths(graph=graph, current_node=second, goal_node=third)
        number = len(list(filter(lambda p: p is not None, paths)))
        if number > 0:
            number_paths *= number
            break
    else:
        raise ValueError(f"Couldn't find path from {second} to {third}")

    # First segment
    paths = find_all_paths(graph=graph, current_node="svr", goal_node=second)
    number = len(list(filter(lambda p: p is not None, paths)))
    if number == 0:
        raise ValueError(f"Couldn't find path from svr to {second}")
    number_paths *= number

    # Third segment
    paths = find_all_paths(graph=graph, current_node=third, goal_node=END_NODE)
    number = len(list(filter(lambda p: p is not None, paths)))
    if number == 0:
        raise ValueError(f"Couldn't find path from {third} to {END_NODE}")
    number_paths *= number

    return number_paths


example_input = Path(__file__).parent.joinpath("example2.txt").read_text().strip()
result = solve(example_input)
expected_value = 2
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
