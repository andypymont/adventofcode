"""
2021 Day 11
https://adventofcode.com/2021/day/11
"""

from collections import deque
from itertools import count
from typing import Dict, Iterator, Set
import aocd # type: ignore

def read_octopuses(text: str) -> Dict[complex, int]:
    octopuses: Dict[complex, int] = {}
    for y, line in enumerate(text.split('\n')):
        for x, digit in enumerate(line):
            octopuses[complex(x, y)] = int(digit)
    return octopuses

DIRECTIONS: Set[complex] = {-1-1j, -1+0j, -1+1j, 0-1j, 0+1j, 1-1j, 1+0j, 1+1j}

def neighbours(point: complex) -> Iterator[complex]:
    return (point + direction for direction in DIRECTIONS)

def step(octopuses: Dict[complex, int]) -> Dict[complex, int]:
    octopuses = {location: energy + 1 for location, energy in octopuses.items()}
    flashed: Set[complex] = set()
    flashers = deque(octopus for octopus, energy in octopuses.items() if energy > 9)
    while flashers:
        flasher = flashers.popleft()
        if flasher not in flashed:
            flasher_neighbours = {n for n in neighbours(flasher) if n in octopuses}
            octopuses.update({n: octopuses[n] + 1 for n in flasher_neighbours})
            flashers.extend(n for n in flasher_neighbours if octopuses[n] > 9 and n not in flashed)
            flashed.add(flasher)
    return {location: (0 if energy > 9 else energy) for location, energy in octopuses.items()}

def flashes(octopuses: Dict[complex, int], steps: int) -> int:
    flash_count = 0
    for _ in range(steps):
        octopuses = step(octopuses)
        flash_count += sum(1 for energy in octopuses.values() if energy == 0)
    return flash_count

def all_flash(octopuses: Dict[complex, int]) -> int:
    for step_no in count(1):
        octopuses = step(octopuses)
        if set(octopuses.values()) == {0}:
            return step_no
    return -1

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    octopuses = {
        0+0j: 5, 1+0j: 4, 2+0j: 8, 3+0j: 3, 4+0j: 1, 5+0j: 4, 6+0j: 3, 7+0j: 2, 8+0j: 2, 9+0j: 3,
        0+1j: 2, 1+1j: 7, 2+1j: 4, 3+1j: 5, 4+1j: 8, 5+1j: 5, 6+1j: 4, 7+1j: 7, 8+1j: 1, 9+1j: 1,
        0+2j: 5, 1+2j: 2, 2+2j: 6, 3+2j: 4, 4+2j: 5, 5+2j: 5, 6+2j: 6, 7+2j: 1, 8+2j: 7, 9+2j: 3,
        0+3j: 6, 1+3j: 1, 2+3j: 4, 3+3j: 1, 4+3j: 3, 5+3j: 3, 6+3j: 6, 7+3j: 1, 8+3j: 4, 9+3j: 6,
        0+4j: 6, 1+4j: 3, 2+4j: 5, 3+4j: 7, 4+4j: 3, 5+4j: 8, 6+4j: 5, 7+4j: 4, 8+4j: 7, 9+4j: 8,
        0+5j: 4, 1+5j: 1, 2+5j: 6, 3+5j: 7, 4+5j: 5, 5+5j: 2, 6+5j: 4, 7+5j: 6, 8+5j: 4, 9+5j: 5,
        0+6j: 2, 1+6j: 1, 2+6j: 7, 3+6j: 6, 4+6j: 8, 5+6j: 4, 6+6j: 1, 7+6j: 7, 8+6j: 2, 9+6j: 1,
        0+7j: 6, 1+7j: 8, 2+7j: 8, 3+7j: 2, 4+7j: 8, 5+7j: 8, 6+7j: 1, 7+7j: 1, 8+7j: 3, 9+7j: 4,
        0+8j: 4, 1+8j: 8, 2+8j: 4, 3+8j: 6, 4+8j: 8, 5+8j: 4, 6+8j: 8, 7+8j: 5, 8+8j: 5, 9+8j: 4,
        0+9j: 5, 1+9j: 2, 2+9j: 8, 3+9j: 3, 4+9j: 7, 5+9j: 5, 6+9j: 1, 7+9j: 5, 8+9j: 2, 9+9j: 6,
    }
    assert read_octopuses('\n'.join((
        '5483143223',
        '2745854711',
        '5264556173',
        '6141336146',
        '6357385478',
        '4167524645',
        '2176841721',
        '6882881134',
        '4846848554',
        '5283751526',
    ))) == octopuses
    step1 = {
        0+0j: 6, 1+0j: 5, 2+0j: 9, 3+0j: 4, 4+0j: 2, 5+0j: 5, 6+0j: 4, 7+0j: 3, 8+0j: 3, 9+0j: 4,
        0+1j: 3, 1+1j: 8, 2+1j: 5, 3+1j: 6, 4+1j: 9, 5+1j: 6, 6+1j: 5, 7+1j: 8, 8+1j: 2, 9+1j: 2,
        0+2j: 6, 1+2j: 3, 2+2j: 7, 3+2j: 5, 4+2j: 6, 5+2j: 6, 6+2j: 7, 7+2j: 2, 8+2j: 8, 9+2j: 4,
        0+3j: 7, 1+3j: 2, 2+3j: 5, 3+3j: 2, 4+3j: 4, 5+3j: 4, 6+3j: 7, 7+3j: 2, 8+3j: 5, 9+3j: 7,
        0+4j: 7, 1+4j: 4, 2+4j: 6, 3+4j: 8, 4+4j: 4, 5+4j: 9, 6+4j: 6, 7+4j: 5, 8+4j: 8, 9+4j: 9,
        0+5j: 5, 1+5j: 2, 2+5j: 7, 3+5j: 8, 4+5j: 6, 5+5j: 3, 6+5j: 5, 7+5j: 7, 8+5j: 5, 9+5j: 6,
        0+6j: 3, 1+6j: 2, 2+6j: 8, 3+6j: 7, 4+6j: 9, 5+6j: 5, 6+6j: 2, 7+6j: 8, 8+6j: 3, 9+6j: 2,
        0+7j: 7, 1+7j: 9, 2+7j: 9, 3+7j: 3, 4+7j: 9, 5+7j: 9, 6+7j: 2, 7+7j: 2, 8+7j: 4, 9+7j: 5,
        0+8j: 5, 1+8j: 9, 2+8j: 5, 3+8j: 7, 4+8j: 9, 5+8j: 5, 6+8j: 9, 7+8j: 6, 8+8j: 6, 9+8j: 5,
        0+9j: 6, 1+9j: 3, 2+9j: 9, 3+9j: 4, 4+9j: 8, 5+9j: 6, 6+9j: 2, 7+9j: 6, 8+9j: 3, 9+9j: 7,
    }
    assert step(octopuses) == step1
    step2 = {
        0+0j: 8, 1+0j: 8, 2+0j: 0, 3+0j: 7, 4+0j: 4, 5+0j: 7, 6+0j: 6, 7+0j: 5, 8+0j: 5, 9+0j: 5,
        0+1j: 5, 1+1j: 0, 2+1j: 8, 3+1j: 9, 4+1j: 0, 5+1j: 8, 6+1j: 7, 7+1j: 0, 8+1j: 5, 9+1j: 4,
        0+2j: 8, 1+2j: 5, 2+2j: 9, 3+2j: 7, 4+2j: 8, 5+2j: 8, 6+2j: 9, 7+2j: 6, 8+2j: 0, 9+2j: 8,
        0+3j: 8, 1+3j: 4, 2+3j: 8, 3+3j: 5, 4+3j: 7, 5+3j: 6, 6+3j: 9, 7+3j: 6, 8+3j: 0, 9+3j: 0,
        0+4j: 8, 1+4j: 7, 2+4j: 0, 3+4j: 0, 4+4j: 9, 5+4j: 0, 6+4j: 8, 7+4j: 8, 8+4j: 0, 9+4j: 0,
        0+5j: 6, 1+5j: 6, 2+5j: 0, 3+5j: 0, 4+5j: 0, 5+5j: 8, 6+5j: 8, 7+5j: 9, 8+5j: 8, 9+5j: 9,
        0+6j: 6, 1+6j: 8, 2+6j: 0, 3+6j: 0, 4+6j: 0, 5+6j: 0, 6+6j: 5, 7+6j: 9, 8+6j: 4, 9+6j: 3,
        0+7j: 0, 1+7j: 0, 2+7j: 0, 3+7j: 0, 4+7j: 0, 5+7j: 0, 6+7j: 7, 7+7j: 4, 8+7j: 5, 9+7j: 6,
        0+8j: 9, 1+8j: 0, 2+8j: 0, 3+8j: 0, 4+8j: 0, 5+8j: 0, 6+8j: 0, 7+8j: 8, 8+8j: 7, 9+8j: 6,
        0+9j: 8, 1+9j: 7, 2+9j: 0, 3+9j: 0, 4+9j: 0, 5+9j: 0, 6+9j: 6, 7+9j: 8, 8+9j: 4, 9+9j: 8,
    }
    assert step(step1) == step2
    assert flashes(octopuses, 1) == 0
    assert flashes(octopuses, 2) == 35
    assert flashes(octopuses, 3) == 80
    assert flashes(octopuses, 10) == 204

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    octopuses = {
        0+0j: 5, 1+0j: 4, 2+0j: 8, 3+0j: 3, 4+0j: 1, 5+0j: 4, 6+0j: 3, 7+0j: 2, 8+0j: 2, 9+0j: 3,
        0+1j: 2, 1+1j: 7, 2+1j: 4, 3+1j: 5, 4+1j: 8, 5+1j: 5, 6+1j: 4, 7+1j: 7, 8+1j: 1, 9+1j: 1,
        0+2j: 5, 1+2j: 2, 2+2j: 6, 3+2j: 4, 4+2j: 5, 5+2j: 5, 6+2j: 6, 7+2j: 1, 8+2j: 7, 9+2j: 3,
        0+3j: 6, 1+3j: 1, 2+3j: 4, 3+3j: 1, 4+3j: 3, 5+3j: 3, 6+3j: 6, 7+3j: 1, 8+3j: 4, 9+3j: 6,
        0+4j: 6, 1+4j: 3, 2+4j: 5, 3+4j: 7, 4+4j: 3, 5+4j: 8, 6+4j: 5, 7+4j: 4, 8+4j: 7, 9+4j: 8,
        0+5j: 4, 1+5j: 1, 2+5j: 6, 3+5j: 7, 4+5j: 5, 5+5j: 2, 6+5j: 4, 7+5j: 6, 8+5j: 4, 9+5j: 5,
        0+6j: 2, 1+6j: 1, 2+6j: 7, 3+6j: 6, 4+6j: 8, 5+6j: 4, 6+6j: 1, 7+6j: 7, 8+6j: 2, 9+6j: 1,
        0+7j: 6, 1+7j: 8, 2+7j: 8, 3+7j: 2, 4+7j: 8, 5+7j: 8, 6+7j: 1, 7+7j: 1, 8+7j: 3, 9+7j: 4,
        0+8j: 4, 1+8j: 8, 2+8j: 4, 3+8j: 6, 4+8j: 8, 5+8j: 4, 6+8j: 8, 7+8j: 5, 8+8j: 5, 9+8j: 4,
        0+9j: 5, 1+9j: 2, 2+9j: 8, 3+9j: 3, 4+9j: 7, 5+9j: 5, 6+9j: 1, 7+9j: 5, 8+9j: 2, 9+9j: 6,
    }
    assert all_flash(octopuses) == 195

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=11)
    octopuses = read_octopuses(data)

    print(f'Part 1: {flashes(octopuses, 100)}')
    print(f'Part 2: {all_flash(octopuses)}')

if __name__ == '__main__':
    main()
