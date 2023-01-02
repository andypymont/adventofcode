"""
2022 Day 3
https://adventofcode.com/2022/day/3
"""

from dataclasses import dataclass
from functools import reduce
from string import ascii_letters
from typing import Iterator, Tuple
import aocd  # type: ignore


@dataclass(frozen=True)
class CommonItemFindingContainer:
    """
    A container which stores chunks of string data, converted into sets, and returns items which
    are common across all of those constituent sets.

    This can be used to model rucksacks (in part 1) and groups of elves (part 2).
    """

    parts: Tuple[frozenset[str], ...]

    @property
    def common_items(self) -> frozenset[str]:
        """
        Reduce the consistent sets to a single set of common items.
        """
        return reduce(lambda a, b: a.intersection(b), self.parts)

    @property
    def first_common_item(self) -> str:
        """
        Return the first common item in all constitutent sets.
        """
        return next(iter(self.common_items))


def rucksack_from_line(line: str) -> CommonItemFindingContainer:
    """
    Parse a single line of the puzzle input and return a CommonItemFindingContainer containing the
    two halves of the line (i.e. the two backpack compartments).
    """
    half = len(line) // 2
    return CommonItemFindingContainer((frozenset(line[:half]), frozenset(line[half:])))


def priority(item: str) -> int:
    """
    Return the priority (int) of the given item type (str).

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.
    """
    return ascii_letters.index(item) + 1


def groups_from_input(input_text: str) -> Iterator[CommonItemFindingContainer]:
    """
    Read the input text, chunk it into groups of three, and yield a CommonItemFindingContainer for
    each group.
    """
    sets = [frozenset(line) for line in input_text.split("\n")]
    for first in range(0, len(sets), 3):
        chunk = tuple(sets[first : first + 3])
        yield CommonItemFindingContainer(chunk)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert rucksack_from_line("vJrwpWtwJgWrhcsFMMfFFhFp").first_common_item == "p"
    assert (
        rucksack_from_line("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL").first_common_item == "L"
    )
    assert rucksack_from_line("PmmdzqPrVvPwwTWBwg").first_common_item == "P"
    assert rucksack_from_line("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn").first_common_item == "v"
    assert rucksack_from_line("ttgJtRGJQctTZtZT").first_common_item == "t"
    assert rucksack_from_line("CrZsJsPPZsGzwwsLwLmpwMDw").first_common_item == "s"
    assert priority("p") == 16
    assert priority("L") == 38
    assert priority("P") == 42
    assert priority("v") == 22
    assert priority("t") == 20
    assert priority("s") == 19


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    test_input = "\n".join(
        (
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw",
        )
    )
    group_one = CommonItemFindingContainer(
        (
            frozenset("vJrwpWtwJgWrhcsFMMfFFhFp"),
            frozenset("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"),
            frozenset("PmmdzqPrVvPwwTWBwg"),
        )
    )
    group_two = CommonItemFindingContainer(
        (
            frozenset("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"),
            frozenset("ttgJtRGJQctTZtZT"),
            frozenset("CrZsJsPPZsGzwwsLwLmpwMDw"),
        )
    )

    input_generator = groups_from_input(test_input)
    assert next(input_generator) == group_one
    assert next(input_generator) == group_two
    assert group_one.first_common_item == "r"
    assert group_two.first_common_item == "Z"


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=3)

    rucksacks = [rucksack_from_line(line) for line in data.split("\n")]
    part_one = sum(priority(rucksack.first_common_item) for rucksack in rucksacks)
    print(f"Part 1: {part_one}")

    part_two = sum(
        priority(group.first_common_item) for group in groups_from_input(data)
    )
    print(f"Part 2: {part_two}")


if __name__ == "__main__":
    main()
