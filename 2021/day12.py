"""
2021 Day 12
https://adventofcode.com/2021/day/12
"""

from collections import Counter, deque
from typing import Dict, Iterator, Set, Tuple
import aocd  # type: ignore


def read_maze(text: str) -> Dict[str, Set[str]]:
    maze: Dict[str, Set[str]] = {}

    for line in text.split("\n"):
        start, finish = line.split("-")
        if start not in maze:
            maze[start] = set()
        maze[start].add(finish)
        if finish not in maze:
            maze[finish] = set()
        maze[finish].add(start)

    return maze


def valid_routes(
    maze: Dict[str, Set[str]], revisit: bool = False
) -> Iterator[Tuple[str, ...]]:
    start: Tuple[str, ...] = ("start",)
    explore = deque([start])

    while explore:
        route = explore.popleft()
        location = route[-1]
        if location == "end":
            yield route
        else:
            small_visited = Counter(loc for loc in route if loc == loc.lower())
            max_visits = (
                1 if (not revisit) else 2 if max(small_visited.values()) < 2 else 1
            )
            explore.extend(
                route + (neighbour,)
                for neighbour in maze.get(location, set())
                if neighbour != "start" and small_visited.get(neighbour, 0) < max_visits
            )


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    maze1 = {
        "start": {"A", "b"},
        "A": {"b", "c", "end", "start"},
        "b": {"A", "d", "end", "start"},
        "c": {"A"},
        "d": {"b"},
        "end": {"A", "b"},
    }
    assert (
        read_maze(
            "\n".join(("start-A", "start-b", "A-c", "A-b", "b-d", "A-end", "b-end"))
        )
        == maze1
    )
    assert set(valid_routes(maze1)) == {
        ("start", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "end"),
        ("start", "A", "b", "end"),
        ("start", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "end"),
        ("start", "A", "c", "A", "end"),
        ("start", "A", "end"),
        ("start", "b", "A", "c", "A", "end"),
        ("start", "b", "A", "end"),
        ("start", "b", "end"),
    }
    maze2 = {
        "dc": {"end", "HN", "kj", "LN", "start"},
        "end": {"dc", "HN"},
        "HN": {"dc", "end", "kj", "start"},
        "kj": {"dc", "HN", "sa", "start"},
        "LN": {"dc"},
        "sa": {"kj"},
        "start": {"dc", "HN", "kj"},
    }
    assert set(valid_routes(maze2)) == {
        ("start", "HN", "dc", "HN", "end"),
        ("start", "HN", "dc", "HN", "kj", "HN", "end"),
        ("start", "HN", "dc", "end"),
        ("start", "HN", "dc", "kj", "HN", "end"),
        ("start", "HN", "end"),
        ("start", "HN", "kj", "HN", "dc", "HN", "end"),
        ("start", "HN", "kj", "HN", "dc", "end"),
        ("start", "HN", "kj", "HN", "end"),
        ("start", "HN", "kj", "dc", "HN", "end"),
        ("start", "HN", "kj", "dc", "end"),
        ("start", "dc", "HN", "end"),
        ("start", "dc", "HN", "kj", "HN", "end"),
        ("start", "dc", "end"),
        ("start", "dc", "kj", "HN", "end"),
        ("start", "kj", "HN", "dc", "HN", "end"),
        ("start", "kj", "HN", "dc", "end"),
        ("start", "kj", "HN", "end"),
        ("start", "kj", "dc", "HN", "end"),
        ("start", "kj", "dc", "end"),
    }
    maze3 = {
        "DX": {"fs", "he", "pj", "start"},
        "end": {"fs", "zg"},
        "he": {"DX", "fs", "pj", "RW", "WI", "zg"},
        "fs": {"DX", "end", "he", "pj"},
        "pj": {"DX", "fs", "he", "RW", "start", "zg"},
        "RW": {"he", "pj", "start", "zg"},
        "sl": {"zg"},
        "start": {"DX", "pj", "RW"},
        "WI": {"he"},
        "zg": {"end", "he", "pj", "RW", "sl"},
    }
    assert sum(1 for _ in valid_routes(maze3)) == 226


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    maze1 = {
        "start": {"A", "b"},
        "A": {"b", "c", "end", "start"},
        "b": {"A", "d", "end", "start"},
        "c": {"A"},
        "d": {"b"},
        "end": {"A", "b"},
    }
    assert set(valid_routes(maze1, True)) == {
        ("start", "A", "b", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "b", "A", "end"),
        ("start", "A", "b", "A", "b", "end"),
        ("start", "A", "b", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "b", "A", "c", "A", "b", "end"),
        ("start", "A", "b", "A", "c", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "end"),
        ("start", "A", "b", "d", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "d", "b", "A", "end"),
        ("start", "A", "b", "d", "b", "end"),
        ("start", "A", "b", "end"),
        ("start", "A", "c", "A", "b", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "A", "b", "end"),
        ("start", "A", "c", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "d", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "d", "b", "end"),
        ("start", "A", "c", "A", "b", "end"),
        ("start", "A", "c", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "c", "A", "b", "end"),
        ("start", "A", "c", "A", "c", "A", "end"),
        ("start", "A", "c", "A", "end"),
        ("start", "A", "end"),
        ("start", "b", "A", "b", "A", "c", "A", "end"),
        ("start", "b", "A", "b", "A", "end"),
        ("start", "b", "A", "b", "end"),
        ("start", "b", "A", "c", "A", "b", "A", "end"),
        ("start", "b", "A", "c", "A", "b", "end"),
        ("start", "b", "A", "c", "A", "c", "A", "end"),
        ("start", "b", "A", "c", "A", "end"),
        ("start", "b", "A", "end"),
        ("start", "b", "d", "b", "A", "c", "A", "end"),
        ("start", "b", "d", "b", "A", "end"),
        ("start", "b", "d", "b", "end"),
        ("start", "b", "end"),
    }
    maze3 = {
        "DX": {"fs", "he", "pj", "start"},
        "end": {"fs", "zg"},
        "he": {"DX", "fs", "pj", "RW", "WI", "zg"},
        "fs": {"DX", "end", "he", "pj"},
        "pj": {"DX", "fs", "he", "RW", "start", "zg"},
        "RW": {"he", "pj", "start", "zg"},
        "sl": {"zg"},
        "start": {"DX", "pj", "RW"},
        "WI": {"he"},
        "zg": {"end", "he", "pj", "RW", "sl"},
    }
    assert sum(1 for _ in valid_routes(maze3, True)) == 3509


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=12)
    maze = read_maze(data)

    print(f"Part 1: {sum(1 for _ in valid_routes(maze))}")
    print(f"Part 2: {sum(1 for _ in valid_routes(maze, True))}")


if __name__ == "__main__":
    main()
