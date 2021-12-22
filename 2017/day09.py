"""
2017 Day 9
https://adventofcode.com/2017/day/9
"""

from typing import Tuple
import aocd  # type: ignore


def parse_stream(stream: str) -> Tuple[int, int]:
    groups = []
    garbage = 0

    in_garbage = False
    cancel = False
    depth = 0

    for char in stream:
        if in_garbage and cancel:
            cancel = False
        elif in_garbage:
            if char == "!":
                cancel = True
            elif char == ">":
                in_garbage = False
            else:
                garbage += 1
        else:
            if char == "<":
                in_garbage = True
            elif char == "{":
                depth += 1
            elif char == "}":
                groups.append(depth)
                depth -= 1

    return sum(groups), garbage


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=9)

    part1, part2 = parse_stream(data)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
