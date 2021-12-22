"""
2018 Day 19
https://adventofcode.com/2018/day/19
"""

# #ip 1
# addi 1 16 1
# seti 1 1 5
# seti 1 4 2
# mulr 5 2 3
# eqrr 3 4 3
# addr 3 1 1
# addi 1 1 1
# addr 5 0 0
# addi 2 1 2
# gtrr 2 4 3
# addr 1 3 1
# seti 2 7 1
# addi 5 1 5
# gtrr 5 4 3
# addr 3 1 1
# seti 1 8 1
# mulr 1 1 1
# addi 4 2 4
# mulr 4 4 4
# mulr 1 4 4
# muli 4 11 4
# addi 3 1 3
# mulr 3 1 3
# addi 3 3 3
# addr 4 3 4
# addr 1 0 1
# seti 0 3 1
# setr 1 1 3
# mulr 3 1 3
# addr 1 3 3
# mulr 1 3 3
# muli 3 14 3
# mulr 3 1 3
# addr 4 3 4
# seti 0 9 0
# seti 0 4 1

# PSUEDOCODE:

#  0 goto 17
#  1 reg5 = 1
#  2 reg2 = 1
#  3 reg3 = reg2 * reg5
#  4 reg3 = 1 if reg3 == reg4 else 0
#  5 reg1 = reg1 + reg3
#  6 goto 8
#  7 reg0 = reg0 + reg5
#  8 reg2 = reg2 + 1
#  9 reg3 = 1 if reg2 > reg4 else 0
# 10 reg1 = reg1 + reg3
# 11 goto 3
# 12 reg5 = reg5 + 1
# 13 reg3 = 1 if reg5 > reg4 else 0
# 14 reg1 = reg1 + reg3
# 15 goto 2
# 16 goto 257
# 17 reg4 = reg4 + 2
# 18 reg4 = reg4 * reg4
# 19 reg4 = reg4 * 19
# 20 reg4 = reg4 * 11
# 21 reg3 = reg3 + 1
# 22 reg3 = reg3 * 22
# 23 reg3 = reg3 + 3
# 24 reg4 = reg4 + reg3
# 25 reg1 = reg1 + reg0
# 26 goto 1
# 27 reg3 = 27
# 28 reg3 = reg3 * 28
# 29 reg3 = reg3 + 29
# 30 reg3 = reg3 * 30
# 31 reg3 = reg3 * 14
# 32 reg3 = reg3 * 32
# 33 reg4 = reg4 + reg3
# 34 reg0 = 0
# 35 goto 1

# IF-THEN-GOTOS:

#  0 goto 17
#  1 reg5 = 1
#  2 reg2 = 1
#  3
#  4 reg3 = 1 if (reg2 * reg5) == reg4 else 0
#  5 if reg3 == 1 then goto 7
#  6 goto 8
#  7 reg0 = reg0 + reg5
#  8 reg2 = reg2 + 1
#  9 reg3 = 1 if reg2 > reg4 else 0
# 10 if reg3 == 1 then goto 12
# 11 goto 3
# 12 reg5 = reg5 + 1
# 13 reg3 = 1 if reg5 > reg4 else 0
# 14 if reg3 == 1 then goto 16
# 15 goto 2
# 16 goto 257
# 17 reg4 = reg4 + 2
# 18 reg4 = reg4 * reg4
# 19 reg4 = reg4 * 19
# 20 reg4 = reg4 * 11
# 21 reg3 = reg3 + 1
# 22 reg3 = reg3 * 22
# 23 reg3 = reg3 + 3
# 24 reg4 = reg4 + reg3
# 25 if reg0 == 1 then goto 27
# 26 goto 1
# 27 reg3 = 27
# 28 reg3 = reg3 * 28
# 29 reg3 = reg3 + 29
# 30 reg3 = reg3 * 30
# 31 reg3 = reg3 * 14
# 32 reg3 = reg3 * 32
# 33 reg4 = reg4 + reg3
# 34 reg0 = 0
# 35 goto 1

# SIMPLIFY ROUTINES:

#  0 goto 17
#  1 reg5 = 1
#  2 reg2 = 1
#  3
#  4 reg3 = 1 if (reg2 * reg5) == reg4 else 0
#  5 if reg3 == 1 then goto 7
#  6 goto 8
#  7 reg0 = reg0 + reg5
#  8 reg2 = reg2 + 1
#  9 reg3 = 1 if reg2 > reg4 else 0
# 10 if reg3 == 1 then goto 12
# 11 goto 3
# 12 reg5 = reg5 + 1
# 13 reg3 = 1 if reg5 > reg4 else 0
# 14 if reg3 == 1 then goto 16
# 15 goto 2
# 16 goto 257
# 17
# 18
# 19
# 20 reg4 = ((reg4 + 2)**2) * 19 * 11
# 21
# 22
# 23 reg3 = ((reg3 + 1) * 22) + 3
# 24 reg4 = reg4 + reg3
# 25 if reg0 == 1 then goto 27
# 26 goto 1
# 27
# 28
# 29
# 30
# 31
# 32 reg3 = ((27 * 28) + 29) * 30 * 14 * 32
# 33 reg4 = reg4 + reg3
# 34 reg0 = 0
# 35 goto 1

# RE-ORDER, TIDY UP, ADD IF STATEMENTS

# 24 reg4 = 10_551_261 if reg0 == 1 else 861
# 34 reg0 = 0

#  1 reg5 = 1
#  2 reg2 = 1
#  5 if (reg2 * reg5) == reg4:
#  7     reg0 = reg0 + reg5
#  8 reg2 = reg2 + 1
# 10 if reg2 > reg4 then goto 12
# 11 goto 5
# 12 reg5 = reg5 + 1
# 14 if (reg5 > reg4):
# 16     return reg0
# 15 goto 2

# ADD LOOPS:

# reg4 = 10_551_261 if reg0 == 1 else 861
# reg0 = 0

#  for reg5 in range(1, reg4):
#      for reg2 in range(1, reg4):
#          if (reg2 * reg5) == reg4:
#              reg0 = reg0 + reg5
# return reg0

# CONCLUSION:

# This is a program which finds the sum of the factors of either a large or an extremely large
# number.


def sum_of_factors(target: int) -> int:
    return target + sum(
        divisor for divisor in range(1, target // 2) if target % divisor == 0
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    # data = aocd.get_data(year=2018, day=19)
    targets = (
        861,
        10_551_261,
    )

    print(f"Part 1: {sum_of_factors(targets[0])}")
    print(f"Part 2: {sum_of_factors(targets[1])}")


if __name__ == "__main__":
    main()
