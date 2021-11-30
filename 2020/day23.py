"""
2020 Day 23
https://adventofcode.com/2020/day/23
"""

from math import prod
from typing import Dict, List
import aocd # type: ignore

class Cup():

    def __init__(self, identifier: int):
        self.identifier = identifier
        self.left = self
        self.right = self

    def __repr__(self) -> str:
        left = None if self.left is self else self.left.identifier
        right = None if self.right is self else self.right.identifier
        return f'Cup(identifier={self.identifier}, left={left}, right={right})'

    def insert(self, new_right_neighbour: 'Cup') -> None:
        new_right_neighbour.left = self
        if self.left is self and self.right is self:
            new_right_neighbour.right = self
            self.left = new_right_neighbour
        else:
            new_right_neighbour.right = self.right
            self.right.left = new_right_neighbour
        self.right = new_right_neighbour

    def remove(self) -> 'Cup':
        self.left.right = self.right
        self.right.left = self.left
        self.left = self
        self.right = self
        return self

class Game():

    def __init__(self, cups: Dict[int, Cup], current: Cup):
        self.cups = cups
        self.current = current

    def __repr__(self) -> str:
        return f'Game(cups=[{len(self.cups)} cups], current={self.current.identifier})'

    @classmethod
    def from_puzzle_input(cls, text: str, million_cups: bool = False) -> 'Game':
        cup_order = tuple(int(digit) for digit in text)
        if million_cups:
            cup_order += tuple(range(max(cup_order)+1, 1_000_001))

        cups = {}
        first = current = Cup(cup_order[0])
        cups[first.identifier] = first

        for cup_id in cup_order[1:]:
            new_cup = Cup(cup_id)
            current.insert(new_cup)
            cups[cup_id] = new_cup
            current = new_cup

        return cls(cups, first)

    @property
    def cup_order(self) -> List[int]:
        order = []
        node = self.cups[1]
        for _ in range(len(self.cups)-1):
            node = node.right
            order.append(node.identifier)
        return order

    def play(self, moves: int) -> 'Game':
        for _ in range(moves):
            removed = [self.current.right, self.current.right.right, self.current.right.right.right]
            for removal in removed:
                removal.remove()
            removed_ids = {removal.identifier for removal in removed}

            destination_id = self.current.identifier - 1
            while destination_id in removed_ids or destination_id == 0:
                destination_id -= 1
                if destination_id <= 0:
                    destination_id = max(cup_id for cup_id in self.cups)
            destination = self.cups[destination_id]

            for insertion in removed:
                destination.insert(insertion)
                destination = insertion
            self.current = self.current.right
        return self

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=23)

    order = Game.from_puzzle_input(data).play(100).cup_order
    part1 = ''.join(str(cup_id) for cup_id in order)
    print(f'Part 1: {part1}')

    bigger_game = Game.from_puzzle_input(data, million_cups=True)
    bigger_game.play(10_000_000)
    interesting_cups = (bigger_game.cups[1].right, bigger_game.cups[1].right.right)
    part2 = prod(cup.identifier for cup in interesting_cups)
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
