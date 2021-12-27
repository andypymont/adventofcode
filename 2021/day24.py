"""
2021 Day 24
https://adventofcode.com/2021/day/24
"""

from collections import deque
from typing import List, Set, Tuple
import aocd  # type: ignore

# Finding the (mostly) repeated pattern in the input program:

# 01        02          03          04          05          06          07
# inp w     inp w       inp w       inp w       inp w       inp w       inp w
# mul x 0   mul x 0     mul x 0     mul x 0     mul x 0     mul x 0     mul x 0
# add x z   add x z     add x z     add x z     add x z     add x z     add x z
# mod x 26  mod x 26    mod x 26    mod x 26    mod x 26    mod x 26    mod x 26
# div z 1   div z 1     div z 1     div z 26    div z 1     div z 26    div z 1
# add x 12  add x 10    add x 10    add x -6    add x 11    add x -12   add x 11
# eql x w   eql x w     eql x w     eql x w     eql x w     eql x w     eql x w
# eql x 0   eql x 0     eql x 0     eql x 0     eql x 0     eql x 0     eql x 0
# mul y 0   mul y 0     mul y 0     mul y 0     mul y 0     mul y 0     mul y 0
# add y 25  add y 25    add y 25    add y 25    add y 25    add y 25    add y 25
# mul y x   mul y x     mul y x     mul y x     mul y x     mul y x     mul y x
# add y 1   add y 1     add y 1     add y 1     add y 1     add y 1     add y 1
# mul z y   mul z y     mul z y     mul z y     mul z y     mul z y     mul z y
# mul y 0   mul y 0     mul y 0     mul y 0     mul y 0     mul y 0     mul y 0
# add y w   add y w     add y w     add y w     add y w     add y w     add y w
# add y 6   add y 2     add y 13    add y 8     add y 13    add y 13    add y 3
# mul y x   mul y x     mul y x     mul y x     mul y x     mul y x     mul y x
# add z y   add z y     add z y     add z y     add z y     add z y     add z y

# 08        09          10          11          12          13          14
# inp w     inp w       inp w       inp w       inp w       inp w       inp w
# mul x 0   mul x 0     mul x 0     mul x 0     mul x 0     mul x 0     mul x 0
# add x z   add x y     add x z     add x z     add x z     add x z     add x z
# mod x 26  mod x 26    mod x 26    mod x 26    mod x 26    mod x 26    mod x 26
# div z 1   div z 1     div z 26    div z 26    div z 26    div z 26    div z 26
# add x 12  add x 12    add x -2    add x -5    add x -4    add x -4    add x -12
# eql x w   eql x w     eql x w     eql x w     eql x w     eql x w     eql x w
# eql x 0   eql x 0     eql x 0     eql x 0     eql x 0     eql x 0     eql x 0
# mul y 0   mul y 0     mul y 0     mul y 0     mul y 0     mul y 0     mul y 0
# add y 25  add y 25    add y 25    add y 25    add y 25    add y 25    add y 25
# mul y x   mul y x     mul y x     mul y x     mul y x     mul y x     mul y x
# add y 1   add y 1     add y 1     add y 1     add y 1     add y 1     add y 1
# mul z y   mul z y     mul z y     mul z y     mul z y     mul z y     mul z y
# mul y 0   mul y 0     mul y 0     mul y 0     mul y 0     mul y 0     mul y 0
# add y w   add y w     add y w     add y w     add y w     add y w     add y w
# add y 11  add y 10    add y 8     add y 14    add y 6     add y 8     add y 2
# mul y x   mul y x     mul y x     mul y x     mul y x     mul y x     mul y x
# add z y   add z y     add z y     add z y     add z y     add z y     add z y

# There are two variations:

# Variation A:
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x VAR1
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y VAR2
# mul y x
# add z y

# In this variation, VAR1 is always >=10, therefore it always results in x = 1:
# mul x 0       x = 0
# add x z       x = z
# mod x 26      x = x % 26
# div z 1
# add x 10      x = (x % 26) + 10
# eql x w       [2-digit number] == [1-digit number] - always False, therefore x = 0
# eql x 0       x = 1
# This results in the stored 'z' value being multiplied by 26 and the new number (INP + VAR2) being
# added to it.

# Variation B:
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x VAR1
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y VAR2
# mul y x
# add z y

# In this variation, VAR1 is negative and the existing z value is divided by 26 on the 5th line.
# There are two possibilities - the value of z % 26 calculated on line 4 and then removed from the
# z-total on line 5 is either equal to -VAR1 or it is not.

#               MATCHED                                     NOT MATCHED
# inp w         w = INP                                     w = INP
# mul x 0       x = 0                                       x = 0
# add x z       x = z                                       x = z
# mod x 26      x = z % 26                                  x = z % 26
# div z 26      z //= 26                                    z //= 26
# add x VAR1    x = (z % 26) + VAR1                         x = (z % 26) + VAR1
# eql x w       x = 1 if (z % 26) + VAR1 == INP else 0      x = 1 if (z % 26) + VAR1 == INP else 0
# eql x 0       x = 0                                       x = 1
# mul y 0       y = 0                                       y = 0
# add y 25      y = 25                                      y = 25
# mul y x       y = 0                                       y = 25
# add y 1       y = 1                                       y = 26
# mul z y       z *= 1                                      z *= 26
# mul y 0       y = 0                                       y = 0
# add y w       y = INP                                     y = INP
# add y VAR2    y = INP + VAR2                              y = INP + VAR2
# mul y x       y = 0                                       y = (INP + VAR2)
# add z y       z += 0                                      z += (INP + VAR2)

# If we want to aim for a z value of 0 at the program's conclusion, we need to avoid the VAR2 value
# being added to z, therefore we need the z % 26 value to match -VAR1. This will be a value added
# on during the most recent 'Variation A' cycle which hasn't yet been examined by a Variation B
# cycle.

# Therefore to disentangle values which produce z == 0:
# - Create an empty queue to represent (base-26) values sent to z
# - Iterate through each cycle's values for VAR1, VAR2 and the line-5 divisor:
# ----- If the line-5 divisor is 1, it's variation A: add (IMP + VAR2) to the z-queue
# ----- If the line-5 divisor is 26, it's variation B: pop from the queue and require the result +
#       VAR1 to equal INP.


def match_requirements(program: str) -> Set[Tuple[int, int, int]]:
    queue: deque[Tuple[int, int]] = deque()
    reqs: List[Tuple[int, int, int]] = []
    lines = [line.split(" ") for line in program.split("\n")]

    for prog_start in range(0, len(lines), 18):
        var1 = int(lines[prog_start + 5][2])
        var2 = int(lines[prog_start + 15][2])

        if lines[prog_start + 4][2] == "1":
            queue.append((prog_start // 18, var2))
        else:
            added, added_diff = queue.pop()
            reqs.append((added, prog_start // 18, added_diff + var1))

    return set(reqs)


def highest_valid_number(reqs: Set[Tuple[int, int, int]]) -> int:
    digits = [9 for _ in range(14)]
    for first, second, delta in reqs:
        higher, lower, gap = (
            (second, first, delta) if delta >= 0 else (first, second, -delta)
        )
        digits[lower] = digits[higher] - gap
    return int("".join(str(d) for d in digits))


def lowest_valid_number(reqs: Set[Tuple[int, int, int]]) -> int:
    digits = [1 for _ in range(14)]
    for first, second, delta in reqs:
        higher, lower, gap = (
            (second, first, delta) if delta >= 0 else (first, second, -delta)
        )
        digits[higher] = digits[lower] + gap
    return int("".join(str(d) for d in digits))


def test_part1() -> None:
    """
    Testing the functions for part 1.
    """
    program = ["mul w 0" for _ in range(72)]
    # Add IMP + 6 to the queue
    program[4] = "div z 1"
    program[5] = "add x 2"
    program[15] = "add y 6"
    # Add IMP + 2 to the queue
    program[22] = "div z 1"
    program[23] = "add x 10"
    program[33] = "add y 2"
    # Remove the second added value above and expect it -6 to equal IMP.
    program[40] = "div z 26"
    program[41] = "add x -6"
    program[51] = "add y 8"
    # Remove the first added value above and expect it -1 to equal IMP.
    program[58] = "div z 26"
    program[59] = "add x -1"
    program[60] = "add y 13"

    reqs = {
        (0, 3, 5),
        (1, 2, -4),
    }
    assert match_requirements("\n".join(program)) == reqs
    assert highest_valid_number(reqs) == 49_599_999_999_999


def test_part2() -> None:
    """
    Testing the functions for part 2.
    """
    reqs = {
        (0, 3, 5),
        (1, 2, -4),
    }
    assert lowest_valid_number(reqs) == 15_161_111_111_111


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=24)
    reqs = match_requirements(data)

    print(f"Part 1: {highest_valid_number(reqs)}")
    print(f"Part 2: {lowest_valid_number(reqs)}")


if __name__ == "__main__":
    main()
