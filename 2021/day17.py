"""
2021 Day 17
https://adventofcode.com/2021/day/17
"""

from typing import Dict, Set, Tuple
import aocd  # type: ignore


def read_target(text: str) -> Tuple[int, int, int, int]:
    parts = [
        [int(val) for val in part[2:].split("..")] for part in text[13:].split(", ")
    ]
    return parts[0][0], parts[0][1], parts[1][0], parts[1][1]


def x_hit(velx: int, lowx: int, highx: int) -> bool:
    x = 0
    while velx >= 0:
        if lowx <= x <= highx:
            return True
        x += velx
        velx -= 1
    return False


def shot(velx: int, vely: int, target: Tuple[int, int, int, int]) -> Tuple[bool, int]:
    lowx, highx, lowy, highy = target
    x, y, highpoint = 0, 0, 0
    while x <= highx and y >= lowy:
        if lowx <= x <= highx and lowy <= y <= highy:
            return True, highpoint
        highpoint = y if y > highpoint else highpoint
        x += velx
        y += vely
        velx = 0 if velx == 0 else velx - 1
        vely -= 1
    return False, highpoint


def x_velocities_hitting(lowx: int, highx: int) -> Set[int]:
    return {x for x in range(highx + 1) if x_hit(x, lowx, highx)}


def all_hitting_shots(target: Tuple[int, int, int, int]) -> Dict[Tuple[int, int], int]:
    results = {}
    for velx in x_velocities_hitting(target[0], target[1]):
        for vely in range(target[2], 101):
            hit, height = shot(velx, vely, target)
            if hit:
                results[(velx, vely)] = height
    return results


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert read_target("target area: x=2..10, y=-15..-10") == (2, 10, -15, -10)
    assert read_target("target area: x=20..30, y=-10..-5") == (20, 30, -10, -5)
    assert x_velocities_hitting(20, 30) == {
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
    }
    assert shot(7, 2, (20, 30, -10, -5)) == (True, 3)
    assert shot(6, 3, (20, 30, -10, -5)) == (True, 6)
    assert shot(17, -4, (20, 30, -10, -5)) == (False, 0)
    assert max(all_hitting_shots((20, 30, -10, -5)).values()) == 45


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert set(all_hitting_shots((20, 30, -10, -5))) == {
        (23, -10),
        (25, -9),
        (27, -5),
        (29, -6),
        (22, -6),
        (21, -7),
        (9, 0),
        (27, -7),
        (24, -5),
        (25, -7),
        (26, -6),
        (25, -5),
        (6, 8),
        (11, -2),
        (20, -5),
        (29, -10),
        (6, 3),
        (28, -7),
        (8, 0),
        (30, -6),
        (29, -8),
        (20, -10),
        (6, 7),
        (6, 4),
        (6, 1),
        (14, -4),
        (21, -6),
        (26, -10),
        (7, -1),
        (7, 7),
        (8, -1),
        (21, -9),
        (6, 2),
        (20, -7),
        (30, -10),
        (14, -3),
        (20, -8),
        (13, -2),
        (7, 3),
        (28, -8),
        (29, -9),
        (15, -3),
        (22, -5),
        (26, -8),
        (25, -8),
        (25, -6),
        (15, -4),
        (9, -2),
        (15, -2),
        (12, -2),
        (28, -9),
        (12, -3),
        (24, -6),
        (23, -7),
        (25, -10),
        (7, 8),
        (11, -3),
        (26, -7),
        (7, 1),
        (23, -9),
        (6, 0),
        (22, -10),
        (27, -6),
        (8, 1),
        (22, -8),
        (13, -4),
        (7, 6),
        (28, -6),
        (11, -4),
        (12, -4),
        (26, -9),
        (7, 4),
        (24, -10),
        (23, -8),
        (30, -8),
        (7, 0),
        (9, -1),
        (10, -1),
        (26, -5),
        (22, -9),
        (6, 5),
        (7, 5),
        (23, -6),
        (28, -10),
        (10, -2),
        (11, -1),
        (20, -9),
        (14, -2),
        (29, -7),
        (13, -3),
        (23, -5),
        (24, -8),
        (27, -9),
        (30, -7),
        (28, -5),
        (21, -10),
        (7, 9),
        (6, 6),
        (21, -5),
        (27, -10),
        (7, 2),
        (30, -9),
        (21, -8),
        (22, -7),
        (24, -9),
        (20, -6),
        (6, 9),
        (29, -5),
        (8, -2),
        (27, -8),
        (30, -5),
        (24, -7),
    }


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=17)
    target = read_target(data)

    shots = all_hitting_shots(target)
    print(f"Part 1: {max(shots.values())}")
    print(f"Part 2: {len(shots)}")


if __name__ == "__main__":
    main()
