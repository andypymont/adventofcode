"""
2023 Day 24
https://adventofcode.com/2023/day/24
"""

from dataclasses import dataclass
from typing import Iterable
import re
import aocd  # type: ignore
import z3  # type: ignore

Point = tuple[int, int, int]

RE_HAILSTONE = re.compile(
    r"(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)"
)


@dataclass(frozen=True)
class Hailstone:
    """
    A single hailstone, represented by tuples of (x, y, z) for position
    and velocity.
    """

    position: Point
    velocity: Point


def read_hailstone(line: str) -> Hailstone:
    """
    Read a hailstone from a single line.
    """
    match = RE_HAILSTONE.match(line)
    if not match:
        raise ValueError
    posx, posy, posz, velx, vely, velz = [int(g) for g in match.groups()]
    return Hailstone((posx, posy, posz), (velx, vely, velz))


def read_hailstones(data: str) -> Iterable[Hailstone]:
    """
    Read the hailstones.
    """
    return [read_hailstone(line) for line in data.split("\n")]


def launch_point_for_moonshot(hailstones: Iterable[Hailstone]) -> int:
    """
    Calculate the point from which a stonecould be thrown hitting every hailstone.
    """
    solver = z3.Solver()
    pos = z3.RealVector("p", 3)
    vel = z3.RealVector("v", 3)
    time = z3.RealVector("t", 3)

    hail = iter(hailstones)
    for hail_ix in range(3):
        hailstone = next(hail)
        for dim in range(3):
            solver.add(
                pos[dim] + vel[dim] * time[hail_ix]
                == hailstone.position[dim] + hailstone.velocity[dim] * time[hail_ix]
            )

    solver.check()
    return int(solver.model().eval(sum(pos)).as_long())


def main() -> None:
    """
    Calculate and output solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2023, day=24)
    hailstones = read_hailstones(data)

    launch = launch_point_for_moonshot(hailstones)
    print(f"Part 1: {launch}")


if __name__ == "__main__":
    main()
