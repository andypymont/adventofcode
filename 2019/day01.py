"""
2019 Day 1
https://adventofcode.com/2019/day/1
"""

import aocd  # type: ignore


def fuel_required(mass: int, recursive: bool = False) -> int:
    fuel = max(mass // 3 - 2, 0)
    if recursive and fuel > 0:
        return fuel + fuel_required(fuel, True)
    return fuel


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert fuel_required(12) == 2
    assert fuel_required(14) == 2
    assert fuel_required(1969) == 654
    assert fuel_required(100756) == 33583


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert fuel_required(14, True) == 2
    assert fuel_required(1969, True) == 966
    assert fuel_required(100756, True) == 50346


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=1)
    masses = [int(line) for line in data.split("\n")]

    print(f"Part 1: {sum(fuel_required(mass) for mass in masses)}")
    print(f"Part 2: {sum(fuel_required(mass, True) for mass in masses)}")


if __name__ == "__main__":
    main()
