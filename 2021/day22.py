"""
2021 Day 22
https://adventofcode.com/2021/day/22
"""

from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple
import aocd  # type: ignore


def read_instruction(line: str) -> Tuple[str, int, int, int, int, int, int]:
    parts = line.split(" ")
    instruction = parts[0]
    dimensions = [dim[2:].split("..") for dim in parts[1].split(",")]
    return (
        instruction,
        int(dimensions[0][0]),
        int(dimensions[0][1]),
        int(dimensions[1][0]),
        int(dimensions[1][1]),
        int(dimensions[2][0]),
        int(dimensions[2][1]),
    )


def read_instructions(text: str) -> List[Tuple[str, int, int, int, int, int, int]]:
    return [read_instruction(line) for line in text.split("\n")]


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other: "Point") -> "Point":
        return self.__class__(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )


def cuboid(
    min_x: int, max_x: int, min_y: int, max_y: int, min_z: int, max_z: int
) -> Set[Point]:
    return {
        Point(x, y, z)
        for x in range(max(min_x, -50), min(max_x, 50) + 1)
        for y in range(max(min_y, -50), min(max_y, 50) + 1)
        for z in range(max(min_z, -50), min(max_z, 50) + 1)
    }


def lights_on(instructions: Iterable[Tuple[str, int, int, int, int, int, int]]):
    lit: Set[Point] = set()
    for instruction, *ranges in instructions:
        points = cuboid(*ranges)
        for point in points:
            lit.discard(point) if instruction == "off" else lit.add(point)
    return len(lit)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert cuboid(10, 12, 10, 12, 10, 12) == {
        Point(10, 10, 10),
        Point(10, 10, 11),
        Point(10, 10, 12),
        Point(10, 11, 10),
        Point(10, 11, 11),
        Point(10, 11, 12),
        Point(10, 12, 10),
        Point(10, 12, 11),
        Point(10, 12, 12),
        Point(11, 10, 10),
        Point(11, 10, 11),
        Point(11, 10, 12),
        Point(11, 11, 10),
        Point(11, 11, 11),
        Point(11, 11, 12),
        Point(11, 12, 10),
        Point(11, 12, 11),
        Point(11, 12, 12),
        Point(12, 10, 10),
        Point(12, 10, 11),
        Point(12, 10, 12),
        Point(12, 11, 10),
        Point(12, 11, 11),
        Point(12, 11, 12),
        Point(12, 12, 10),
        Point(12, 12, 11),
        Point(12, 12, 12),
    }
    example1 = [
        ("on", 10, 12, 10, 12, 10, 12),
        ("on", 11, 13, 11, 13, 11, 13),
        ("off", 9, 11, 9, 11, 9, 11),
        ("on", 10, 10, 10, 10, 10, 10),
    ]
    assert (
        read_instructions(
            "\n".join(
                (
                    "on x=10..12,y=10..12,z=10..12",
                    "on x=11..13,y=11..13,z=11..13",
                    "off x=9..11,y=9..11,z=9..11",
                    "on x=10..10,y=10..10,z=10..10",
                )
            )
        )
        == example1
    )
    assert lights_on(example1) == 39
    example2 = [
        ("on", -20, 26, -36, 17, -47, 7),
        ("on", -20, 33, -21, 23, -26, 28),
        ("on", -22, 28, -29, 23, -38, 16),
        ("on", -46, 7, -6, 46, -50, -1),
        ("on", -49, 1, -3, 46, -24, 28),
        ("on", 2, 47, -22, 22, -23, 27),
        ("on", -27, 23, -28, 26, -21, 29),
        ("on", -39, 5, -6, 47, -3, 44),
        ("on", -30, 21, -8, 43, -13, 34),
        ("on", -22, 26, -27, 20, -29, 19),
        ("off", -48, -32, 26, 41, -47, -37),
        ("on", -12, 35, 6, 50, -50, -2),
        ("off", -48, -32, -32, -16, -15, -5),
        ("on", -18, 26, -33, 15, -7, 46),
        ("off", -40, -22, -38, -28, 23, 41),
        ("on", -16, 35, -41, 10, -47, 6),
        ("off", -32, -23, 11, 30, -14, 3),
        ("on", -49, -5, -3, 45, -29, 18),
        ("off", 18, 30, -20, -8, -3, 13),
        ("on", -41, 9, -7, 43, -33, 15),
        ("on", -54112, -39298, -85059, -49293, -27449, 7877),
        ("on", 967, 23432, 45373, 81175, 27513, 53682),
    ]
    assert (
        read_instructions(
            "\n".join(
                (
                    "on x=-20..26,y=-36..17,z=-47..7",
                    "on x=-20..33,y=-21..23,z=-26..28",
                    "on x=-22..28,y=-29..23,z=-38..16",
                    "on x=-46..7,y=-6..46,z=-50..-1",
                    "on x=-49..1,y=-3..46,z=-24..28",
                    "on x=2..47,y=-22..22,z=-23..27",
                    "on x=-27..23,y=-28..26,z=-21..29",
                    "on x=-39..5,y=-6..47,z=-3..44",
                    "on x=-30..21,y=-8..43,z=-13..34",
                    "on x=-22..26,y=-27..20,z=-29..19",
                    "off x=-48..-32,y=26..41,z=-47..-37",
                    "on x=-12..35,y=6..50,z=-50..-2",
                    "off x=-48..-32,y=-32..-16,z=-15..-5",
                    "on x=-18..26,y=-33..15,z=-7..46",
                    "off x=-40..-22,y=-38..-28,z=23..41",
                    "on x=-16..35,y=-41..10,z=-47..6",
                    "off x=-32..-23,y=11..30,z=-14..3",
                    "on x=-49..-5,y=-3..45,z=-29..18",
                    "off x=18..30,y=-20..-8,z=-3..13",
                    "on x=-41..9,y=-7..43,z=-33..15",
                    "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877",
                    "on x=967..23432,y=45373..81175,z=27513..53682",
                )
            )
        )
        == example2
    )
    assert lights_on(example2) == 590784


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=22)
    instructions = read_instructions(data)

    print(f"Part 1: {lights_on(instructions)}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
