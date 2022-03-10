"""
2019 Day 18
https://adventofcode.com/2019/day/18
"""

from collections import deque
from dataclasses import dataclass
from functools import reduce
from heapq import heappop, heappush
from operator import or_
from string import ascii_lowercase, ascii_uppercase
from typing import Dict, Iterator, List, Set, Tuple
import aocd  # type: ignore


def neighbours(point: complex) -> Iterator[complex]:
    """
    Yield all orthogonal neighbours of the given point.
    """
    yield point + complex(0, -1)
    yield point + complex(1, 0)
    yield point + complex(0, 1)
    yield point + complex(-1, 0)


@dataclass(frozen=True)
class Connection:
    """
    A connection between two points of interest in the maze.
    """

    dist: int
    keys: int


@dataclass
class Maze:
    """
    Detailed information about the layout of the maze.
    """

    walls: Set[complex]
    keys: Dict[int, complex]
    doors: Dict[int, complex]
    robots: Dict[int, complex]

    @staticmethod
    def key_number(char: str) -> int:
        """
        Convert a key character into an int so it can be used in binary operations.
        """
        return 2 ** (ord(char.lower()) - 97)

    @classmethod
    def from_text(cls, text: str) -> "Maze":
        """
        Create a Maze object from the puzzle input text.
        """
        walls: Set[complex] = set()
        keys: Dict[int, complex] = {}
        doors: Dict[int, complex] = {}
        robots: Dict[int, complex] = {}

        for y_coord, line in enumerate(text.split("\n")):
            for x_coord, char in enumerate(line):
                pos = complex(x_coord, y_coord)
                if char == "#":
                    walls.add(pos)
                elif char in ascii_lowercase:
                    keys[cls.key_number(char)] = pos
                elif char in ascii_uppercase:
                    doors[cls.key_number(char)] = pos
                elif char == "@":
                    robots[0 - len(robots)] = pos

        return cls(walls, keys, doors, robots)

    def to_graph(self) -> Dict[int, Dict[int, Connection]]:
        """
        Return a graph of the routes between points of interest (starts and keys).
        """
        door_locations = {loc: d for d, loc in self.doors.items()}
        key_locations = {loc: k for k, loc in self.keys.items()}

        graph: Dict[int, Dict[int, Connection]] = {}
        floodfill: deque[Tuple[int, complex, Set[complex], int, int]] = deque()

        for key, pos in self.keys.items():
            graph[key] = {}
            floodfill.append((key, pos, set(self.walls), 0, 0))
        for robot, pos in self.robots.items():
            graph[robot] = {}
            floodfill.append((robot, pos, set(self.walls), 0, 0))

        while floodfill:
            start, pos, visited, keyring, steps = floodfill.popleft()
            visited.add(pos)

            key_here = key_locations.get(pos)
            if key_here and key_here != start:
                graph[start][key_here] = Connection(steps, keyring)
                keyring |= key_here
            if door_here := door_locations.get(pos):
                keyring |= door_here

            for newpos in neighbours(pos):
                if newpos not in visited:
                    floodfill.append((start, newpos, visited, keyring, steps + 1))

        return graph


@dataclass(frozen=True, order=True)
class GraphPathSearchState:
    """
    A single state in our search of paths through a graph.
    """

    dist: int
    keyring: int
    positions: Tuple[int, ...]

    def reachable_locations(
        self, graph: Dict[int, Dict[int, Connection]], pos: int
    ) -> Dict[int, int]:
        """
        Yield the set of reachable locations in the given graph, from a specific
        location and with the current keyring.
        """
        return {
            newpos: connection.dist
            for newpos, connection in graph[pos].items()
            if newpos & self.keyring == 0
            and connection.keys & self.keyring == connection.keys
        }

    def reachable_states(
        self, graph: Dict[int, Dict[int, Connection]]
    ) -> Iterator["GraphPathSearchState"]:
        """
        Yield all reachable states from this current state.
        """
        for robot, pos in enumerate(self.positions):
            for newpos, dist in self.reachable_locations(graph, pos).items():
                positions = tuple(
                    newpos if p == robot else pos
                    for p, pos in enumerate(self.positions)
                )
                yield self.__class__(self.dist + dist, self.keyring | newpos, positions)


def shortest_path(graph: Dict[int, Dict[int, Connection]]) -> int:
    """
    Given a connection graph for a maze, calculate the shortest possible route.
    """
    starts = tuple(node for node in graph if node <= 0)
    full_keyring = reduce(or_, (node for node in graph if node > 0))
    visited = set()
    consider: List[GraphPathSearchState] = [GraphPathSearchState(0, 0, starts)]

    while consider:
        state = heappop(consider)
        if state.keyring & full_keyring == full_keyring:
            return state.dist
        for reachable in state.reachable_states(graph):
            if reachable not in visited:
                heappush(consider, reachable)
                visited.add(reachable)

    return -1


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    maze1 = Maze(
        walls={
            0 + 0j,
            1 + 0j,
            2 + 0j,
            3 + 0j,
            4 + 0j,
            5 + 0j,
            6 + 0j,
            7 + 0j,
            8 + 0j,
            0 + 1j,
            8 + 1j,
            0 + 2j,
            1 + 2j,
            2 + 2j,
            3 + 2j,
            4 + 2j,
            5 + 2j,
            6 + 2j,
            7 + 2j,
            8 + 2j,
        },
        keys={
            1: 7 + 1j,
            2: 1 + 1j,
        },
        doors={
            1: 3 + 1j,
        },
        robots={
            0: 5 + 1j,
        },
    )
    assert (
        Maze.from_text(
            "\n".join(
                (
                    "#########",
                    "#b.A.@.a#",
                    "#########",
                )
            )
        )
        == maze1
    )
    eg1 = {
        0: {
            1: Connection(dist=2, keys=0),
            2: Connection(dist=4, keys=1),
        },
        1: {
            2: Connection(dist=6, keys=1),
        },
        2: {
            1: Connection(dist=6, keys=1),
        },
    }
    assert maze1.to_graph() == eg1
    assert shortest_path(eg1) == 8

    eg2 = {
        0: {
            1: Connection(2, 0),
            2: Connection(4, 1),
            4: Connection(6, 3),
            8: Connection(30, 7),
            16: Connection(8, 7),
            32: Connection(14, 31),
        },
        1: {
            2: Connection(6, 1),
            4: Connection(4, 2),
            8: Connection(28, 6),
            16: Connection(10, 7),
            32: Connection(16, 31),
        },
        2: {
            1: Connection(6, 1),
            4: Connection(10, 3),
            8: Connection(34, 7),
            16: Connection(4, 4),
            32: Connection(10, 28),
        },
        4: {
            1: Connection(4, 2),
            2: Connection(10, 3),
            8: Connection(24, 0),
            16: Connection(14, 7),
            32: Connection(20, 31),
        },
        8: {
            1: Connection(28, 6),
            2: Connection(34, 7),
            4: Connection(24, 0),
            16: Connection(38, 7),
            32: Connection(44, 31),
        },
        16: {
            1: Connection(10, 7),
            2: Connection(4, 4),
            4: Connection(14, 7),
            8: Connection(38, 7),
            32: Connection(6, 24),
        },
        32: {
            1: Connection(16, 31),
            2: Connection(10, 28),
            4: Connection(20, 31),
            8: Connection(44, 31),
            16: Connection(6, 24),
        },
    }
    assert (
        Maze.from_text(
            "\n".join(
                (
                    "########################",
                    "#f.D.E.e.C.b.A.@.a.B.c.#",
                    "######################.#",
                    "#d.....................#",
                    "########################",
                )
            )
        ).to_graph()
        == eg2
    )
    assert shortest_path(eg2) == 86

    eg3 = Maze.from_text(
        "\n".join(
            (
                "#######",
                "#a.#Cd#",
                "##...##",
                "##.@.##",
                "##...##",
                "#cB#Ab#",
                "#######",
            )
        )
    ).to_graph()
    assert shortest_path(eg3) == 26


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=18)

    maze = Maze.from_text(data)
    graph = maze.to_graph()
    print(f"Part 1: {shortest_path(graph)}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
