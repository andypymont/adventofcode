"""
2018 Day 13
https://adventofcode.com/2018/day/13
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import aocd  # type: ignore


@dataclass(frozen=True, order=True)
class Point:
    y_coord: int
    x_coord: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y_coord + other.y_coord, self.x_coord + other.x_coord)


def read_tracks(text: str) -> Dict[Point, "str"]:
    tracks = {}
    lines = text.translate(text.maketrans("^v<>", "||--")).split("\n")
    for y_coord, line in enumerate(lines):
        for x_coord, char in enumerate(line):
            if char in ("|", "-", "\\", "/", "+"):
                tracks[Point(y_coord, x_coord)] = char
    return tracks


UP = Point(-1, 0)
DOWN = Point(1, 0)
LEFT = Point(0, -1)
RIGHT = Point(0, 1)
COMPASS = (UP, RIGHT, DOWN, LEFT)
TURNS = ("left", "ahead", "right")


def turned_direction(direction: Point, change: str) -> Point:
    if change == "ahead":
        return direction
    delta = 1 if change == "right" else -1
    return COMPASS[(COMPASS.index(direction) + delta) % len(COMPASS)]


@dataclass(frozen=True, order=True)
class Minecart:
    position: Point
    direction: Point
    turns: int

    @classmethod
    def create_minecart(cls, y_coord: int, x_coord: int, char: str) -> "Minecart":
        direction = {
            "^": UP,
            "v": DOWN,
            "<": LEFT,
            ">": RIGHT,
        }[char]
        return cls(Point(y_coord, x_coord), direction, 0)

    @property
    def next_turn(self) -> Point:
        return turned_direction(self.direction, TURNS[self.turns % len(TURNS)])

    def next_step(self, track_char: str) -> "Minecart":
        new_dir = self.direction
        turns = self.turns

        if track_char == "\\":
            if self.direction == UP:
                new_dir = LEFT
            elif self.direction == RIGHT:
                new_dir = DOWN
            elif self.direction == DOWN:
                new_dir = RIGHT
            elif self.direction == LEFT:
                new_dir = UP

        elif track_char == "/":
            if self.direction == UP:
                new_dir = RIGHT
            elif self.direction == RIGHT:
                new_dir = UP
            elif self.direction == DOWN:
                new_dir = LEFT
            elif self.direction == LEFT:
                new_dir = DOWN

        elif track_char == "+":
            new_dir = self.next_turn
            turns += 1

        return Minecart(self.position + new_dir, new_dir, turns)


def read_minecarts(text: str) -> List[Minecart]:
    return [
        Minecart.create_minecart(y, x, char)
        for y, line in enumerate(text.split("\n"))
        for x, char in enumerate(line)
        if char in "^v<>"
    ]


def crashes_and_remaining_cart(
    tracks: Dict[Point, "str"], minecarts: List[Minecart]
) -> Tuple[List[Point], Minecart]:
    crashes: List[Point] = []
    while len(minecarts) > 1:
        minecarts = sorted(minecarts)
        crashed_this_turn = set()
        for cart_no, cart in enumerate(minecarts):
            minecarts[cart_no] = cart.next_step(tracks[minecarts[cart_no].position])
            for crash_position in [minecart.position for minecart in minecarts]:
                victims = [
                    victimid
                    for victimid, minecart in enumerate(minecarts)
                    if minecart.position == crash_position
                ]
                if len(victims) > 1:
                    crashed_this_turn.update(victims)
                    crashes.append(minecarts[victims[0]].position)
        minecarts = [
            minecart
            for ix, minecart in enumerate(minecarts)
            if ix not in crashed_this_turn
        ]

    return crashes, minecarts[0]


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=13)
    tracks = read_tracks(data)
    minecarts = read_minecarts(data)
    crashes, cart = crashes_and_remaining_cart(tracks, minecarts)

    print(f"Part 1: {crashes[0].x_coord},{crashes[0].y_coord}")
    print(f"Part 2: {cart.position.x_coord},{cart.position.y_coord}")


if __name__ == "__main__":
    main()
