"""
2019 Day 12
https://adventofcode.com/2019/day/12
"""

import re
from itertools import count
from typing import Dict, Tuple
import aocd # type: ignore
import numpy as np

RE_MOON = re.compile(r'<x=([-\d ]+), y=([-\d ]+), z=([-\d ]+)>')

def read_moon(line: str) -> Tuple[int, int, int]:
    match = RE_MOON.match(line)
    if not match:
        raise ValueError
    posx, posy, posz = [int(g) for g in match.groups()]
    return posx, posy, posz

def read_moons(text: str) -> np.ndarray:
    return np.array([read_moon(line) + (0, 0, 0) for line in text.split('\n')])

def advance_moon(moon: np.ndarray, moons: np.ndarray) -> np.ndarray:
    gravity = np.array([
        (moons[:,col] > moon[col]).sum() - (moons[:,col] < moon[col]).sum()
        for col in range(3)
    ])
    return moon + np.hstack((gravity + moon[3:], gravity))

def advance(moons: np.ndarray, steps: int = 1) -> np.ndarray:
    for _ in range(steps):
        moons = np.array([advance_moon(moon, moons) for moon in moons])
    return moons

def total_energy(moons: np.ndarray) -> int:
    values = np.absolute(moons)
    potential = values[:,0] + values[:,1] + values[:,2]
    kinetic = values[:,3] + values[:,4] + values[:,5]
    return int((potential * kinetic).sum())

DIMENSIONS: Dict[str, Tuple[int, int]] = {
    'x': (0, 3),
    'y': (1, 4),
    'z': (2, 5),
}

def steps_to_repeat(moons: np.ndarray) -> int:
    search: Dict[str, str] = {
        dim: moons[:, cols] for dim, cols in DIMENSIONS.items()
    }
    found: Dict[str, int] = {}

    for steps in count(1):
        moons = advance(moons)
        for dimension, cols in DIMENSIONS.items():
            if (moons[:, cols] == search[dimension]).all():
                found[dimension] = steps
        if len(found) == 3:
            break
    
    return int(np.lcm.reduce([found['x'], found['y'], found['z']]))

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    example = '\n'.join((
        '<x=-1, y=0, z=2>',
        '<x=2, y=-10, z=-7>',
        '<x=4, y=-8, z=8>',
        '<x=3, y=5, z=-1>',
    ))
    moons = np.array([
        [-1, 0, 2, 0, 0, 0],
        [2, -10, -7, 0, 0, 0],
        [4, -8, 8, 0, 0, 0],
        [3, 5, -1, 0, 0, 0]
    ])
    assert (moons == read_moons(example)).all()
    one = np.array([
        [2, -1, 1, 3, -1, -1],
        [3, -7, -4, 1, 3, 3],
        [1, -7, 5, -3, 1, -3],
        [2, 2, 0, -1, -3, 1]
    ])
    assert(advance(moons) == one).all()
    ten = np.array([
        [2, 1, -3, -3, -2, 1],
        [1, -8, 0, -1, 1, 3],
        [3, -6, 1, 3, 2, -3],
        [2, 0, 4, 1, -1, -1],
    ])
    assert (advance(moons, 10) == ten).all()
    assert total_energy(ten) == 179

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    moons = np.array([
        [-1, 0, 2, 0, 0, 0],
        [2, -10, -7, 0, 0, 0],
        [4, -8, 8, 0, 0, 0],
        [3, 5, -1, 0, 0, 0],
    ])
    assert steps_to_repeat(moons) == 2772

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=12)
    moons = read_moons(data)

    thousand = advance(moons, 1000)
    print(f'Part 1: {total_energy(thousand)}')

    print(f'Part 2: {steps_to_repeat(moons)}')

if __name__ == '__main__':
    main()
