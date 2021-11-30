"""
2018 Day 9
https://adventofcode.com/2018/day/9
"""

import re
import aocd # type: ignore

RE_SCENARIO = re.compile(r'(\d+) players; last marble is worth (\d+) points')

class Marble:

    def __init__(self, number: int):
        self.number = number
        self.left = self
        self.right = self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Marble):
            return NotImplemented
        return self.number == other.number

    def __repr__(self) -> str:
        left = f'Marble(number={self.left.number}, ...)' if self.left else 'None'
        right = f'Marble(number={self.right.number}, ...)' if self.right else 'None'
        return f'Marble(number={self.number}, left={left}, right={right})'

    @classmethod
    def initial_marble(cls, number: int = 0) -> 'Marble':
        marble = cls(number)
        marble.left = marble
        marble.right = marble
        return marble

    @property
    def seven_counter_clockwise(self) -> 'Marble':
        return self.right.right.right.right.right.right.right

    def place(self, marble: 'Marble') -> 'Marble':
        marble.right, marble.left = self.left, self.left.left
        marble.right.left = marble.left.right = marble
        return marble

    def remove(self) -> 'Marble':
        self.left.right = self.right
        self.right.left = self.left
        self.left = self
        self.right = self
        return self

def play_game(players: int, last_marble: int) -> int:
    collected = dict((player, 0) for player in range(players))
    player = 0

    marble = Marble.initial_marble()
    for marble_no in range(1, last_marble+1):
        new_marble = Marble(marble_no)
        if marble_no % 23 == 0:
            collected[player] += new_marble.number
            seven_cc = marble.seven_counter_clockwise
            marble = seven_cc.left
            collected[player] += seven_cc.remove().number
        else:
            marble = marble.place(new_marble)

        player = (player + 1) % players

    return max(score for (player, score) in collected.items())

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=9)
    matches = RE_SCENARIO.search(data)
    if matches:
        players, last_marble = map(int, matches.groups())

        print(f'Part 1: {play_game(players, last_marble)}')
        print(f'Part 2: {play_game(players, last_marble*100)}')

if __name__ == '__main__':
    main()
