"""
2018 Day 8
https://adventofcode.com/2018/day/8
"""

from dataclasses import dataclass
from typing import Iterator, Tuple
import aocd # type: ignore

def iterator_from_text(text: str) -> Iterator[int]:
    return (int(item) for item in text.split(' '))

@dataclass(frozen=True)
class Node():
    children: Tuple
    metadata: Tuple

    @property
    def value(self) -> int:
        if len(self.children) == 0:
            return sum(self.metadata)
        indices = [ix-1 for ix in self.metadata if 0 < ix <= len(self.children)]
        return sum(self.children[ix].value for ix in indices)

    @property
    def total_metadata(self) -> int:
        return sum(self.metadata) + sum(child.total_metadata for child in self.children)

    @classmethod
    def from_iterator(cls, generator: Iterator[int]) -> 'Node':
        childcount = next(generator)
        metacount = next(generator)
        children = tuple(cls.from_iterator(generator) for child in range(childcount))
        metadata = tuple(next(generator) for child in range(metacount))
        return cls(children, metadata)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=8)
    root = Node.from_iterator(iterator_from_text(data))

    print(f'Part 1: {root.total_metadata}')
    print(f'Part 2: {root.value}')

if __name__ == '__main__':
    main()
