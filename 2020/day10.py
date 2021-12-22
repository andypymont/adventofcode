"""
2020 Day 10
https://adventofcode.com/2020/day/10
"""

from collections import deque
from math import prod
from typing import List
import aocd  # type: ignore


def read_adapters(text: str) -> List[int]:
    return [int(adapter) for adapter in text.split("\n")]


def adapter_sections(adapters: List[int]) -> List[List[int]]:
    adapters = sorted(adapters)
    sections = []
    section = [0]
    for index, adapter in enumerate(adapters):
        section.append(adapter)
        if index == len(adapters) - 1 or adapters[index] + 3 == adapters[index + 1]:
            if section:
                sections.append(section)
                section = []
    return sections


def multiply_one_and_three_gaps(sections: List[List[int]]) -> int:
    threes = len(sections)
    ones = sum(len(section) - 1 for section in sections)
    return ones * threes


def routes_through_section(section: List[int]) -> int:
    if len(section) == 1:
        return 1

    routes = 0
    search = deque([section[0:1]])

    while search:
        route = search.popleft()
        position = route[-1]
        if position == max(section):
            routes += 1
        else:
            for other in section:
                if position < other <= (position + 3):
                    search.append(route + [other])

    return routes


def total_routes(sections: List[List[int]]) -> int:
    return prod(routes_through_section(section) for section in sections)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=10)
    adapters = read_adapters(data)
    sections = adapter_sections(adapters)

    print(f"Part 1: {multiply_one_and_three_gaps(sections)}")
    print(f"Part 2: {total_routes(sections)}")


if __name__ == "__main__":
    main()
