"""
2016 Day 17
https://adventofcode.com/2016/day/17
"""

from dataclasses import dataclass
from collections import deque
from hashlib import md5
from typing import Iterator
import aocd # type: ignore

@dataclass(frozen=True)
class Point():
    """
    A 2-dimensional point within the maze of locations.
    """
    x_coord: int
    y_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x_coord+other.x_coord, self.y_coord+other.y_coord)

    @property
    def within_maze(self) -> bool:
        """
        Return True/False whether this point is within the maze.
        """
        return 0 < self.x_coord <= 4 and 0 < self.y_coord <= 4

@dataclass(frozen=True)
class Journey():
    """
    A journey through the maze of shifting doors.
    """
    passcode: str
    path: str
    location: Point

    def __len__(self) -> int:
        return len(self.path)

    @property
    def md5(self) -> str:
        """
        Calculate the md5 hash for this journey's passcode and the path travelled so far.
        """
        return md5((self.passcode+self.path).encode('utf-8')).hexdigest()

    def all_possible_moves(self) -> 'Iterator[Journey]':
        """
        Generator returning all possible moves from the current location.
        """
        for char, (direction, vector) in zip(self.md5, [
            ('U', Point(x_coord=0, y_coord=-1)),
            ('D', Point(x_coord=0, y_coord=1)),
            ('L', Point(x_coord=-1, y_coord=0)),
            ('R', Point(x_coord=1, y_coord=0)),
        ]):
            neighbour = self.location + vector
            if neighbour.within_maze and (char in 'bcdef'):
                yield Journey(self.passcode, self.path + direction, neighbour)

def find_paths(passcode: str) -> Iterator[str]:
    """
    Find all of the possible paths from (1, 1) to (4, 4), for the given passcode.
    """
    destination = Point(4, 4)
    initial = Journey(passcode, '', Point(1, 1))
    search = deque([initial])

    while search:
        candidate = search.popleft()
        if candidate.location == destination:
            yield candidate.path
        else:
            search.extend(candidate.all_possible_moves())

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=17)
    paths = find_paths(data)

    print(f'Part 1: {next(paths)}')

    *_, path = paths
    print(f'Part 2: {len(path)}')

if __name__ == '__main__':
    main()
