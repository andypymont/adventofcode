"""
2022 Day 14
https://adventofcode.com/2022/day/14
"""

from functools import reduce
from itertools import pairwise
from operator import or_
from typing import Iterator
import aocd  # type: ignore


def read_point(point_str: str) -> complex:
    """
    Read a single point from a string 'x,y' into a complex number: complex(y, x).
    """
    parts = [int(part) for part in point_str.split(",")]
    return complex(parts[1], parts[0])


def points_of_interest(text: str) -> tuple[complex, ...]:
    """
    Split a single line of the puzzle input and return the points of interest between which lines of
    rock are drawn.
    """
    return tuple(read_point(point) for point in text.split(" -> "))


def read_rock(text: str) -> set[complex]:
    """
    Read the rock structure from a single line of the puzzle input, returning the set of locations
    occupied by the structure, as complex numbers complex(y, x).
    """
    rock: set[complex] = set()
    poi = points_of_interest(text)
    for start, finish in pairwise(poi):
        delta = complex(
            1 if finish.real > start.real else -1 if finish.real < start.real else 0,
            1 if finish.imag > start.imag else -1 if finish.imag < start.imag else 0,
        )
        point = start
        while point != finish:
            rock.add(point)
            point += delta
        rock.add(finish)

    return rock


def read_rocks(text: str) -> set[complex]:
    """
    Read the rock structures from the puzzle input, returning the set of locations occupied by rock
    from all of the structures (i.e. the union of the sets occupied by each).
    """
    return reduce(or_, (read_rock(line) for line in text.split("\n")))


def drop_sand(occupied: set[complex]) -> complex | None:
    """
    Drop a single unit of sand into the given set of occupied locations (starting from y=0, x=500)
    and return the location where it comes to rest as complex (y, x).

    If the sand drops below the entire rock structure into infinite space, instead return None.
    """
    prev = complex(-1, 500)
    sand = complex(0, 500)
    max_y = max(pt.real for pt in occupied)

    while sand != prev:
        prev = sand
        if (down := sand + complex(1, 0)) not in occupied:
            sand = down
        elif (down_left := sand + complex(1, -1)) not in occupied:
            sand = down_left
        elif (down_right := sand + complex(1, 1)) not in occupied:
            sand = down_right
        if sand.real >= max_y:
            return None

    return sand


def sandfill(rock: set[complex]) -> Iterator[complex]:
    """
    Fill the given rock structure with sand until all new sand is flowing off into infinite space,
    yielding each space at which sand comes to rest.
    """
    resting_sand: set[complex] = set()
    while True:
        if (sand := drop_sand(rock | resting_sand)) is None:
            return
        yield sand
        resting_sand.add(sand)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert points_of_interest("498,4 -> 498,6 -> 496,6") == (
        complex(4, 498),
        complex(6, 498),
        complex(6, 496),
    )
    assert read_rock("498,4 -> 498,6 -> 496,6") == {
        complex(4, 498),
        complex(5, 498),
        complex(6, 498),
        complex(6, 497),
        complex(6, 496),
    }
    assert read_rock("503,4 -> 502,4 -> 502,9 -> 494,9") == {
        complex(4, 503),
        complex(4, 502),
        complex(5, 502),
        complex(6, 502),
        complex(7, 502),
        complex(8, 502),
        complex(9, 502),
        complex(9, 501),
        complex(9, 500),
        complex(9, 499),
        complex(9, 498),
        complex(9, 497),
        complex(9, 496),
        complex(9, 495),
        complex(9, 494),
    }
    rocks = {
        complex(4, 498),
        complex(5, 498),
        complex(6, 498),
        complex(6, 497),
        complex(6, 496),
        complex(4, 503),
        complex(4, 502),
        complex(5, 502),
        complex(6, 502),
        complex(7, 502),
        complex(8, 502),
        complex(9, 502),
        complex(9, 501),
        complex(9, 500),
        complex(9, 499),
        complex(9, 498),
        complex(9, 497),
        complex(9, 496),
        complex(9, 495),
        complex(9, 494),
    }
    assert (
        read_rocks(
            "\n".join(
                (
                    "498,4 -> 498,6 -> 496,6",
                    "503,4 -> 502,4 -> 502,9 -> 494,9",
                )
            )
        )
        == rocks
    )
    assert drop_sand(rocks) == complex(8, 500)
    assert drop_sand(rocks | {complex(8, 500)}) == complex(8, 499)
    assert drop_sand(rocks | {complex(8, 500), complex(8, 499)}) == complex(8, 501)
    sand = {
        complex(8, 500),
        complex(8, 499),
        complex(8, 501),
        complex(7, 500),
        complex(8, 498),
        complex(7, 499),
        complex(7, 501),
        complex(6, 500),
        complex(8, 497),
        complex(7, 498),
        complex(6, 499),
        complex(6, 501),
        complex(5, 500),
        complex(5, 499),
        complex(5, 501),
        complex(4, 500),
        complex(4, 499),
        complex(4, 501),
        complex(3, 500),
        complex(3, 499),
        complex(3, 501),
        complex(2, 500),
        complex(5, 497),
        complex(8, 495),
    }
    assert drop_sand(rocks | sand) is None

    assert tuple(sandfill(rocks)) == (
        complex(8, 500),
        complex(8, 499),
        complex(8, 501),
        complex(7, 500),
        complex(8, 498),
        complex(7, 499),
        complex(7, 501),
        complex(6, 500),
        complex(8, 497),
        complex(7, 498),
        complex(6, 499),
        complex(6, 501),
        complex(5, 500),
        complex(5, 499),
        complex(5, 501),
        complex(4, 500),
        complex(4, 499),
        complex(4, 501),
        complex(3, 500),
        complex(3, 499),
        complex(3, 501),
        complex(2, 500),
        complex(5, 497),
        complex(8, 495),
    )


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=14)
    rock = read_rocks(data)

    print(f"Part 1: {sum(1 for _ in sandfill(rock))}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
