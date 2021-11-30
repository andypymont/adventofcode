"""
2020 Day 15
https://adventofcode.com/2020/day/15
"""

from collections import deque
from typing import Dict, Iterable, Optional
import aocd # type: ignore

class ElfMemoryGame():

    def __init__(self, starting_numbers: Iterable[int]):
        self.appearances: Dict[int, deque[int]] = {}
        self.length = 0
        for number in starting_numbers:
            self.add(number)

    def __len__(self) -> int:
        return self.length

    def next_number(self, previous: Optional[int] = None) -> int:
        previous = previous or self.latest
        appeared = self.appearances[previous]
        return abs(appeared[1] - appeared[0])

    def extend(self, length: int) -> None:
        while self.length < length:
            self.add(self.next_number())

    def add(self, number: int) -> None:
        if number in self.appearances:
            self.appearances[number].append(self.length)
        else:
            self.appearances[number] = deque([self.length, self.length], maxlen=2)
        self.length += 1
        self.latest = number

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=15)

    emg = ElfMemoryGame(map(int, data.split(',')))
    emg.extend(2020)
    print(f'Part 1: {emg.latest}')

    emg.extend(30_000_000)
    print(f'Part 2: {emg.latest}')

if __name__ == '__main__':
    main()
