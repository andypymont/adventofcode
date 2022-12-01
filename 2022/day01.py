"""
2022 Day 01
https://adventofcode.com/2022/day/1
"""

from typing import Iterable
import aocd  # type: ignore


def parse_input(text: str) -> Iterable[Iterable[int]]:
    """
    Read the puzzle input and return an iterable of elves, each of which is an iterable of carried
    calorie values.
    """
    return tuple(
        tuple(int(x) for x in section.split("\n")) for section in text.split("\n\n")
    )


def most_calories_carried(elves: Iterable[Iterable[int]], number: int) -> int:
    """
    For a given iterable of elves, return the total calories carried by the specified number of
    elves carrying the most.
    """
    totals = sorted((sum(elf) for elf in elves), reverse=True)
    return sum(totals[:number])


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    elves = (
        (2000, 3000),
        (4000,),
        (5000, 6000),
        (7000, 8000, 9000),
        (10_000,),
    )

    assert (
        parse_input(
            "\n".join(
                (
                    "2000",
                    "3000",
                    "",
                    "4000",
                    "",
                    "5000",
                    "6000",
                    "",
                    "7000",
                    "8000",
                    "9000",
                    "",
                    "10000",
                )
            )
        )
        == elves
    )
    assert most_calories_carried(elves, 1) == 24_000
    assert most_calories_carried(elves[:3], 1) == 11_000


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    elves = (
        (2000, 3000),
        (4000,),
        (5000, 6000),
        (7000, 8000, 9000),
        (10_000,),
    )
    assert most_calories_carried(elves, 3) == 24_000 + 11_000 + 10_000


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=1)
    elves = parse_input(data)

    print(f"Part 1: {most_calories_carried(elves, 1)}")
    print(f"Part 2: {most_calories_carried(elves, 3)}")


if __name__ == "__main__":
    main()
