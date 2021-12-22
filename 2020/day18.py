"""
2020 Day 18
https://adventofcode.com/2020/day/18
"""
from math import prod
from operator import add, mul
from typing import Optional, Union
import re
import aocd  # type: ignore

re_brackets = re.compile(r"\(([\d\s\*\+]+)\)")


def new_math(expression: str) -> int:
    match: Union[bool, Optional[re.Match[str]]] = True
    while match:
        match = re_brackets.search(expression)
        if match:
            start, end = match.span()
            expression = (
                expression[:start]
                + str(new_math(expression[start + 1 : end - 1]))
                + expression[end:]
            )

    value = 0
    operator = add

    for item in expression.split(" "):
        if item == "+":
            operator = add
        elif item == "*":
            operator = mul
        else:
            value = operator(value, int(item))
    return value


def new_new_math(expression: str) -> int:
    match: Union[bool, Optional[re.Match[str]]] = True
    while match:
        match = re_brackets.search(expression)
        if match:
            start, end = match.span()
            expression = (
                expression[:start]
                + str(new_new_math(expression[start + 1 : end - 1]))
                + expression[end:]
            )

    if "*" in expression:
        return prod(
            new_new_math(subexpression) for subexpression in expression.split(" * ")
        )

    if "+" in expression:
        return sum(
            new_new_math(subexpression) for subexpression in expression.split(" + ")
        )

    return int(expression)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=18)
    lines = data.split("\n")

    print(f"Part 1: {sum(new_math(line) for line in lines)}")
    print(f"Part 2: {sum(new_new_math(line) for line in lines)}")


if __name__ == "__main__":
    main()
