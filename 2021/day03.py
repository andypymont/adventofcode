"""
2021 Day 3
https://adventofcode.com/2021/day/3
"""

from collections import Counter
from typing import Callable, Iterable
import aocd  # type: ignore


def most_common(values: Iterable[str], position: int) -> str:
    counts = Counter(value[position] for value in values)
    return "1" if counts.get("1", 0) >= counts.get("0", 0) else "0"


def least_common(values: Iterable[str], position: int) -> str:
    return "0" if most_common(values, position) == "1" else "1"


def rate(
    values: Iterable[str], filter_func: Callable[[Iterable[str], int], str]
) -> str:
    length = min(len(value) for value in values)
    return "".join(filter_func(values, pos) for pos in range(length))


def gamma_rate(values: Iterable[str]) -> str:
    return rate(values, most_common)


def epsilon_rate(values: Iterable[str]) -> str:
    return rate(values, least_common)


def best_matching_value(
    binary_numbers: Iterable[str],
    filter_func: Callable[[Iterable[str], int], str],
    position: int = 0,
) -> str:
    filter_value = filter_func(binary_numbers, position)
    filtered = [number for number in binary_numbers if number[position] == filter_value]
    if len(filtered) == 0:
        raise ValueError
    if len(filtered) == 1:
        return filtered[0]
    return best_matching_value(filtered, filter_func, position + 1)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    examples = (
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    )
    assert gamma_rate(examples) == "10110"
    assert epsilon_rate(examples) == "01001"


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    examples = (
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    )
    assert best_matching_value(examples, most_common) == "10111"
    assert best_matching_value(examples, least_common) == "01010"


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=3)
    binary_numbers = data.split("\n")

    gamma = int(gamma_rate(binary_numbers), 2)
    epsilon = int(epsilon_rate(binary_numbers), 2)
    print(f"Part 1: {gamma * epsilon}")

    oxygen = int(best_matching_value(binary_numbers, most_common), 2)
    carbon = int(best_matching_value(binary_numbers, least_common), 2)
    print(f"Part 2: {oxygen * carbon}")


if __name__ == "__main__":
    main()
