"""
2018 Day 5
https://adventofcode.com/2018/day/5
"""

import string
import aocd  # type: ignore


def single_reaction(polymer: str) -> str:
    for element_no, element in enumerate(string.ascii_lowercase):
        polar = string.ascii_uppercase[element_no]
        for pair in (element + polar, polar + element):
            if pair in polymer:
                return polymer.replace(pair, "")
    return polymer


def fully_react(polymer: str) -> str:
    reacted = single_reaction(polymer)
    while polymer != reacted:
        polymer, reacted = reacted, single_reaction(reacted)
    return reacted


def remove_all(polymer: str, element: str) -> str:
    return polymer.replace(element.lower(), "").replace(element.upper(), "")


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=5)

    print(f"Part 1: {len(fully_react(data))}")
    print(
        f"Part 2: {min(len(fully_react(remove_all(data, l))) for l in string.ascii_lowercase)}"
    )


if __name__ == "__main__":
    main()
