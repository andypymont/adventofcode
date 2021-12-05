"""
2019 Day 6
https://adventofcode.com/2019/day/6
"""

from collections import deque
from typing import Dict, Set, Tuple
import aocd # type: ignore

def read_orbits(text: str) -> Dict[str, str]:
    orbits: Dict[str, str] = {}
    for line in text.split('\n'):
        orbitee, orbiter = line.split(')')
        orbits[orbiter] = orbitee
    return orbits

def count_orbits(orbits: Dict[str, str], name: str) -> int:
    if name not in orbits:
        return 0
    return 1 + count_orbits(orbits, orbits[name])

def total_orbits(orbits: Dict[str, str]) -> int:
    return sum(count_orbits(orbits, name) for name in orbits.keys())

def transfer_map(orbits: Dict[str, str]) -> Dict[str, Set[str]]:
    transfers: Dict[str, Set[str]] = {}
    for orbiter, orbitee in orbits.items():
        if orbiter not in transfers:
            transfers[orbiter] = set()
        if orbitee not in transfers:
            transfers[orbitee] = set()
        transfers[orbiter].add(orbitee)
        transfers[orbitee].add(orbiter)
    return transfers

def shortest_path(transfers: Dict[str, Set[str]], origin: str, target: str) -> int:
    search: deque[Tuple[str, int]] = deque([(origin, 0)])
    visited: Set[str] = set()

    while search:
        location, distance = search.popleft()

        if location == target:
            return distance - 2

        visited.add(location)
        for reachable in transfers.get(location, set()):
            if reachable not in visited:
                search.append((reachable, distance + 1))

    return -1

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    ex1 = '\n'.join((
        'COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L'
    ))
    eg1 = {
        'L': 'K',
        'K': 'J',
        'J': 'E',
        'F': 'E',
        'E': 'D',
        'I': 'D',
        'D': 'C',
        'C': 'B',
        'H': 'G',
        'G': 'B',
        'B': 'COM'
    }
    assert read_orbits(ex1) == eg1
    assert count_orbits(eg1, 'D') == 3
    assert count_orbits(eg1, 'L') == 7
    assert count_orbits(eg1, 'COM') == 0
    assert total_orbits(eg1) == 42

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    orbits = {
        'B': 'COM',
        'C': 'B',
        'D': 'C',
        'E': 'D',
        'F': 'E',
        'G': 'B',
        'H': 'G',
        'I': 'D',
        'J': 'E',
        'K': 'J',
        'L': 'K',
        'SAN': 'I',
        'YOU': 'K',
    }
    transfers = {
        'COM': {'B'},
        'B': {'COM', 'C', 'G'},
        'C': {'B', 'D'},
        'D': {'C', 'E', 'I'},
        'E': {'D', 'F', 'J'},
        'F': {'E'},
        'G': {'B', 'H'},
        'H': {'G'},
        'I': {'D', 'SAN'},
        'J': {'E', 'K'},
        'K': {'J', 'L', 'YOU'},
        'L': {'K'},
        'SAN': {'I'},
        'YOU': {'K'},
    }
    assert transfer_map(orbits) == transfers
    assert shortest_path(transfers, 'YOU', 'SAN') == 4

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=6)

    orbits = read_orbits(data)
    print(f'Part 1: {total_orbits(orbits)}')

    transfers = transfer_map(orbits)
    print(f'Part 2: {shortest_path(transfers, "YOU", "SAN")}')

if __name__ == '__main__':
    main()
