"""
2021 Day 20
https://adventofcode.com/2021/day/20
"""

from dataclasses import dataclass
from typing import List, Set, Tuple
import aocd  # type: ignore

DIRECTIONS: List[complex] = [
    -1 - 1j,
    0 - 1j,
    1 - 1j,
    -1 + 0j,
    0 + 0j,
    1 + 0j,
    -1 + 1j,
    0 + 1j,
    1 + 1j,
]


def square_surrounding(point: complex) -> List[complex]:
    return [point + direction for direction in DIRECTIONS]


def output_pixel(image: Set[complex], point: complex, algorithm: str) -> str:
    return algorithm[
        int("".join("1" if pt in image else "0" for pt in square_surrounding(point)), 2)
    ]


@dataclass
class Image:
    inside_on: Set[complex]
    top_left: complex
    bottom_right: complex
    outside_on: bool

    @classmethod
    def from_text(cls, text: str) -> "Image":
        inside_on: Set[complex] = set()
        point = complex(0, 0)
        for y, line in enumerate(text.split("\n")):
            for x, char in enumerate(line):
                point = complex(x, y)
                if char == "#":
                    inside_on.add(point)
        return cls(inside_on, complex(0, 0), point, False)

    @property
    def limits(self) -> Tuple[int, int, int, int]:
        return (
            int(self.top_left.real),
            int(self.bottom_right.real),
            int(self.top_left.imag),
            int(self.bottom_right.imag),
        )

    @property
    def pixels_lit(self) -> int:
        if self.outside_on:
            raise ValueError("Infinite pixels are turned on!")
        return len(self.inside_on)

    def pixel_on(self, pixel: complex) -> bool:
        if (
            self.top_left.real <= pixel.real <= self.bottom_right.imag
            and self.top_left.imag <= pixel.imag <= self.bottom_right.imag
        ):
            return pixel in self.inside_on
        return self.outside_on

    def output_pixel_on(self, pixel: complex, algorithm: str) -> bool:
        return (
            algorithm[
                int(
                    "".join(
                        "1" if self.pixel_on(pt) else "0"
                        for pt in square_surrounding(pixel)
                    ),
                    2,
                )
            ]
            == "#"
        )

    def enhance_once(self, algorithm: str) -> "Image":
        minx, maxx, miny, maxy = self.limits
        new_pixels = {
            complex(x, y)
            for x in range(minx - 1, maxx + 2)
            for y in range(miny - 1, maxy + 2)
            if self.output_pixel_on(complex(x, y), algorithm)
        }
        return self.__class__(
            new_pixels,
            self.top_left + complex(-1, -1),
            self.bottom_right + complex(1, 1),
            self.outside_on if algorithm[0] == "." else not self.outside_on,
        )

    def enhance(self, algorithm: str, times: int = 1) -> "Image":
        image = self
        for _ in range(times):
            image = image.enhance_once(algorithm)
        return image


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    initial = Image(
        {
            0 + 0j,
            3 + 0j,
            0 + 1j,
            0 + 2j,
            1 + 2j,
            4 + 2j,
            2 + 3j,
            2 + 4j,
            3 + 4j,
            4 + 4j,
        },
        0 + 0j,
        4 + 4j,
        False,
    )
    assert (
        Image.from_text(
            "\n".join(
                (
                    "#..#.",
                    "#....",
                    "##..#",
                    "..#..",
                    "..###",
                )
            )
        )
        == initial
    )
    algo = "".join(
        (
            "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##",
            "#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###",
            ".######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.",
            ".#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....",
            ".#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..",
            "...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....",
            "..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#",
        )
    )
    once = Image(
        {
            0 - 1j,
            1 - 1j,
            3 - 1j,
            4 - 1j,
            -1 + 0j,
            2 + 0j,
            4 + 0j,
            -1 + 1j,
            0 + 1j,
            2 + 1j,
            5 + 1j,
            -1 + 2j,
            0 + 2j,
            1 + 2j,
            2 + 2j,
            5 + 2j,
            0 + 3j,
            3 + 3j,
            4 + 3j,
            1 + 4j,
            2 + 4j,
            5 + 4j,
            2 + 5j,
            4 + 5j,
        },
        -1 - 1j,
        5 + 5j,
        False,
    )
    twice = Image(
        {
            5 - 2j,
            -1 - 1j,
            2 - 1j,
            4 - 1j,
            -2 + 0j,
            0 + 0j,
            4 + 0j,
            5 + 0j,
            6 + 0j,
            -2 + 1j,
            2 + 1j,
            3 + 1j,
            5 + 1j,
            -2 + 2j,
            4 + 2j,
            6 + 2j,
            -1 + 3j,
            1 + 3j,
            2 + 3j,
            3 + 3j,
            4 + 3j,
            5 + 3j,
            0 + 4j,
            2 + 4j,
            3 + 4j,
            4 + 4j,
            5 + 4j,
            6 + 4j,
            1 + 5j,
            2 + 5j,
            4 + 5j,
            5 + 5j,
            2 + 6j,
            3 + 6j,
            4 + 6j,
        },
        -2 - 2j,
        6 + 6j,
        False,
    )
    assert initial.enhance(algo) == once
    assert once.enhance(algo) == twice
    assert initial.enhance(algo, 2).pixels_lit == 35


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    algo = "".join(
        (
            "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##",
            "#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###",
            ".######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.",
            ".#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....",
            ".#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..",
            "...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....",
            "..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#",
        )
    )
    initial = Image(
        {
            0 + 0j,
            3 + 0j,
            0 + 1j,
            0 + 2j,
            1 + 2j,
            4 + 2j,
            2 + 3j,
            2 + 4j,
            3 + 4j,
            4 + 4j,
        },
        0 + 0j,
        4 + 4j,
        False,
    )
    assert initial.enhance(algo, 50).pixels_lit == 3351


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=20)
    algorithm, raw_image = data.split("\n\n")
    image = Image.from_text(raw_image)

    print(f"Part 1: {image.enhance(algorithm, 2).pixels_lit}")
    print(f"Part 2: {image.enhance(algorithm, 50).pixels_lit}")


if __name__ == "__main__":
    main()
