"""
2016 Day 19
https://adventofcode.com/2016/day/19
"""

# The problem presented here in 2016 Day 19 is also known as The Josephus Problem:
# https://www.youtube.com/watch?v=uCsD3ZGzMgE

from typing import Sequence
import numpy as np
import aocd  # type: ignore


def who_wins(elfcount: int) -> int:
    """
    Use the general solution of the Josephus problem to solve for the given quantity of elves.
    Return the number of the winning elf.
    """
    binary = np.binary_repr(elfcount)
    return int(binary[1:] + binary[0], 2)


class Elf:
    """
    An elf, sat in the circle and ready for the Josephus-inspired game.
    """

    number: int
    prev: "Elf"
    next: "Elf"

    def __init__(self, number: int):
        self.number = number

    def delete(self) -> None:
        """
        Remove this elf from the circle and update its neighbours to point at each other instead.
        """
        self.next.prev = self.prev
        self.prev.next = self.next

    @classmethod
    def circle(cls, length: int) -> "Sequence[Elf]":
        """
        Instatiate a circle of elves of the given length, each aware of its neighbours.
        """
        circle = [cls(x) for x in range(1, length + 1)]
        for index in range(length):
            circle[index].prev = circle[(index - 1) % length]
            circle[index].next = circle[(index + 1) % length]
        return circle


def who_wins_opposite(elfcount: int) -> int:
    """
    Return the number of the Elf that wins in the 'eliminate opposite' version of the game.
    """
    circle = Elf.circle(elfcount)

    elf = circle[0]
    mid = circle[int(elfcount / 2)]

    for theft in range(elfcount - 1):
        mid.delete()
        mid = mid.next
        if (elfcount - theft) % 2 == 1:
            mid = mid.next
        elf = elf.next

    return elf.number


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=19)
    elfcount = int(data)

    print(f"Part 1: {who_wins(elfcount)}")
    print(f"Part 2: {who_wins_opposite(elfcount)}")


if __name__ == "__main__":
    main()
