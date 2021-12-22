"""
2016 Day 2
https://adventofcode.com/2016/day/2
"""

from typing import Dict, Sequence, Union
import aocd  # type: ignore

Key = Union[str, bool]
Keypad = Sequence[Sequence[Key]]


def key_in_direction(start: Key, direction: str, keypad: Keypad) -> Key:
    """
    Return the value of the key in the given direction.
    """
    row = next(r for r in keypad if start in r)
    x_pos = row.index(start)
    col = [c[x_pos] for c in keypad]
    y_pos = col.index(start)

    directions: Dict[str, Key] = {
        "U": col[max(0, y_pos - 1)],
        "D": col[min(y_pos + 1, len(col) - 1)],
        "L": row[max(0, x_pos - 1)],
        "R": row[min(x_pos + 1, len(row) - 1)],
    }

    return directions[direction] or start


def passcode_from_directions(directions: str, keypad: Keypad) -> str:
    """
    Calculate the passcode, given the directions and the relevant keypad.
    """
    passcode = ""
    position: Key = "5"

    for line in directions.split("\n"):
        if line:
            for direction in line:
                position = key_in_direction(position, direction, keypad)
            passcode += str(position)

    return passcode


KEYPAD_PART_ONE: Keypad = (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "9"))
KEYPAD_PART_TWO: Keypad = (
    (False, False, "1", False, False),
    (False, "2", "3", "4", False),
    ("5", "6", "7", "8", "9"),
    (False, "A", "B", "C", False),
    (False, False, "D", False, False),
)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=2)

    print(f"Part 1: {passcode_from_directions(data, KEYPAD_PART_ONE)}")
    print(f"Part 2: {passcode_from_directions(data, KEYPAD_PART_TWO)}")


if __name__ == "__main__":
    main()
