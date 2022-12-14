"""
2022 Day 14
https://adventofcode.com/2022/day/14
"""

from functools import reduce
from itertools import pairwise, takewhile
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
    for start, finish in pairwise(points_of_interest(text)):
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


DROP_DIRECTIONS = (
    complex(1, 0),
    complex(1, -1),
    complex(1, 1),
)


def drop_sand(rocks: set[complex], resting_sand: set[complex]) -> complex:
    """
    Drop a single unit of sand into the given set of occupied locations (starting from y=0, x=500)
    and return the location where it comes to rest as complex (y, x).

    An infinite-length floor is present two y coordinates below the highest y value present in the
    rock structure and will also block the falling of sand.
    """
    floor_y = max(pt.real for pt in rocks) + 2
    occupied = rocks | resting_sand

    prev = complex(-1, 500)
    sand = complex(0, 500)

    while sand != prev:
        prev = sand
        for direction in DROP_DIRECTIONS:
            attempt = sand + direction
            if (attempt not in occupied) and (attempt.real < floor_y):
                sand = attempt
                break

    return sand


def sandfill(rocks: set[complex]) -> Iterator[complex]:
    """
    Fill the given rock structure with sand until all new sand is flowing off into infinite space,
    yielding each space at which sand comes to rest.
    """
    resting_sand: set[complex] = set()
    while complex(0, 500) not in resting_sand:
        yield (sand := drop_sand(rocks, resting_sand))
        resting_sand.add(sand)


def sand_needed_to_fill(rocks: set[complex]) -> tuple[int, int]:
    """
    Return the amount of sand needed to fill the given rock structures with and without an
    infinite-length floor present two y values below the structure.
    """
    no_floor = with_floor = 0
    hit_infinite = False
    floor_y = max(pt.real for pt in rocks) + 1

    for sand in sandfill(rocks):
        if not (hit_infinite := (hit_infinite or sand.real == floor_y)):
            no_floor += 1
        with_floor += 1

    return no_floor, with_floor


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
    assert drop_sand(rocks, set()) == complex(8, 500)
    assert drop_sand(rocks, {complex(8, 500)}) == complex(8, 499)
    assert drop_sand(rocks, {complex(8, 500), complex(8, 499)}) == complex(8, 501)
    assert tuple(takewhile(lambda pt: pt.real < 10, sandfill(rocks))) == (
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


def test_part2() -> None:
    """
    Examples for Part 2.
    """
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
    assert drop_sand(rocks, sand) == complex(10, 493)
    assert drop_sand(rocks, sand | {complex(10, 493)}) == complex(10, 492)

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
        complex(10, 493),
        complex(10, 492),
        complex(10, 494),
        complex(9, 493),
        complex(8, 494),
        complex(8, 496),
        complex(7, 495),
        complex(10, 491),
        complex(9, 492),
        complex(8, 493),
        complex(7, 494),
        complex(7, 496),
        complex(6, 495),
        complex(5, 496),
        complex(4, 497),
        complex(3, 498),
        complex(2, 499),
        complex(3, 502),
        complex(2, 501),
        complex(1, 500),
        complex(10, 490),
        complex(9, 491),
        complex(8, 492),
        complex(7, 493),
        complex(6, 494),
        complex(5, 495),
        complex(4, 496),
        complex(3, 497),
        complex(2, 498),
        complex(1, 499),
        complex(10, 504),
        complex(10, 503),
        complex(10, 505),
        complex(9, 504),
        complex(10, 502),
        complex(9, 503),
        complex(10, 506),
        complex(9, 505),
        complex(8, 504),
        complex(8, 503),
        complex(10, 507),
        complex(9, 506),
        complex(8, 505),
        complex(7, 504),
        complex(7, 503),
        complex(10, 508),
        complex(9, 507),
        complex(8, 506),
        complex(7, 505),
        complex(6, 504),
        complex(6, 503),
        complex(10, 509),
        complex(9, 508),
        complex(8, 507),
        complex(7, 506),
        complex(6, 505),
        complex(5, 504),
        complex(5, 503),
        complex(10, 510),
        complex(9, 509),
        complex(8, 508),
        complex(7, 507),
        complex(6, 506),
        complex(5, 505),
        complex(4, 504),
        complex(3, 503),
        complex(2, 502),
        complex(1, 501),
        complex(0, 500),
    )
    assert sand_needed_to_fill(rocks) == (24, 93)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=14)
    rock = read_rocks(data)
    part_one, part_two = sand_needed_to_fill(rock)
    print(f"Part 1: {part_one}")
    print(f"Part 2: {part_two}")


if __name__ == "__main__":
    main()
