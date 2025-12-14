from __future__ import annotations

from pathlib import Path

END_NODE = "out"


def count_paths(
    graph: dict[str, list[str]],
    *,
    start: str,
    end: str,
    forbidden: frozenset[str],
    cache: dict[tuple[str, str, frozenset[str]], int],
) -> int:
    """Count all paths from node to end, avoiding forbidden nodes."""

    # graph doesn't need to be cached since it is immutable
    key = (start, end, forbidden)
    if key in cache:
        return cache[key]

    count = 0
    if start in forbidden:
        return 0
    elif start == end:
        return 1
    elif start == END_NODE:
        return 0
    else:
        for output in graph[start]:
            count += count_paths(
                graph, start=output, end=end, forbidden=forbidden, cache=cache
            )

    cache[key] = count
    return count


def solve(input: str) -> int:
    graph: dict[str, list[str]] = {}
    cache: dict[tuple[str, str, frozenset[str]], int] = {}

    for line in input.split("\n"):
        node, others = line.split(": ")
        outputs = others.split(" ")
        graph[node] = outputs

    # Count paths for both orderings of dac and fft
    total = 0

    # Ordering 1: svr -> dac -> fft -> out
    # We forbid fft in the first segment to avoid counting paths where fft comes before dac
    paths_svr_to_dac = count_paths(
        graph, start="svr", end="dac", forbidden=frozenset({"fft"}), cache=cache
    )
    paths_dac_to_fft = count_paths(
        graph, start="dac", end="fft", forbidden=frozenset(), cache=cache
    )
    paths_fft_to_out = count_paths(
        graph, start="fft", end=END_NODE, forbidden=frozenset(), cache=cache
    )
    total += paths_svr_to_dac * paths_dac_to_fft * paths_fft_to_out

    # Ordering 2: svr -> fft -> dac -> out
    # We forbid dac in the first segment to avoid counting paths where dac comes before fft
    paths_svr_to_fft = count_paths(
        graph, start="svr", end="fft", forbidden=frozenset({"dac"}), cache=cache
    )
    paths_fft_to_dac = count_paths(
        graph, start="fft", end="dac", forbidden=frozenset(), cache=cache
    )
    paths_dac_to_out = count_paths(
        graph, start="dac", end=END_NODE, forbidden=frozenset(), cache=cache
    )
    total += paths_svr_to_fft * paths_fft_to_dac * paths_dac_to_out

    return total


example_input = Path(__file__).parent.joinpath("example2.txt").read_text().strip()
result = solve(example_input)
expected_value = 2
assert result == expected_value, f"Value is {result}, but should be {expected_value}"

actual_input = Path(__file__).parent.joinpath("input.txt").read_text().strip()
result = solve(actual_input)
print(result)
