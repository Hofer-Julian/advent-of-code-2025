from __future__ import annotations

from pathlib import Path
from typing import Generator

END_NODE = "out"


def find_all_paths(
    *,
    graph: dict[str, list[str]],
    current_node: str,
    goal_node: str,
    ignored_nodes: set[str],
    path: list[str] | None = None,
) -> Generator[list[str] | None, None, None]:
    # Initialize path on first call
    if path is None:
        path = []

    # Add current node to the path
    path = path + [current_node]

    if current_node in ignored_nodes:
        yield None
        return
    elif current_node == goal_node:
        yield path
        return
    elif current_node == END_NODE:
        yield None
        return

    for output in graph[current_node]:
        yield from find_all_paths(
            graph=graph,
            current_node=output,
            goal_node=goal_node,
            ignored_nodes=ignored_nodes,
            path=path,
        )


def solve(input: str) -> int:
    graph = {}
    for line in input.split("\n"):
        node, others = line.split(": ")
        outputs = others.split(" ")
        graph[node] = outputs

    for second in ["fft", "dac"]:
        number_paths = 1
        third = "dac" if second == "fft" else "fft"

        ignored_nodes = set()

        # Third segment
        print(f"Find paths from {third} to {END_NODE}")
        paths = find_all_paths(
            graph=graph,
            current_node=third,
            goal_node=END_NODE,
            ignored_nodes=ignored_nodes,
        )
        valid_paths = []
        for p in paths:
            assert p is not None
            valid_paths.append(p)
        for path in valid_paths:
            for node in path[1:-1]:
                ignored_nodes.add(node)
        number = len(valid_paths)
        if number == 0:
            raise ValueError(f"Couldn't find path from {third} to {END_NODE}")
        number_paths *= number

        # Second segment
        print(f"Find paths from {second} to {third}")
        paths = find_all_paths(
            graph=graph,
            current_node=second,
            goal_node=third,
            ignored_nodes=ignored_nodes,
        )
        valid_paths = list(filter(lambda p: p is not None, paths))
        for path in valid_paths:
            for node in path[1:-1]:
                ignored_nodes.add(node)
        number = len(valid_paths)
        if number > 0:
            number_paths *= number
        else:
            print(f"No path found from {second} to {third}")
            continue

        # First segment
        paths = find_all_paths(
            graph=graph,
            current_node="svr",
            goal_node=second,
            ignored_nodes=ignored_nodes,
        )
        valid_paths = list(filter(lambda p: p is not None, paths))
        number = len(valid_paths)
        if number == 0:
            raise ValueError(f"Couldn't find path from svr to {second}")
        number_paths *= number

        print(f"Finished path from svr to {second}")

        break

    return number_paths


print("Calculate example")
example_input = Path(__file__).parent.joinpath("example2.txt").read_text().strip()
result = solve(example_input)
expected_value = 2
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

print("\nCalculate input")
actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
