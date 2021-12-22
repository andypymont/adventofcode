"""
2016 Day 11
https://adventofcode.com/2016/day/11
"""

from collections import deque
from itertools import chain, combinations
from functools import reduce
from operator import add
from typing import Any, Dict, Iterable, Sequence, Tuple
import re
import aocd  # type: ignore

RE_CHIPS = re.compile(r"(?:a|an) (\w+)-compatible microchip")
RE_GENERATORS = re.compile(r"(?:a|an) (\w+) generator")


def read_items(text: str) -> Tuple[int, ...]:
    """
    Read initial item positions from the puzzle description.
    """
    elements: Dict[str, Tuple[int, int]] = {}

    for floor, line in enumerate(text.split("\n")):
        for match in RE_CHIPS.finditer(line):
            genfloor, _ = elements.get(match.group(1), (0, 0))
            elements[match.group(1)] = (genfloor, floor)
        for match in RE_GENERATORS.finditer(line):
            _, chipfloor = elements.get(match.group(1), (0, 0))
            elements[match.group(1)] = (floor, chipfloor)

    return reduce(add, elements.values())


class GameState:
    """
    The current state of the puzzle, i.e. the floor on which each item and the elevator are
    currently located.
    """

    def __init__(self, elevator: int, items: Iterable[int]):
        self.elevator = elevator
        items = list(items)
        item_pairs = (items[i : i + 2] for i in range(0, len(items), 2))
        self.items = tuple(item for pair in sorted(item_pairs) for item in pair)

    def __eq__(self, other: Any) -> bool:
        return self.elevator == other.elevator and self.items == other.items

    def __hash__(self) -> int:
        return hash((self.elevator, self.items))

    def __repr__(self) -> str:
        return f"GameState(elevator={self.elevator}, items={repr(self.items)})"

    def is_legal(self) -> bool:
        """
        Check whether the game-state is legal, i.e. whether any microchip is co-located with a set
        of generators not including its own.
        """
        generators = tuple(item for n, item in enumerate(self.items) if n % 2 == 0)
        microchips = tuple(item for n, item in enumerate(self.items) if n % 2 == 1)
        return not any(
            (
                generators[n] != microchip
                and sum(1 for gen in generators if gen == microchip) > 0
            )
            for n, microchip in enumerate(microchips)
        )

    def apply_move(self, direction: int, itemindices: Sequence[int]) -> "GameState":
        """
        Make a move, taking the elevator in the given direction and bringing along the items from
        self.items which have the given indices.
        """
        items = tuple(
            (item + direction if index in itemindices else item)
            for index, item in enumerate(self.items)
        )
        return GameState(self.elevator + direction, items)

    def all_possible_moves(self) -> "Iterable[GameState]":
        """
        Calculate all possible next-moves from this state.
        """
        reachable = [
            itemno for itemno, floor in enumerate(self.items) if floor == self.elevator
        ]
        combos = list(
            chain(*(combinations(reachable, quantity) for quantity in (1, 2)))
        )

        upward = (
            (self.apply_move(+1, combo) for combo in combos)
            if self.elevator < 3
            else tuple()
        )
        dnward = (
            (self.apply_move(-1, combo) for combo in combos)
            if self.elevator > 0
            else tuple()
        )

        return chain(upward, dnward)


def find_shortest_solution(start: GameState) -> int:
    """
    Find the shortest number of moves from the given state to a winning one.
    """
    finish = GameState(3, [3 for item in start.items])
    visited = set()
    search = deque([(0, start)])

    while search:
        moves, state = search.popleft()

        if state == finish:
            return moves
        if state not in visited:
            search.extend(
                (moves + 1, newstate)
                for newstate in state.all_possible_moves()
                if newstate.is_legal()
            )
            visited.add(state)

    return -1


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=11)
    items = read_items(data)

    state_p1 = GameState(0, items)
    print(f"Part 1: {find_shortest_solution(state_p1)}")

    state_p2 = GameState(0, items + (0, 0, 0, 0))
    print(f"Part 2: {find_shortest_solution(state_p2)}")


if __name__ == "__main__":
    main()
