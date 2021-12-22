"""
2018 Day 11
https://adventofcode.com/2018/day/11
"""

from typing import Dict, Iterator, Tuple, Union
import aocd  # type: ignore


def hundreds(number: int) -> int:
    return int(str(number).zfill(3)[-3])


def power_level(x_coord: int, y_coord: int, grid_serial: int) -> int:
    rack = x_coord + 10
    power = ((rack * y_coord) + grid_serial) * rack
    return hundreds(power) - 5


def grid_power_squares(serial: int) -> Iterator[Tuple[Tuple[int, int, int], int]]:
    # To get through part 2 in particular without running calculations like mad, we need to create
    # this summed area table: we iterate through each potential *bottom corner* for squares and
    # calculate them all at once.
    sat: Dict[Tuple[int, int], int] = {}
    for x_coord in range(1, 301):
        for y_coord in range(1, 301):
            powerlevel = power_level(x_coord, y_coord, serial)
            sat[(x_coord, y_coord)] = sum(
                (
                    powerlevel,
                    sat.get((x_coord, y_coord - 1), 0),
                    sat.get((x_coord - 1, y_coord), 0),
                    -sat.get((x_coord - 1, y_coord - 1), 0),
                )
            )
            for squaresize in range(1, min(x_coord, y_coord)):
                corners = (
                    sat.get((x_coord, y_coord), 0),
                    sat.get((x_coord - squaresize, y_coord - squaresize), 0),
                    -sat.get((x_coord, y_coord - squaresize), 0),
                    -sat.get((x_coord - squaresize, y_coord), 0),
                )
                yield (
                    (x_coord - squaresize + 1, y_coord - squaresize + 1, squaresize),
                    sum(corners),
                )


def best_grid_power_squares(serial: int) -> Dict[Union[int, str], Tuple[int, int, int]]:
    bestsquares: Dict[Union[int, str], Tuple[int, int, int]] = {}
    bestvalues: Dict[Union[int, str], int] = {}
    for ((x_coord, y_coord, squaresize), value) in grid_power_squares(serial):
        if value > bestvalues.get(squaresize, 0):
            bestsquares[squaresize] = (x_coord, y_coord, squaresize)
            bestvalues[squaresize] = value
        if value > bestvalues.get("all", 0):
            bestsquares["all"] = (x_coord, y_coord, squaresize)
            bestvalues["all"] = value
    return bestsquares


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=11)

    serial = int(data)
    bgps = best_grid_power_squares(serial)

    part1 = ",".join(str(x) for x in bgps[3][:2])
    print(f"Part 1: {part1}")

    part2 = ",".join(str(x) for x in bgps["all"])
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
