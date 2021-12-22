"""
2015 Day 1
https://adventofcode.com/2015/day/1
"""

import aocd  # type: ignore


def floor_reached(directions: str) -> int:
    """
    Calculate floor reached:
     ( = up one floor
     ) = down one floor
    """
    return sum(1 if char == "(" else -1 for char in directions)


def test_part1():
    """
    Examples for Part 1.
    """
    assert floor_reached("(())") == 0
    assert floor_reached("()()") == 0
    assert floor_reached("(((") == 3
    assert floor_reached("(()(()(") == 3
    assert floor_reached("))(((((") == 3
    assert floor_reached("())") == -1
    assert floor_reached("))(") == -1
    assert floor_reached(")))") == -3
    assert floor_reached(")())())") == -3


def enters_basement(directions: str) -> int:
    """
    On which instruction number (first instruction is 1) does Santa first enter
    the basement?
    """
    total: int = 0

    for i, direction in enumerate(directions):
        total += 1 if direction == "(" else -1
        if total < 0:
            return i + 1

    return -1


def test_part2():
    """
    Examples for Part 2.
    """
    assert enters_basement(")") == 1
    assert enters_basement("()())") == 5


def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=1)

    print(f"Part 1: {floor_reached(data)}")
    print(f"Part 2: {enters_basement(data)}")


if __name__ == "__main__":
    main()
