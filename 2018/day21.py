"""
2018 Day 21
https://adventofcode.com/2018/day/21
"""

from typing import Iterator, Optional

# #ip 1
# seti 123 0 5
# bani 5 456 5
# eqri 5 72 5
# addr 5 1 1
# seti 0 0 1
# seti 0 9 5
# bori 5 65536 2
# seti 7571367 9 5
# bani 2 255 4
# addr 5 4 5
# bani 5 16777215 5
# muli 5 65899 5
# bani 5 16777215 5
# gtir 256 2 4
# addr 4 1 1
# addi 1 1 1
# seti 27 1 1
# seti 0 2 4
# addi 4 1 3
# muli 3 256 3
# gtrr 3 2 3
# addr 3 1 1
# addi 1 1 1
# seti 25 6 1
# addi 4 1 4
# seti 17 8 1
# setr 4 6 2
# seti 7 4 1
# eqrr 5 0 4
# addr 4 1 1
# seti 5 5 1

# PSEUDOCODE

#  0 reg5 = 123
#  1 reg5 = reg5 & 456
#  2 reg5 = 1 if reg5 == 72 else 0
#  3 reg1 = reg1 + reg5
#  4 goto 1
#  5 reg5 = 0
#  6 reg2 = reg5 | 65536
#  7 reg5 = 7571367
#  8 reg4 = reg2 & 255
#  9 reg5 = reg5 + reg4
# 10 reg5 = reg5 & 16777215
# 11 reg5 = reg5 * 65899
# 12 reg5 = reg5 & 16777215
# 13 reg4 = 1 if 256 > reg2 else 0
# 14 reg1 = reg1 + reg4
# 15 goto 17
# 16 goto 28
# 17 reg4 = 0
# 18 reg3 = reg4 + 1
# 19 reg3 = reg3 * 256
# 20 reg3 = 1 if reg3 > reg2 else 0
# 21 reg1 = reg1 + reg3
# 22 goto 24
# 23 goto 26
# 24 reg4 = reg4 + 1
# 25 goto 18
# 26 reg2 = reg4
# 27 goto 8
# 28 reg4 = 1 if reg5 == reg0 else 0
# 29 reg1 = reg1 + reg4
# 30 goto 6

# IF STATEMENTS

#  0 reg5 = 123
#  1 reg5 = reg5 & 456
#  3 if reg5 == 72:
#        goto 6
#  4 goto 1
#  5 reg5 = 0
#  6 reg2 = reg5 | 65536
#  7 reg5 = 7571367
#  8 reg4 = reg2 & 255
#  9 reg5 = reg5 + reg4
# 10 reg5 = reg5 & 16777215
# 11 reg5 = reg5 * 65899
# 12 reg5 = reg5 & 16777215
# 14 if 256 > reg2:
#         goto 28
# 17 reg4 = 0
# 18 reg3 = reg4 + 1
# 19 reg3 = reg3 * 256
# 21 if reg3 > reg2:
#         goto 26
# 24 reg4 = reg4 + 1
# 25 goto 18
# 26 reg2 = reg4
# 27 goto 8
# 28 if reg5 == reg0:
#         goto 31
# 30 goto 6

# SIMPLIFY ROUTINES

#  3 while 123 & 456 != 72:
#       pass
#  5 reg5 = 0
#  6 reg2 = reg5 | 65536
#  7 reg5 = 7571367
#  8 reg4 = reg2 & 255
#  9 reg5 = (((reg5 + reg4) & 16777215) * 65899) & 16777215
# 14 if 256 > reg2:
#         goto 28
# 17 reg4 = 0
# 21 if (reg4 + 1) * 256 > reg2:
#         goto 26
# 24 reg4 = reg4 + 1
# 25 goto 21
# 26 reg2 = reg4
# 27 goto 8
# 28 if reg5 == reg0:
#         goto 31
# 30 goto 6

# LOOPS

#    while True:
#  6     reg2 = reg5 | 65536
#  7     reg5 = 7571367
#        while True:
#  8         reg4 = reg2 & 255
#  9         reg5 = (((reg5 + reg4) & 16777215) * 65899) & 16777215
# 14         if 256 > reg2:
# 28             if reg5 == reg0:
#                    return
#            else:
# 26             reg4 = reg4 /= 256

# CONCLUSION:
# A program for Part 1 will just return the first number seen (in reg5) at line 28 - the function
# is below. After seeing the description for part 2, I changed this from *return* to *yield* in
# order to be able to capture both the first and last value.


def activation_system() -> Iterator[int]:
    b = 0
    while True:
        a = b | 65536
        b = 7571367

        while True:
            b = (((b + (a & 255)) & 16777215) * 65899) & 16777215
            if a < 256:
                yield b
                break
            a = a // 256


def last_solution() -> Optional[int]:
    solutions = set()
    prev = None

    for solution in activation_system():
        if solution in solutions:
            return prev

        solutions.add(solution)
        prev = solution

    return None


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    print(f"Part 1: {next(activation_system())}")
    print(f"Part 2: {last_solution()}")


if __name__ == "__main__":
    main()
