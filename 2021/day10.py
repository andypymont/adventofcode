"""
2021 Day 10
https://adventofcode.com/2021/day/10
"""

from collections import deque
from enum import Enum
from functools import reduce
from typing import Dict, Tuple
from numpy import median
import aocd  # type: ignore


class ErrorType(Enum):
    INCOMPLETE = 0
    CORRUPTED = 1


BRACKETS: Dict[str, str] = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def error_on_line(line: str) -> Tuple[ErrorType, str]:
    chunks: deque[str] = deque()
    for char in line:
        if char in BRACKETS:
            chunks.appendleft(char)
        elif len(chunks) == 0:
            return (ErrorType.CORRUPTED, char)
        elif char != BRACKETS[chunks.popleft()]:
            return (ErrorType.CORRUPTED, char)
    return (ErrorType.INCOMPLETE, "".join(BRACKETS[char] for char in chunks))


CORRUPT_ERROR_VALUES: Dict[str, int] = {
    "": 0,
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def total_corrupted_errors(subsystem: str) -> int:
    return sum(
        CORRUPT_ERROR_VALUES[char]
        for errortype, char in [error_on_line(line) for line in subsystem.split("\n")]
        if errortype == ErrorType.CORRUPTED
    )


INCOMPLETE_ERROR_VALUES: Dict[str, int] = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def incomplete_error_score(brackets: str) -> int:
    return reduce(
        lambda total, bracket: (total * 5) + INCOMPLETE_ERROR_VALUES[bracket],
        brackets,
        0,
    )


def median_incomplete_error(subsystem: str) -> int:
    return int(
        median(
            [
                incomplete_error_score(brackets)
                for errortype, brackets in [
                    error_on_line(line) for line in subsystem.split("\n")
                ]
                if errortype == ErrorType.INCOMPLETE
            ]
        )
    )


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert error_on_line("{([(<{}[<>[]}>{[]{[(<()>") == (ErrorType.CORRUPTED, "}")
    assert error_on_line("[[<[([]))<([[{}[[()]]]") == (ErrorType.CORRUPTED, ")")
    assert error_on_line("[{[{({}]{}}([{[{{{}}([]") == (ErrorType.CORRUPTED, "]")
    assert error_on_line("[<(<(<(<{}))><([]([]()") == (ErrorType.CORRUPTED, ")")
    assert error_on_line("<{([([[(<>()){}]>(<<{{") == (ErrorType.CORRUPTED, ">")
    assert (
        total_corrupted_errors(
            "\n".join(
                (
                    "[({(<(())[]>[[{[]{<()<>>",
                    "[(()[<>])]({[<{<<[]>>(",
                    "{([(<{}[<>[]}>{[]{[(<()>",
                    "(((({<>}<{<{<>}{[]{[]{}",
                    "[[<[([]))<([[{}[[()]]]",
                    "[{[{({}]{}}([{[{{{}}([]",
                    "{<[[]]>}<{[{[{[]{()[[[]",
                    "[<(<(<(<{}))><([]([]()",
                    "<{([([[(<>()){}]>(<<{{",
                    "<{([{{}}[<[[[<>{}]]]>[]]",
                )
            )
        )
        == 26397
    )


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert error_on_line("[({(<(())[]>[[{[]{<()<>>") == (
        ErrorType.INCOMPLETE,
        "}}]])})]",
    )
    assert error_on_line("[(()[<>])]({[<{<<[]>>(") == (ErrorType.INCOMPLETE, ")}>]})")
    assert error_on_line("(((({<>}<{<{<>}{[]{[]{}") == (
        ErrorType.INCOMPLETE,
        "}}>}>))))",
    )
    assert error_on_line("{<[[]]>}<{[{[{[]{()[[[]") == (
        ErrorType.INCOMPLETE,
        "]]}}]}]}>",
    )
    assert error_on_line("<{([{{}}[<[[[<>{}]]]>[]]") == (ErrorType.INCOMPLETE, "])}>")
    assert incomplete_error_score("])}>") == 294
    assert incomplete_error_score("}}]])})]") == 288957
    assert incomplete_error_score(")}>]})") == 5566
    assert incomplete_error_score("}}>}>))))") == 1480781
    assert incomplete_error_score("]]}}]}]}>") == 995444
    assert incomplete_error_score("])}>") == 294
    assert (
        median_incomplete_error(
            "\n".join(
                (
                    "[({(<(())[]>[[{[]{<()<>>",
                    "[(()[<>])]({[<{<<[]>>(",
                    "{([(<{}[<>[]}>{[]{[(<()>",
                    "(((({<>}<{<{<>}{[]{[]{}",
                    "[[<[([]))<([[{}[[()]]]",
                    "[{[{({}]{}}([{[{{{}}([]",
                    "{<[[]]>}<{[{[{[]{()[[[]",
                    "[<(<(<(<{}))><([]([]()",
                    "<{([([[(<>()){}]>(<<{{",
                    "<{([{{}}[<[[[<>{}]]]>[]]",
                )
            )
        )
        == 288957
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=10)

    print(f"Part 1: {total_corrupted_errors(data)}")
    print(f"Part 2: {median_incomplete_error(data)}")


if __name__ == "__main__":
    main()
