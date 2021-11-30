"""
2015 Day 6
https://adventofcode.com/2015/day/6
"""

from typing import Callable, Iterable, Tuple
import aocd # type: ignore
import numpy as np

def empty_grid() -> np.ndarray:
    """"
    Create an empty 1000 by 1000 array of zeroes.
    """
    return np.zeros((1000, 1000), dtype=int, order='C')

def act(
    grid: np.ndarray,
    func: Callable[[np.ndarray], np.ndarray],
    top_left: Tuple[int, int],
    bottom_right: Tuple[int, int]) -> None:
    """
    Apply the given function to every cell in the given grid that is in the rectangular region
    defined by the given top-left and bottom-right coordinates.
    """
    min_x, min_y = top_left
    max_x, max_y = bottom_right
    grid[min_y:(max_y+1), min_x:(max_x+1)] = func(grid[min_y:(max_y+1), min_x:(max_x+1)])

@np.vectorize
def turned_on(_: int) -> int:
    """
    Turn on all cells in the region, i.e. set to 1.
    """
    return 1

@np.vectorize
def turned_off(_: int) -> int:
    """
    Turn off all cells in the region, i.e. set to 0.
    """
    return 0

@np.vectorize
def toggled(value: int) -> int:
    """
    Toggle all cells in the region.
    """
    return 1 - value

def read_coords(coords: str) -> Tuple[int, int]:
    """
    Translate a string in the format 'X,Y' into a tuple containing integers X and Y.
    """
    split_coords = [int(i) for i in coords.split(',')]

    x_coord = 0 if len(split_coords) == 0 else split_coords[0]
    y_coord = 0 if len(split_coords) <= 1 else split_coords[1]

    return (x_coord, y_coord)

def process_instructions(
    instructions: Iterable[str],
    on_func: Callable[[np.ndarray], np.ndarray] = turned_on,
    off_func: Callable[[np.ndarray], np.ndarray] = turned_off,
    toggle_func: Callable[[np.ndarray], np.ndarray] = toggled
    ) -> int:
    """
    Begin with an empty grid, run through the provided set of instructions using the provided
    vectorized functions, and return the total of the values in the modified grid.
    """
    grid = empty_grid()

    for instruction in instructions:
        words = instruction.split()
        if words[0] == 'turn' and words[1] == 'on':
            act(grid, on_func, read_coords(words[2]), read_coords(words[4]))
        elif words[0] == 'turn' and words[1] == 'off':
            act(grid, off_func, read_coords(words[2]), read_coords(words[4]))
        elif words[0] == 'toggle':
            act(grid, toggle_func, read_coords(words[1]), read_coords(words[3]))

    return np.sum(grid)

def test_part1():
    """
    Examples for Part 1.
    """
    grid = empty_grid()
    assert np.sum(grid) == 0
    act(grid, turned_on, (0, 0), (999, 999))
    assert np.sum(grid) == 1_000_000
    act(grid, toggled, (0, 0), (999, 0))
    assert np.sum(grid) == 999_000
    act(grid, turned_off, (499, 499), (500, 500))
    assert np.sum(grid) == 998_996
    assert process_instructions((
        'turn on 0,0 through 999,999',
        'toggle 0,0 through 999,0',
        'turn off 499,499 through 500,500'
    )) == 998_996

@np.vectorize
def turn_up(value: int) -> int:
    """
    Turn up cells in the given region, i.e. increase brightness by 1.
    """
    return value + 1

@np.vectorize
def turn_down(value: int) -> int:
    """
    Turn down cells in the given region, i.e. decrease brightness by 1.
    """
    return 0 if value == 0 else value - 1

@np.vectorize
def turn_up_twice(value: int) -> int:
    """
    Turn up cells in the given region twice, i.e. increase brightness by 2.
    """
    return value + 2

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=6)
    all_instructions = data.split('\n')

    print(f'Part 1: {process_instructions(all_instructions)}')
    print(f'Part 2: {process_instructions(all_instructions, turn_up, turn_down, turn_up_twice)}')

if __name__ == '__main__':
    main()
