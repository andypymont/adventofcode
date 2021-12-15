"""
2021 Day 15
https://adventofcode.com/2021/day/15
"""

from heapq import heappop, heappush
from typing import Tuple
import aocd # type: ignore
import numpy as np

def read_map(text: str) -> np.ndarray:
    return np.array([list(line) for line in text.split('\n')], int)

MAX_INT = np.iinfo(np.int64).max

def lowest_risk_path(risk_map: np.ndarray, initial: Tuple[int, int] = (0, 0)) -> float:
    max_y = risk_map.shape[0] - 1
    max_x = risk_map.shape[1] - 1
    risks = np.ones_like(risk_map) * MAX_INT
    risks[initial] = 0
    queue = [(0, initial)]

    while queue:
        current_risk, current_pos = heappop(queue)

        if current_pos == (max_y, max_x):
            return current_risk

        if current_risk > risks[current_pos]:
            continue

        y, x = current_pos
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            ny, nx = y + dy, x + dx
            if 0 <= ny <= max_y and 0 <= nx <= max_x:
                risk = current_risk + risk_map[ny, nx]
                if risk < risks[ny, nx]:
                    risks[ny, nx] = risk
                    heappush(queue, (risk, (ny, nx)))

    return -1

def increment(risk_map: np.ndarray, increment_by: int) -> np.ndarray:
    incremented = risk_map + increment_by
    while (incremented > 9).any():
        incremented[incremented > 9] -= 9
    return incremented

def extend_risk_map(risk_map: np.ndarray) -> np.ndarray:
    increments = [
        [0, 1, 2, 3, 4],
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8],
    ]
    return np.block([[increment(risk_map, value) for value in row] for row in increments])

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    risk_map = np.array([
        [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
        [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
        [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
        [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
        [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
        [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
        [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
        [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
        [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
        [2, 3, 1, 1, 9, 4, 4, 5, 8, 1],
    ])
    assert (read_map('\n'.join((
        '1163751742',
        '1381373672',
        '2136511328',
        '3694931569',
        '7463417111',
        '1319128137',
        '1359912421',
        '3125421639',
        '1293138521',
        '2311944581',
    ))) == risk_map).all()
    assert lowest_risk_path(risk_map) == 40

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    risk_map = np.array([
        [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
        [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
        [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
        [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
        [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
        [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
        [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
        [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
        [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
        [2, 3, 1, 1, 9, 4, 4, 5, 8, 1],
    ])
    extended = extend_risk_map(risk_map)
    assert extended.shape == (50, 50)
    assert extended[1, 2] == 8
    assert extended[1, 12] == 9
    assert extended[1, 22] == 1
    assert extended[1, 32] == 2
    assert extended[1, 42] == 3
    assert extended[11, 2] == 9
    assert extended[11, 12] == 1
    assert extended[11, 22] == 2
    assert extended[11, 32] == 3
    assert extended[11, 42] == 4
    assert extended[41, 42] == 7
    assert lowest_risk_path(extended) == 315

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=15)

    risk_map = read_map(data)
    print(f'Part 1: {lowest_risk_path(risk_map)}')

    extended = extend_risk_map(risk_map)
    print(f'Part 2: {lowest_risk_path(extended)}')

if __name__ == '__main__':
    main()
