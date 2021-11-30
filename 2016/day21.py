"""
2016 Day 21
https://adventofcode.com/2016/day/21
"""

from itertools import chain, permutations
from typing import Callable, Dict, Sequence, Tuple
import re
import aocd # type: ignore

def swap_position(password: str, args: Sequence[str]) -> str:
    """
    Swap position operation: the sequence 'args' should contain two positions, X and Y. The letters
    at these two positions in the given string will be swapped.
    """
    first, second, *_ = [int(arg) for arg in args]
    if first > second:
        first, second = second, first
    return ''.join(chain(
        password[:first],
        password[second:second+1],
        password[first+1:second],
        password[first:first+1],
        password[second+1:]
    ))

def swap_letter(password: str, args: Sequence[str]) -> str:
    """
    Swap letter operation: the sequence 'args' should contain two letters, X and Y. These letters
    will be swapped with one another wherever they appear in the given string.
    """
    letters: Dict[str, str] = {args[0]: args[1], args[1]: args[0]}
    return ''.join(letters.get(x, x) for x in password)

def reverse_positions(password: str, args: Sequence[str]) -> str:
    """
    Reverse positions operation: the sequence 'args' should contain two indices, X and Y. The
    letters from position X to position Y (inclusive) within the string will be reversed.
    """
    first, second, *_ = [int(arg) for arg in args]
    if first > second:
        first, second = second, first
    return ''.join(chain(password[:first],
                         reversed(password[first:second+1]),
                         password[second+1:]))

def rotate(password: str, args: Sequence[str]) -> str:
    """
    Rotate operation: the sequence 'args' should contain a direction 'left' or 'right', followed by
    a number, X. The whole string will be rotated X steps in the given direction.
    """
    direction = args[0]
    steps = int(args[1])
    return rotate_left(password, steps) if direction == 'left' else rotate_right(password, steps)

def rotate_left(password: str, steps: int) -> str:
    """
    Rotate the string, so each character moves the given number of steps to the left.
    """
    for _ in range(steps):
        password = password[1:] + password[0]
    return password

def rotate_right(password: str, steps: int) -> str:
    """
    Rotate the string, so each character moves the given number of steps to the right.
    """
    for _ in range(steps):
        password = password[-1] + password[:-1]
    return password

def rotate_on_letter(password: str, args: Sequence[str]) -> str:
    """
    Rotate based on letter operation: the sequence 'args' should contain a letter, X. The whole
    string will be rotated to the right based on the index of letter X with in the original string.
    """
    pos = password.find(args[0])
    pos += (1 if pos >= 4 else 0)
    return rotate_right(password, 1 + pos)

def move_position(password: str, args: Sequence[str]) -> str:
    """
    Move position operation: the sequence 'args' should contain two indices, X and Y. The character
    at index X will be removed from the original string and inserted at position Y.
    """
    first, second, *_ = [int(arg) for arg in args]
    removed = password[first]
    without = password[:first] + password[first+1:]
    return without[:second] + removed + without[second:]

RE_SWAP_POSITION = re.compile(r'swap position (\d+) with position (\d+)')
RE_SWAP_LETTER = re.compile(r'swap letter (\w) with letter (\w)')
RE_REVERSE_POSITIONS = re.compile(r'reverse positions (\d+) through (\d+)')
RE_ROTATE = re.compile(r'rotate (left|right) (\d+) step(?:s*)')
RE_ROTATE_ON_LETTER = re.compile(r'rotate based on position of letter (\w)')
RE_MOVE_POSITION = re.compile(r'move position (\d+) to position (\d+)')

ScrambleFunction = Callable[[str, Sequence[str]], str]
actions: Sequence[Tuple[re.Pattern, ScrambleFunction]] = (
    (RE_SWAP_POSITION, swap_position),
    (RE_SWAP_LETTER, swap_letter),
    (RE_REVERSE_POSITIONS, reverse_positions),
    (RE_ROTATE, rotate),
    (RE_ROTATE_ON_LETTER, rotate_on_letter),
    (RE_MOVE_POSITION, move_position),
)

def scramble_password(password: str, instructions: str) -> str:
    """
    Scramble the given password using the given set of instructions.
    """
    for line in instructions.split('\n'):
        for (regex, action) in actions:
            check = regex.search(line)
            if check:
                password = action(password, check.groups())
    return password

def find_password(scrambled: str, instructions: str) -> str:
    """
    Find the original password, given the scrambled output and the set of instructions.
    """
    for possibility in (''.join(poss) for poss in permutations(scrambled)):
        if scramble_password(possibility, instructions) == scrambled:
            return possibility
    return ''

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=21)

    print(f'Part 1: {scramble_password("abcdefgh", data)}')
    print(f'Part 2: {find_password("fbgdceah", data)}')

if __name__ == '__main__':
    main()
