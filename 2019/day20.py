"""
2019 Day 20
https://adventofcode.com/2019/day/20
"""

from collections import deque
from dataclasses import dataclass
from string import ascii_uppercase
from typing import Dict, Iterator, List, Sequence, Set, Tuple
import aocd  # type: ignore


@dataclass(frozen=True)
class Portal:
    """
    A portal between two locations in the maze.
    """

    inner: complex
    outer: complex

    @classmethod
    def from_ends(cls, ends: Sequence[complex], max_x: int, max_y: int) -> "Portal":
        """
        Create a portal with the appropriate ordering of inner/outer ends, based on
        their locations.
        """
        first = ends[0]
        second = ends[1]
        if (
            first.real == 2
            or first.real == (max_x - 2)
            or first.imag == 2
            or first.imag == (max_y - 2)
        ):
            return cls(inner=second, outer=first)
        return cls(inner=first, outer=second)


COMPASS = (
    0 - 1j,
    1 + 0j,
    0 + 1j,
    -1 + 0j,
)


@dataclass
class Maze:
    """
    Representation of the available paths and portals of the maze.
    """

    spaces: Set[complex]
    portals: Set[Portal]
    start: complex
    finish: complex

    @staticmethod
    def labels(lines: Sequence[str], x_coord: int, y_coord: int) -> Iterator[str]:
        """
        Check if the space is labelled in any of the four compass directions and yield
        any such labels.
        """
        north = lines[y_coord - 2][x_coord] + lines[y_coord - 1][x_coord]
        east = lines[y_coord][x_coord + 1] + lines[y_coord][x_coord + 2]
        south = lines[y_coord + 1][x_coord] + lines[y_coord + 2][x_coord]
        west = lines[y_coord][x_coord - 2] + lines[y_coord][x_coord - 1]

        for label in (north, east, south, west):
            if label[0] in ascii_uppercase and label[1] in ascii_uppercase:
                yield label

    @classmethod
    def from_text(cls, text: str) -> "Maze":
        """
        Create a Maze instance from the puzzle input.
        """
        spaces: Set[complex] = set()
        labels: Dict[str, List[complex]] = {}

        lines = text.split("\n")
        max_y = len(lines) - 1
        max_x = len(lines[0]) - 1

        for y_coord, line in enumerate(lines):
            for x_coord, char in enumerate(line):
                if char == ".":
                    pos = complex(x_coord, y_coord)
                    spaces.add(pos)
                    for label in cls.labels(lines, x_coord, y_coord):
                        if label not in labels:
                            labels[label] = []
                        labels[label].append(pos)

        return cls(
            spaces,
            {
                Portal.from_ends(ends, max_x, max_y)
                for ends in labels.values()
                if len(ends) == 2
            },
            labels["AA"][0],
            labels["ZZ"][0],
        )

    def neighbours(self, position: complex) -> Set[complex]:
        """
        Yield the neighbours of the given position, including those accessible via
        portals.
        """
        neighbours = {position + direction for direction in COMPASS}
        inner = {portal.outer for portal in self.portals if portal.inner == position}
        outer = {portal.inner for portal in self.portals if portal.outer == position}

        return (neighbours | outer | inner).intersection(self.spaces)

    def neighbours_recursive(
        self, level: int, position: complex
    ) -> Set[Tuple[int, complex]]:
        """
        Yield the neighbours of the given position, including those accessible via
        portals, in the recursive, nested set of mazes.
        """
        neighbours = {(level, position + direction) for direction in COMPASS}
        inner = {
            (level + 1, portal.outer)
            for portal in self.portals
            if portal.inner == position
        }
        outer = {
            (level - 1, portal.inner)
            for portal in self.portals
            if portal.outer == position and level > 0
        }

        return {
            (level, position)
            for (level, position) in neighbours | outer | inner
            if position in self.spaces
        }

    def shortest_path(self) -> int:
        """
        Calculate the shortest path through the maze.
        """
        consider = deque([(self.start, 0)])
        visited: Set[complex] = set()

        while consider:
            pos, dist = consider.popleft()
            if pos == self.finish:
                return dist
            visited.add(pos)
            for neighbour in self.neighbours(pos):
                if neighbour not in visited:
                    consider.append((neighbour, dist + 1))

        return -1

    def shortest_path_recursive(self) -> int:
        """
        Calculate the shortest path through the recursive, nested set of mazes.
        """
        consider = deque([(0, self.start, 0)])
        visited: Set[Tuple[int, complex]] = set()

        while consider:
            level, pos, dist = consider.popleft()
            if pos == self.finish and level == 0:
                return dist
            visited.add((level, pos))
            for neighbour in self.neighbours_recursive(level, pos):
                if neighbour not in visited:
                    consider.append(neighbour + (dist + 1,))

        return -1


EXAMPLES = (
    Maze(
        spaces={
            9 + 2j,
            9 + 3j,
            10 + 3j,
            11 + 3j,
            12 + 3j,
            13 + 3j,
            14 + 3j,
            15 + 3j,
            16 + 3j,
            17 + 3j,
            9 + 4j,
            17 + 4j,
            9 + 5j,
            17 + 5j,
            9 + 6j,
            17 + 6j,
            17 + 7j,
            2 + 8j,
            3 + 8j,
            4 + 8j,
            17 + 8j,
            4 + 9j,
            17 + 9j,
            4 + 10j,
            5 + 10j,
            6 + 10j,
            17 + 10j,
            17 + 11j,
            11 + 12j,
            17 + 12j,
            2 + 13j,
            3 + 13j,
            11 + 13j,
            12 + 13j,
            13 + 13j,
            17 + 13j,
            3 + 14j,
            13 + 14j,
            17 + 14j,
            2 + 15j,
            3 + 15j,
            13 + 15j,
            14 + 15j,
            15 + 15j,
            16 + 15j,
            17 + 15j,
            13 + 16j,
        },
        portals={
            Portal(inner=9 + 6j, outer=2 + 8j),
            Portal(inner=6 + 10j, outer=2 + 13j),
            Portal(inner=11 + 12j, outer=2 + 15j),
        },
        start=9 + 2j,
        finish=13 + 16j,
    ),
    Maze(
        spaces={
            19 + 2j,
            3 + 3j,
            5 + 3j,
            6 + 3j,
            7 + 3j,
            9 + 3j,
            10 + 3j,
            11 + 3j,
            12 + 3j,
            13 + 3j,
            14 + 3j,
            15 + 3j,
            16 + 3j,
            17 + 3j,
            18 + 3j,
            19 + 3j,
            20 + 3j,
            21 + 3j,
            22 + 3j,
            23 + 3j,
            24 + 3j,
            25 + 3j,
            26 + 3j,
            27 + 3j,
            29 + 3j,
            31 + 3j,
            3 + 4j,
            5 + 4j,
            7 + 4j,
            11 + 4j,
            15 + 4j,
            19 + 4j,
            29 + 4j,
            31 + 4j,
            3 + 5j,
            5 + 5j,
            7 + 5j,
            8 + 5j,
            9 + 5j,
            10 + 5j,
            11 + 5j,
            12 + 5j,
            13 + 5j,
            15 + 5j,
            16 + 5j,
            17 + 5j,
            19 + 5j,
            20 + 5j,
            21 + 5j,
            22 + 5j,
            23 + 5j,
            25 + 5j,
            27 + 5j,
            29 + 5j,
            30 + 5j,
            31 + 5j,
            3 + 6j,
            13 + 6j,
            17 + 6j,
            23 + 6j,
            25 + 6j,
            27 + 6j,
            31 + 6j,
            3 + 7j,
            4 + 7j,
            5 + 7j,
            6 + 7j,
            7 + 7j,
            8 + 7j,
            9 + 7j,
            10 + 7j,
            11 + 7j,
            12 + 7j,
            13 + 7j,
            14 + 7j,
            15 + 7j,
            17 + 7j,
            19 + 7j,
            20 + 7j,
            21 + 7j,
            22 + 7j,
            23 + 7j,
            25 + 7j,
            26 + 7j,
            27 + 7j,
            28 + 7j,
            29 + 7j,
            30 + 7j,
            31 + 7j,
            5 + 8j,
            17 + 8j,
            21 + 8j,
            27 + 8j,
            29 + 8j,
            31 + 8j,
            3 + 9j,
            4 + 9j,
            5 + 9j,
            6 + 9j,
            7 + 9j,
            27 + 9j,
            29 + 9j,
            31 + 9j,
            31 + 10j,
            3 + 11j,
            5 + 11j,
            6 + 11j,
            7 + 11j,
            27 + 11j,
            28 + 11j,
            29 + 11j,
            30 + 11j,
            31 + 11j,
            32 + 11j,
            3 + 12j,
            5 + 12j,
            7 + 12j,
            27 + 12j,
            3 + 13j,
            4 + 13j,
            5 + 13j,
            7 + 13j,
            26 + 13j,
            27 + 13j,
            28 + 13j,
            29 + 13j,
            31 + 13j,
            3 + 14j,
            7 + 14j,
            3 + 14j,
            31 + 14j,
            2 + 15j,
            3 + 15j,
            4 + 15j,
            5 + 15j,
            7 + 15j,
            27 + 15j,
            28 + 15j,
            29 + 15j,
            30 + 15j,
            31 + 15j,
            7 + 16j,
            27 + 16j,
            31 + 16j,
            2 + 17j,
            3 + 17j,
            4 + 17j,
            5 + 17j,
            6 + 17j,
            7 + 17j,
            26 + 17j,
            27 + 17j,
            28 + 17j,
            29 + 17j,
            31 + 17j,
            32 + 17j,
            5 + 18j,
            2 + 19j,
            3 + 19j,
            5 + 19j,
            7 + 19j,
            27 + 19j,
            28 + 19j,
            29 + 19j,
            30 + 19j,
            31 + 19j,
            3 + 20j,
            5 + 20j,
            7 + 20j,
            29 + 20j,
            31 + 20j,
            3 + 21j,
            4 + 21j,
            5 + 21j,
            7 + 21j,
            8 + 21j,
            26 + 21j,
            27 + 21j,
            28 + 21j,
            29 + 21j,
            31 + 21j,
            32 + 21j,
            7 + 22j,
            27 + 22j,
            2 + 23j,
            3 + 23j,
            4 + 23j,
            5 + 23j,
            6 + 23j,
            7 + 23j,
            26 + 23j,
            27 + 23j,
            29 + 23j,
            30 + 23j,
            31 + 23j,
            32 + 23j,
            3 + 24j,
            7 + 24j,
            27 + 24j,
            31 + 24j,
            3 + 25j,
            5 + 25j,
            6 + 25j,
            7 + 25j,
            27 + 25j,
            28 + 25j,
            29 + 25j,
            30 + 25j,
            31 + 25j,
            5 + 26j,
            27 + 26j,
            29 + 26j,
            3 + 27j,
            4 + 27j,
            5 + 27j,
            6 + 27j,
            7 + 27j,
            27 + 27j,
            29 + 27j,
            30 + 27j,
            31 + 27j,
            3 + 28j,
            7 + 28j,
            13 + 28j,
            15 + 28j,
            21 + 28j,
            27 + 28j,
            31 + 28j,
            3 + 29j,
            4 + 29j,
            5 + 29j,
            7 + 29j,
            9 + 29j,
            11 + 29j,
            12 + 29j,
            13 + 29j,
            15 + 29j,
            16 + 29j,
            17 + 29j,
            18 + 29j,
            19 + 29j,
            21 + 29j,
            22 + 29j,
            23 + 29j,
            24 + 29j,
            25 + 29j,
            27 + 29j,
            29 + 29j,
            30 + 29j,
            31 + 29j,
            3 + 30j,
            9 + 30j,
            13 + 30j,
            17 + 30j,
            19 + 30j,
            21 + 30j,
            31 + 30j,
            3 + 31j,
            4 + 31j,
            5 + 31j,
            7 + 31j,
            9 + 31j,
            10 + 31j,
            11 + 31j,
            12 + 31j,
            13 + 31j,
            15 + 31j,
            16 + 31j,
            17 + 31j,
            19 + 31j,
            21 + 31j,
            23 + 31j,
            25 + 31j,
            26 + 31j,
            27 + 31j,
            28 + 31j,
            29 + 31j,
            31 + 31j,
            3 + 32j,
            7 + 32j,
            13 + 32j,
            17 + 32j,
            21 + 32j,
            23 + 32j,
            25 + 32j,
            3 + 33j,
            5 + 33j,
            6 + 33j,
            7 + 33j,
            8 + 33j,
            9 + 33j,
            10 + 33j,
            11 + 33j,
            12 + 33j,
            13 + 33j,
            15 + 33j,
            16 + 33j,
            17 + 33j,
            19 + 33j,
            20 + 33j,
            21 + 33j,
            22 + 33j,
            23 + 33j,
            24 + 33j,
            25 + 33j,
            26 + 33j,
            27 + 33j,
            28 + 33j,
            29 + 33j,
            30 + 33j,
            31 + 33j,
            11 + 34j,
            15 + 34j,
            19 + 34j,
        },
        portals={
            Portal(inner=17 + 8j, outer=32 + 17j),
            Portal(inner=8 + 21j, outer=2 + 15j),
            Portal(inner=26 + 21j, outer=11 + 34j),
            Portal(inner=21 + 8j, outer=19 + 34j),
            Portal(inner=13 + 28j, outer=2 + 19j),
            Portal(inner=21 + 28j, outer=15 + 34j),
            Portal(inner=15 + 28j, outer=32 + 21j),
            Portal(inner=26 + 17j, outer=32 + 23j),
            Portal(inner=26 + 23j, outer=32 + 11j),
            Portal(inner=26 + 13j, outer=2 + 23j),
        },
        start=19 + 2j,
        finish=2 + 17j,
    ),
    Maze(
        spaces={
            (7 + 32j),
            (11 + 32j),
            (17 + 32j),
            (19 + 32j),
            (21 + 32j),
            (23 + 32j),
            (25 + 32j),
            (29 + 32j),
            (33 + 32j),
            (35 + 32j),
            (39 + 32j),
            (2 + 25j),
            (3 + 25j),
            (4 + 25j),
            (5 + 25j),
            (7 + 25j),
            (37 + 25j),
            (38 + 25j),
            (39 + 25j),
            (40 + 25j),
            (41 + 25j),
            (42 + 25j),
            (3 + 18j),
            (7 + 18j),
            (37 + 18j),
            (41 + 18j),
            (3 + 11j),
            (5 + 11j),
            (6 + 11j),
            (7 + 11j),
            (37 + 11j),
            (38 + 11j),
            (39 + 11j),
            (41 + 11j),
            (5 + 4j),
            (7 + 4j),
            (9 + 4j),
            (11 + 4j),
            (13 + 4j),
            (15 + 4j),
            (17 + 4j),
            (19 + 4j),
            (23 + 4j),
            (25 + 4j),
            (27 + 4j),
            (35 + 4j),
            (37 + 4j),
            (39 + 4j),
            (3 + 29j),
            (4 + 29j),
            (5 + 29j),
            (6 + 29j),
            (7 + 29j),
            (9 + 29j),
            (10 + 29j),
            (11 + 29j),
            (13 + 29j),
            (14 + 29j),
            (15 + 29j),
            (16 + 29j),
            (17 + 29j),
            (19 + 29j),
            (20 + 29j),
            (21 + 29j),
            (22 + 29j),
            (23 + 29j),
            (24 + 29j),
            (25 + 29j),
            (27 + 29j),
            (28 + 29j),
            (29 + 29j),
            (31 + 29j),
            (32 + 29j),
            (33 + 29j),
            (34 + 29j),
            (35 + 29j),
            (37 + 29j),
            (39 + 29j),
            (40 + 29j),
            (41 + 29j),
            (7 + 22j),
            (2 + 15j),
            (3 + 15j),
            (4 + 15j),
            (5 + 15j),
            (6 + 15j),
            (7 + 15j),
            (37 + 15j),
            (38 + 15j),
            (39 + 15j),
            (40 + 15j),
            (41 + 15j),
            (3 + 8j),
            (13 + 8j),
            (21 + 8j),
            (23 + 8j),
            (31 + 8j),
            (39 + 8j),
            (3 + 33j),
            (4 + 33j),
            (5 + 33j),
            (6 + 33j),
            (7 + 33j),
            (8 + 33j),
            (9 + 33j),
            (11 + 33j),
            (12 + 33j),
            (13 + 33j),
            (14 + 33j),
            (15 + 33j),
            (17 + 33j),
            (19 + 33j),
            (20 + 33j),
            (21 + 33j),
            (23 + 33j),
            (24 + 33j),
            (25 + 33j),
            (26 + 33j),
            (27 + 33j),
            (28 + 33j),
            (29 + 33j),
            (30 + 33j),
            (31 + 33j),
            (32 + 33j),
            (33 + 33j),
            (34 + 33j),
            (35 + 33j),
            (36 + 33j),
            (37 + 33j),
            (39 + 33j),
            (40 + 33j),
            (41 + 33j),
            (5 + 26j),
            (37 + 26j),
            (39 + 26j),
            (41 + 26j),
            (3 + 19j),
            (4 + 19j),
            (5 + 19j),
            (6 + 19j),
            (7 + 19j),
            (37 + 19j),
            (38 + 19j),
            (39 + 19j),
            (41 + 19j),
            (3 + 12j),
            (7 + 12j),
            (37 + 12j),
            (41 + 12j),
            (3 + 5j),
            (5 + 5j),
            (6 + 5j),
            (7 + 5j),
            (9 + 5j),
            (11 + 5j),
            (13 + 5j),
            (14 + 5j),
            (15 + 5j),
            (17 + 5j),
            (19 + 5j),
            (21 + 5j),
            (22 + 5j),
            (23 + 5j),
            (25 + 5j),
            (26 + 5j),
            (27 + 5j),
            (29 + 5j),
            (30 + 5j),
            (31 + 5j),
            (33 + 5j),
            (35 + 5j),
            (36 + 5j),
            (37 + 5j),
            (38 + 5j),
            (39 + 5j),
            (40 + 5j),
            (41 + 5j),
            (7 + 30j),
            (9 + 30j),
            (13 + 30j),
            (21 + 30j),
            (29 + 30j),
            (33 + 30j),
            (37 + 30j),
            (39 + 30j),
            (41 + 30j),
            (3 + 23j),
            (4 + 23j),
            (5 + 23j),
            (6 + 23j),
            (7 + 23j),
            (8 + 23j),
            (36 + 23j),
            (37 + 23j),
            (39 + 23j),
            (40 + 23j),
            (41 + 23j),
            (3 + 9j),
            (4 + 9j),
            (5 + 9j),
            (7 + 9j),
            (37 + 9j),
            (39 + 9j),
            (41 + 9j),
            (13 + 2j),
            (15 + 2j),
            (17 + 2j),
            (19 + 2j),
            (27 + 2j),
            (15 + 34j),
            (17 + 34j),
            (19 + 34j),
            (23 + 34j),
            (3 + 27j),
            (4 + 27j),
            (5 + 27j),
            (6 + 27j),
            (7 + 27j),
            (37 + 27j),
            (39 + 27j),
            (41 + 27j),
            (5 + 20j),
            (37 + 20j),
            (39 + 20j),
            (41 + 20j),
            (3 + 13j),
            (5 + 13j),
            (6 + 13j),
            (7 + 13j),
            (8 + 13j),
            (36 + 13j),
            (37 + 13j),
            (39 + 13j),
            (41 + 13j),
            (42 + 13j),
            (3 + 6j),
            (7 + 6j),
            (15 + 6j),
            (19 + 6j),
            (23 + 6j),
            (25 + 6j),
            (29 + 6j),
            (33 + 6j),
            (35 + 6j),
            (3 + 31j),
            (4 + 31j),
            (5 + 31j),
            (6 + 31j),
            (7 + 31j),
            (8 + 31j),
            (9 + 31j),
            (11 + 31j),
            (12 + 31j),
            (13 + 31j),
            (14 + 31j),
            (15 + 31j),
            (16 + 31j),
            (17 + 31j),
            (19 + 31j),
            (21 + 31j),
            (23 + 31j),
            (25 + 31j),
            (27 + 31j),
            (28 + 31j),
            (29 + 31j),
            (31 + 31j),
            (32 + 31j),
            (33 + 31j),
            (35 + 31j),
            (36 + 31j),
            (37 + 31j),
            (39 + 31j),
            (41 + 31j),
            (5 + 24j),
            (7 + 24j),
            (37 + 24j),
            (41 + 24j),
            (3 + 17j),
            (5 + 17j),
            (6 + 17j),
            (7 + 17j),
            (8 + 17j),
            (37 + 17j),
            (38 + 17j),
            (39 + 17j),
            (40 + 17j),
            (41 + 17j),
            (42 + 17j),
            (3 + 10j),
            (7 + 10j),
            (37 + 10j),
            (39 + 10j),
            (41 + 10j),
            (3 + 3j),
            (4 + 3j),
            (5 + 3j),
            (7 + 3j),
            (8 + 3j),
            (9 + 3j),
            (10 + 3j),
            (11 + 3j),
            (12 + 3j),
            (13 + 3j),
            (15 + 3j),
            (17 + 3j),
            (18 + 3j),
            (19 + 3j),
            (20 + 3j),
            (21 + 3j),
            (22 + 3j),
            (23 + 3j),
            (25 + 3j),
            (27 + 3j),
            (28 + 3j),
            (29 + 3j),
            (30 + 3j),
            (31 + 3j),
            (32 + 3j),
            (33 + 3j),
            (35 + 3j),
            (37 + 3j),
            (39 + 3j),
            (40 + 3j),
            (41 + 3j),
            (5 + 28j),
            (17 + 28j),
            (21 + 28j),
            (29 + 28j),
            (39 + 28j),
            (2 + 21j),
            (3 + 21j),
            (4 + 21j),
            (5 + 21j),
            (7 + 21j),
            (36 + 21j),
            (37 + 21j),
            (39 + 21j),
            (41 + 21j),
            (3 + 14j),
            (7 + 14j),
            (37 + 14j),
            (39 + 14j),
            (41 + 14j),
            (3 + 7j),
            (4 + 7j),
            (5 + 7j),
            (7 + 7j),
            (8 + 7j),
            (9 + 7j),
            (10 + 7j),
            (11 + 7j),
            (12 + 7j),
            (13 + 7j),
            (15 + 7j),
            (17 + 7j),
            (18 + 7j),
            (19 + 7j),
            (21 + 7j),
            (22 + 7j),
            (23 + 7j),
            (25 + 7j),
            (26 + 7j),
            (27 + 7j),
            (28 + 7j),
            (29 + 7j),
            (30 + 7j),
            (31 + 7j),
            (32 + 7j),
            (33 + 7j),
            (34 + 7j),
            (35 + 7j),
            (36 + 7j),
            (37 + 7j),
            (39 + 7j),
            (40 + 7j),
            (41 + 7j),
        },
        portals={
            Portal(inner=(23 + 8j), outer=(42 + 17j)),
            Portal(inner=(8 + 23j), outer=(2 + 15j)),
            Portal(inner=(36 + 13j), outer=(19 + 2j)),
            Portal(inner=(8 + 17j), outer=(27 + 2j)),
            Portal(inner=(21 + 28j), outer=(17 + 2j)),
            Portal(inner=(13 + 8j), outer=(19 + 34j)),
            Portal(inner=(36 + 21j), outer=(42 + 25j)),
            Portal(inner=(31 + 8j), outer=(42 + 13j)),
            Portal(inner=(36 + 23j), outer=(23 + 34j)),
            Portal(inner=(29 + 28j), outer=(15 + 2j)),
            Portal(inner=(17 + 28j), outer=(2 + 21j)),
            Portal(inner=(8 + 13j), outer=(17 + 34j)),
            Portal(inner=(21 + 8j), outer=(2 + 25j)),
        },
        start=(15 + 34j),
        finish=(13 + 2j),
    ),
)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert (
        Maze.from_text(
            "\n".join(
                (
                    "         A           ",
                    "         A           ",
                    "  #######.#########  ",
                    "  #######.........#  ",
                    "  #######.#######.#  ",
                    "  #######.#######.#  ",
                    "  #######.#######.#  ",
                    "  #####  B    ###.#  ",
                    "BC...##  C    ###.#  ",
                    "  ##.##       ###.#  ",
                    "  ##...DE  F  ###.#  ",
                    "  #####    G  ###.#  ",
                    "  #########.#####.#  ",
                    "DE..#######...###.#  ",
                    "  #.#########.###.#  ",
                    "FG..#########.....#  ",
                    "  ###########.#####  ",
                    "             Z       ",
                    "             Z       ",
                )
            )
        )
        == EXAMPLES[0]
    )
    assert EXAMPLES[0].shortest_path() == 23

    assert (
        Maze.from_text(
            "\n".join(
                (
                    "                   A               ",
                    "                   A               ",
                    "  #################.#############  ",
                    "  #.#...#...................#.#.#  ",
                    "  #.#.#.###.###.###.#########.#.#  ",
                    "  #.#.#.......#...#.....#.#.#...#  ",
                    "  #.#########.###.#####.#.#.###.#  ",
                    "  #.............#.#.....#.......#  ",
                    "  ###.###########.###.#####.#.#.#  ",
                    "  #.....#        A   C    #.#.#.#  ",
                    "  #######        S   P    #####.#  ",
                    "  #.#...#                 #......VT",
                    "  #.#.#.#                 #.#####  ",
                    "  #...#.#               YN....#.#  ",
                    "  #.###.#                 #####.#  ",
                    "DI....#.#                 #.....#  ",
                    "  #####.#                 #.###.#  ",
                    "ZZ......#               QG....#..AS",
                    "  ###.###                 #######  ",
                    "JO..#.#.#                 #.....#  ",
                    "  #.#.#.#                 ###.#.#  ",
                    "  #...#..DI             BU....#..LF",
                    "  #####.#                 #.#####  ",
                    "YN......#               VT..#....QG",
                    "  #.###.#                 #.###.#  ",
                    "  #.#...#                 #.....#  ",
                    "  ###.###    J L     J    #.#.###  ",
                    "  #.....#    O F     P    #.#...#  ",
                    "  #.###.#####.#.#####.#####.###.#  ",
                    "  #...#.#.#...#.....#.....#.#...#  ",
                    "  #.#####.###.###.#.#.#########.#  ",
                    "  #...#.#.....#...#.#.#.#.....#.#  ",
                    "  #.###.#####.###.###.#.#.#######  ",
                    "  #.#.........#...#.............#  ",
                    "  #########.###.###.#############  ",
                    "           B   J   C               ",
                    "           U   P   P               ",
                )
            )
        )
        == EXAMPLES[1]
    )
    assert EXAMPLES[1].shortest_path() == 58


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert EXAMPLES[0].shortest_path_recursive() == 26
    assert EXAMPLES[2].shortest_path_recursive() == 396


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=20)

    maze = Maze.from_text(data)
    print(f"Part 1: {maze.shortest_path()}")
    print(f"Part 2: {maze.shortest_path_recursive()}")


if __name__ == "__main__":
    main()
