"""
2018 Day 23
https://adventofcode.com/2018/day/23
"""

from dataclasses import dataclass
from typing import Iterable, Set, Sequence
import aocd  # type: ignore
import regex as re  # type: ignore
import z3  # type: ignore

re_nanobot = re.compile(r"pos=<([-\d]+),([-\d]+),([-\d]+)>, r=(\d+)")


@dataclass(frozen=True, order=True)
class Point:
    x_coord: int
    y_coord: int
    z_coord: int

    def __add__(self, other: "Point") -> "Point":
        return Point(
            self.x_coord + other.x_coord,
            self.y_coord + other.y_coord,
            self.z_coord + other.z_coord,
        )

    def distance_from(self, other: "Point") -> int:
        return sum(
            (
                abs(self.x_coord - other.x_coord),
                abs(self.y_coord - other.y_coord),
                abs(self.z_coord - other.z_coord),
            )
        )


def zabs(value: int) -> z3.If:
    return z3.If(value >= 0, value, -value)


@dataclass(frozen=True, order=True)
class Nanobot:
    radius: int
    location: Point

    @classmethod
    def from_regex_groups(cls, groups: Sequence[str]) -> "Nanobot":
        x_coord, y_coord, z_coord, radius = [int(val) for val in groups]
        return cls(radius, Point(x_coord, y_coord, z_coord))

    def in_range_of(self, location: Point) -> bool:
        return self.location.distance_from(location) <= self.radius

    def z3_in_range_of(self, x_coord: int, y_coord: int, z_coord: int) -> z3.If:
        return z3.If(
            (
                zabs(x_coord - self.location.x_coord)
                + zabs(y_coord - self.location.y_coord)
                + zabs(z_coord - self.location.z_coord)
            )
            <= self.radius,
            1,
            0,
        )

    def number_in_range(self, locations: Iterable[Point]) -> int:
        return sum(1 for nanobot in locations if self.in_range_of(nanobot))


def read_nanobots(text: str) -> Set[Nanobot]:
    return {Nanobot.from_regex_groups(groups) for groups in re_nanobot.findall(text)}


def in_range_of_strongest(nanobots: Iterable[Nanobot]) -> int:
    strongest = max(nanobot for nanobot in nanobots)
    return strongest.number_in_range(nanobot.location for nanobot in nanobots)


def distance_to_point_in_range_of_most_nanobots(nanobots: Iterable[Nanobot]) -> int:
    x_coord = z3.Int("x")
    y_coord = z3.Int("y")
    z_coord = z3.Int("z")

    bots_in_range = {
        z3.Int(f"in_range_{botno}"): bot.z3_in_range_of(x_coord, y_coord, z_coord)
        for botno, bot in enumerate(nanobots)
    }

    opt = z3.Optimize()
    for variable, constraint in bots_in_range.items():
        opt.add(variable == constraint)

    bot_count = z3.Int("bot_count")
    opt.add(bot_count == sum(bots_in_range.keys()))

    dist = z3.Int("dist")
    opt.add(dist == zabs(x_coord) + zabs(y_coord) + zabs(z_coord))

    opt.maximize(bot_count)
    nearest_point = opt.minimize(dist)

    opt.check()

    return opt.lower(nearest_point)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=23)
    nanobots = read_nanobots(data)

    print(f"Part 1: {in_range_of_strongest(nanobots)}")
    print(f"Part 2: {distance_to_point_in_range_of_most_nanobots(nanobots)}")


if __name__ == "__main__":
    main()
