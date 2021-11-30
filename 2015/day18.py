"""
2015 Day 18
https://adventofcode.com/2015/day/18
"""

from typing import Callable
import numpy as np
import aocd # type: ignore

def load_initial_grid(source: str, fix_corners: bool = False) -> np.ndarray:
    """
    Create the initial grid from the puzzle input.
    """
    lines = source.split('\n')
    if fix_corners:
        lines[0] = '#' + lines[0][1:-1] + '#'
        lines[-1] = '#' + lines[-1][1:-1] + '#'
    return np.array([[1 if char == '#' else 0 for char in line] for line in lines])

def neighbours_on(grid: np.ndarray, y_coord: int, x_coord: int) -> int:
    """
    Return the sum of the neighbours of the given y,x coordinate.
    """
    max_y, max_x = grid.shape
    return grid[
        max(y_coord-1, 0):min(y_coord+2, max_y),
        max(x_coord-1, 0):min(x_coord+2, max_x)
    ].sum()

def new_value(grid: np.ndarray, y_coord: int, x_coord: int) -> int:
    """
    Calculate the new value for the given y,x coordinate.
    """
    neighbours = neighbours_on(grid, y_coord, x_coord)
    if grid[y_coord][x_coord] == 1:
        return 1 if neighbours in (3, 4) else 0
    return 1 if neighbours == 3 else 0

def next_state(
    state: np.ndarray,
    new_val_func: Callable[[np.ndarray, int, int], int] = new_value
) -> np.ndarray:
    """
    Calculate the next state from the current state.
    """
    rows, cols = state.shape
    return np.array([[new_val_func(state, y, x) for x in range(cols)] for y in range(rows)])

def run_steps(
    grid: np.ndarray,
    steps: int,
    new_val_func: Callable[[np.ndarray, int, int], int] = new_value
) -> np.ndarray:
    """
    Run X number of steps and return the result.
    """
    for _ in range(steps):
        grid = next_state(grid, new_val_func)
    return grid

def new_value_broken_light(grid: np.ndarray, y_coord: int, x_coord: int) -> int:
    """
    Calculate the new value for the given y,x coordinate but accounting for the broken
    lights in the corners.
    """
    rows, cols = grid.shape
    if y_coord in (0, rows - 1) and x_coord in (0, cols - 1):
        return 1
    return new_value(grid, y_coord, x_coord)

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=18)

    grid = load_initial_grid(data)
    print(f'Part 1: {run_steps(grid, 100).sum()}')

    grid = load_initial_grid(data, fix_corners=True)
    print(f'Part 2: {run_steps(grid, 100, new_value_broken_light).sum()}')

if __name__ == '__main__':
    main()
