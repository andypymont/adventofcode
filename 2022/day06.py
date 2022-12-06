"""
2022 Day 6
https://adventofcode.com/2022/day/6
"""

from collections import deque
import aocd  # type: ignore
import pytest


def first_marker(buffer: str, length: int) -> int:
    """
    In the protocol being used by the Elves, the start of a packet is indicated by a sequence of
    four characters that are all different.
    """
    window: deque[str] = deque(maxlen=length)

    for pos, char in enumerate(buffer):
        window.append(char)
        if len(window) == length and len(set(window)) == length:
            return pos + 1

    raise ValueError("No start packet detected")


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert first_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert first_marker("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert first_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert first_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11
    with pytest.raises(ValueError):
        first_marker("aabbaabbcc", 4)


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert first_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert first_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert first_marker("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert first_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert first_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26
    with pytest.raises(ValueError):
        first_marker("hellomyfriendhowareyouthisfineevening", 14)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=6)

    print(f"Part 1: {first_marker(data, 4)}")
    print(f"Part 2: {first_marker(data, 14)}")


if __name__ == "__main__":
    main()
