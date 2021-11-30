"""
2020 Day 24
https://adventofcode.com/2020/day/24
"""

from dataclasses import dataclass
from functools import reduce
from operator import __or__ as union
from typing import Set
import aocd # type: ignore

@dataclass(frozen=True, order=True)
class Hex():
    x: int
    y: int

    @classmethod
    def from_directions(cls, directions: str) -> 'Hex':
        pos = 0
        location = cls(0, 0)
        while pos < len(directions):
            direction = COMPASS.get(directions[pos:pos+2])
            if direction:
                location += direction
                pos += 2
            else:
                location += COMPASS[directions[pos]]
                pos += 1
        return location

    def __add__(self, other: 'Hex') -> 'Hex':
        return Hex(self.x+other.x, self.y+other.y)

    @property
    def neighbours(self) -> Set['Hex']:
        return set(self+other for other in COMPASS.values())

COMPASS = {
'nw': Hex(0, 1),
'ne': Hex(1, 0),
'w': Hex(-1, 1),
'e': Hex(1, -1),
'sw': Hex(-1, 0),
'se': Hex(0, -1),
}

def black_tiles(text: str) -> Set[Hex]:
    tiles: Set[Hex] = set()
    for line in text.split('\n'):
        tile = Hex.from_directions(line)
        if tile in tiles:
            tiles.remove(tile)
        else:
            tiles.add(tile)
    return tiles

def hex_game_of_life(tiles: Set[Hex], steps: int) -> Set[Hex]:
    for _ in range(steps):
        relevant = reduce(union, (tile.neighbours for tile in tiles), tiles)
        tiles = {
            tile for tile in relevant
            if (tile in tiles and len(tile.neighbours.intersection(tiles)) in (1, 2))
            or (tile not in tiles and len(tile.neighbours.intersection(tiles)) == 2)
        }
    return tiles

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=24)
    black = black_tiles(data)

    print(f'Part 1: {len(black)}')
    print(f'Part 2: {len(hex_game_of_life(black, 100))}')

if __name__ == '__main__':
    main()
