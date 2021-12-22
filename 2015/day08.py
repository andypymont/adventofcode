"""
2015 Day 8
https://adventofcode.com/2015/day/8
"""

import json
import regex as re  # type: ignore
import aocd  # type: ignore


def in_memory(string: str) -> str:
    """
    Determine how string would appear in memory by removing opening/closing quotes and resolving
    escaped characters.
    """
    in_mem = string[1:-1].replace("\\\\", "x")
    in_mem = in_mem.replace('\\"', "x")
    in_mem, _ = re.subn("\\\\x..", "x", in_mem)
    return in_mem


def difference(string: str) -> int:
    """
    Calculate the difference in length between the code representation of a string literal and the
    in-memory string itself.
    """
    return len(string) - len(in_memory(string))


def test_part1():
    """
    Examples for Part 1.
    """
    assert difference('""') == 2
    assert difference('"abc"') == 2
    assert difference('"aaa\\"aaa"') == 3


def encoded_difference(string: str) -> int:
    """
    Calculate the difference in length between the given sample and an output string which encodes
    it with appropriate escape characters.
    """
    return len(json.dumps(string)) - len(string)


def test_part2():
    """
    Examples for Part 2.
    """
    assert encoded_difference('""') == 4
    assert encoded_difference('"abc"') == 4


def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=8)
    samples = data.split("\n")

    print(f"Part 1: {sum(difference(sample) for sample in samples)}")
    print(f"Part 2: {sum(encoded_difference(sample) for sample in samples)}")


if __name__ == "__main__":
    main()
