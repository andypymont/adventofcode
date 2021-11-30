"""
2016 Day 22
https://adventofcode.com/2016/day/22
"""

from collections import Counter, deque
from dataclasses import dataclass
from itertools import permutations
from typing import Sequence, Set, Tuple
import re
import aocd # type: ignore

re_node = re.compile(r'node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')

@dataclass(frozen=True)
class Point():
    """
    Simple object representing a two-dimensional point.
    """
    x_coord: int
    y_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x_coord+other.x_coord, self.y_coord+other.y_coord)

@dataclass(frozen=True)
class Node():
    """
    A single node on the disk.
    """
    location: Point
    size: int
    used: int
    avail: int

    def forms_viable_pair_with(self, other: 'Node') -> bool:
        """
        Return True/False whether this node can be paired with the given second node.
        """
        return self.used > 0 and self.used <= other.avail

    @classmethod
    def from_match_groups(cls, groups: Sequence[str]) -> 'Node':
        """
        Class method: instantiate a single Node based on the given set of groups for a regex match
        for one node.
        """
        x_coord, y_coord, size, used, avail, _ = map(int, groups)
        return cls(Point(x_coord, y_coord), size, used, avail)

    @classmethod
    def all_from_df_text(cls, text: str) -> 'Sequence[Node]':
        """
        Class method: return a sequence of Node objects, one for each node described in the given
        puzzle input.
        """
        return [cls.from_match_groups(groups) for groups in re_node.findall(text)]

def all_viable_pairs(nodes: Sequence[Node]) -> Sequence[Tuple[Node, Node]]:
    """
    Calculate and return all viable pairs of nodes in the given sequence.
    """
    return [(a, b) for (a, b) in permutations(nodes, 2) if a.forms_viable_pair_with(b)]

COMPASS = (Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0))

@dataclass(frozen=True)
class Situation():
    """
    The current situation on the disk, for use in simulating moves to find the quickest solution.
    """
    reachable: Set[Point]
    empty: Point
    target: Point
    moves: int

    @classmethod
    def from_node_list(cls, nodelist: Sequence[Node]) -> 'Situation':
        """
        Class method to instantiate a Situation object from a sequence of Node objects.
        """
        pairs = all_viable_pairs(nodelist)
        count = Counter([a.location for a, b in pairs] + [b.location for a, b in pairs])
        reachable = set(count.keys())
        empty = next(location for location, c in count.items() if c > 1)
        target = Point(max(loc.x_coord for loc in reachable), 0)
        return cls(reachable, empty, target, 0)

    @property
    def is_valid_state(self) -> bool:
        """
        Property representing whether this is a valid state.
        """
        return self.empty in self.reachable and self.target in self.reachable

    @property
    def description(self) -> str:
        """
        Simple string representation, suitable for debugging and for hashing in order to store
        visited states in the breadth-first-search.
        """
        return f'empty:({str(self.empty)}),target:({str(self.target)})'

    def move_empty_cell(self, direction: Point) -> 'Situation':
        """
        Slide the empty space around the disk in the given direction.
        """
        new_empty = self.empty + direction
        return Situation(
            self.reachable,
            new_empty,
            self.empty if new_empty == self.target else self.target,
            self.moves+1
        )

    def all_possible_moves(self) -> 'Sequence[Situation]':
        """
        Return a sequence of all possible moves from this situation.
        """
        return [
            move
            for move in [self.move_empty_cell(direction) for direction in COMPASS]
            if move.is_valid_state
        ]

def find_shortest_solution(nodes: Sequence[Node]) -> int:
    """
    Find the shortest number of moves to solve the sliding puzzle.
    """
    initial = Situation.from_node_list(nodes)
    visited = set([initial.description])
    search = deque([initial])

    while search:
        candidate = search.popleft()
        if candidate.target == Point(0, 0):
            return candidate.moves
        for potential_next_move in candidate.all_possible_moves():
            if potential_next_move.description not in visited:
                visited.add(potential_next_move.description)
                search.append(potential_next_move)

    return -1

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=22)
    nodes = Node.all_from_df_text(data)

    print(f'Part 1: {len(all_viable_pairs(nodes))}')
    print(f'Part 2: {find_shortest_solution(nodes)}')

if __name__ == '__main__':
    main()
