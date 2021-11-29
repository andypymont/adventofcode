"""
2018 Day 18
https://adventofcode.com/2018/day/18
"""

from typing import Dict, Optional, Tuple
import aocd # type: ignore

OPEN = '.'
TREES = '|'
LUMBERYARD = '#'

AdjacencyMap = Dict[int, Tuple[int, ...]]
Cycle = Tuple[int, int]

def read_input(text: str) -> Tuple[int, str]:
    lines = text.split('\n')
    size = len(lines)
    return (size, ''.join(lines))

def adjacency_map(size: int) -> AdjacencyMap:
    adj_map = {}

    limit = size**2

    for pos in range(limit):
        x_pos = pos % size
        left = (pos - size - 1, pos - 1, pos + size - 1) if x_pos > 0 else tuple()
        right = (pos - size + 1, pos + 1, pos + size + 1) if x_pos < (size - 1) else tuple()
        vert = (pos - size, pos + size)

        adj_map[pos] = tuple(p for p in left+right+vert if 0 < p < limit)

    return adj_map

def new_char(area: str, pos: int, adj_map: AdjacencyMap) -> str:
    adj_trees = 0
    adj_lumberyards = 0

    for adj in adj_map[pos]:
        if area[adj] == TREES:
            adj_trees += 1
        elif area[adj] == LUMBERYARD:
            adj_lumberyards += 1

    char = area[pos]

    if char == OPEN:
        return TREES if adj_trees >= 3 else OPEN
    if char == TREES:
        return LUMBERYARD if adj_lumberyards >= 3 else TREES

    return LUMBERYARD if adj_trees > 0 and adj_lumberyards > 0 else OPEN

def next_state(state: str, adj_map: AdjacencyMap) -> str:
    return ''.join(new_char(state, pos, adj_map) for pos in range(len(state)))

def calculate_simulation_cycle(state: str, adj_map: AdjacencyMap) -> Cycle:
    minute = 0

    cache = {}
    cache[state] = minute

    while True:
        minute += 1
        state = next_state(state, adj_map)
        if state in cache:
            return (cache[state], minute)
        cache[state] = minute

def simulate(state: str, adj_map: AdjacencyMap, minutes: int, cycle: Optional[Cycle] = None) -> str:
    if cycle:
        start, end = cycle
        length = end - start

        if minutes > start:
            minutes = start + ((minutes - start) % length)

    for _ in range(minutes):
        state = next_state(state, adj_map)
    return state

def resource_value(state: str) -> int:
    wooded = sum(1 for char in state if char == TREES)
    lyards = sum(1 for char in state if char == LUMBERYARD)
    return wooded * lyards

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=18)
    size, initial_state = read_input(data)
    adj_map = adjacency_map(size)
    cycle = calculate_simulation_cycle(initial_state, adj_map)

    part1 = resource_value(simulate(initial_state, adj_map, 10))
    print(f'Part 1: {part1}')

    part2 = resource_value(simulate(initial_state, adj_map, 1_000_000_000, cycle))
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
