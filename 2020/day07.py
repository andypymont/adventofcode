"""
2020 Day 7
https://adventofcode.com/2020/day/7
"""

from collections import deque
from typing import Dict, Iterator, Set
import re
import aocd  # type: ignore

re_bag = re.compile(r"([\w ]+) bags contain (.+)\.")
re_contents = re.compile(r"(\d+) ([\w ]+) bag")


def read_rules(text: str) -> Dict[str, Dict[str, int]]:
    return {
        bag: {colour: int(number) for number, colour in re_contents.findall(contents)}
        for bag, contents in re_bag.findall(text)
    }


def bags_that_can_contain(
    rules: Dict[str, Dict[str, int]], colour: str
) -> Iterator[str]:
    for outer, contents in rules.items():
        if colour in contents:
            yield outer


def potential_outermost_bags(rules: Dict[str, Dict[str, int]], colour: str) -> Set[str]:
    visited = set()
    search = deque([colour])
    while search:
        candidate = search.popleft()
        if candidate not in visited:
            visited.add(candidate)
            search.extend(bags_that_can_contain(rules, candidate))

    visited.remove(colour)
    return visited


def total_bags(rules: Dict[str, Dict[str, int]], colour: str) -> int:
    contents = rules.get(colour, {})
    return 1 + sum(
        total_bags(rules, inner) * quantity for (inner, quantity) in contents.items()
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=7)
    rules = read_rules(data)

    part1 = len(potential_outermost_bags(rules, "shiny gold"))
    print(f"Part 1: {part1}")

    part2 = total_bags(rules, "shiny gold") - 1
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
