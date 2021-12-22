"""
2021 Day 1
https://adventofcode.com/2021/day/1
"""

from itertools import tee
from typing import Any, Iterable, Tuple
import aocd  # type: ignore


def pairwise(iterable: Iterable[Any]) -> Iterable[Tuple[Any, Any]]:
    """
    Pairwise (as implemented in itertools in Python 3.10)
    e.g. pairwise('ABCDEFG') --> AB BC CD DE EF FG
    """
    one, two = tee(iterable)
    next(two, None)
    return zip(one, two)


def triwise(iterable: Iterable[Any]) -> Iterable[Tuple[Any, Any, Any]]:
    """
    Three-variable version of pairwise.
    e.g. triwise('ABCDEFG') --> ABC BCD CDE DEF EFG
    """
    one, two, three = tee(iterable, 3)
    next(two, None)
    next(three, None)
    next(three, None)
    return zip(one, two, three)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    items = (199, 200, 208, 210, 200, 207, 240, 269, 260, 263)
    assert sum(1 for first, second in pairwise(items) if second > first) == 7


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    items = (199, 200, 208, 210, 200, 207)
    triples = list(triwise(items))
    assert triples == [
        (199, 200, 208),
        (200, 208, 210),
        (208, 210, 200),
        (210, 200, 207),
    ]


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=1)
    numbers = [int(line) for line in data.split("\n")]

    print(f"Part 1: {sum(1 for first, second in pairwise(numbers) if second > first)}")

    windows = [sum(window) for window in triwise(numbers)]
    print(f"Part 2: {sum(1 for first, second in pairwise(windows) if second > first)}")


if __name__ == "__main__":
    main()
