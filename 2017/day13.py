"""
2017 Day 13
https://adventofcode.com/2017/day/13
"""

from typing import Iterable, Iterator, Sequence
import aocd  # type: ignore
import regex as re  # type: ignore


class Scanner:
    def __init__(self, depth: int, height: int):
        self.depth = depth
        self.height = height

    def __repr__(self) -> str:
        return f"Scanner(depth={self.depth}, height={self.height})"

    @property
    def cycle_size(self) -> int:
        return (self.height - 1) * 2

    @property
    def severity(self) -> int:
        return self.depth * self.height

    def collision(self, launch_time: int) -> bool:
        picosecond = launch_time + self.depth
        return picosecond % self.cycle_size == 0


RE_SCANNER = re.compile(r"(\d+): (\d+)")


def read_scanners(text: str) -> Sequence[Scanner]:
    return tuple(
        Scanner(int(depth), int(height)) for depth, height in RE_SCANNER.findall(text)
    )


def collisions(scanners: Iterable[Scanner], launch_time: int = 0) -> Iterator[int]:
    for scanner in scanners:
        if scanner.collision(launch_time):
            yield scanner.severity


def safe_journey(scanners: Sequence[Scanner], launch_time: int) -> bool:
    for _ in collisions(scanners, launch_time):
        return False
    return True


def find_safe_journey(scanners: Sequence[Scanner]) -> int:
    launch_time = 0
    while not safe_journey(scanners, launch_time):
        launch_time += 1
    return launch_time


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=13)
    scanners = read_scanners(data)

    print(f"Part 1: {sum(collisions(scanners))}")
    print(f"Part 2: {find_safe_journey(scanners)}")


if __name__ == "__main__":
    main()
