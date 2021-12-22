"""
2016 Day 6
https://adventofcode.com/2016/day/6
"""

from typing import Sequence, Tuple
import pandas as pd  # type: ignore
import aocd  # type: ignore


def most_and_least_common(lines: Sequence[str], column: int) -> Tuple[str, str]:
    """
    Calculate the most and least common values in a given column of the input.
    """
    series = pd.Series([line[column] for line in lines])
    return (
        next(series.value_counts().iteritems())[0],
        next(series.value_counts(ascending=True).iteritems())[0],
    )


def assemble_messages(lines: Sequence[str]) -> Tuple[str, str]:
    """
    Assemble the most and least common letters from each column in order to produce two possible
    messages.
    """
    most_and_least = [most_and_least_common(lines, column) for column in range(8)]
    return (
        "".join(most for most, _ in most_and_least),
        "".join(least for _, least in most_and_least),
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2016, day=6)
    most_common, least_common = assemble_messages(data.split("\n"))
    print(f"Part 1: {most_common}")
    print(f"Part 2: {least_common}")


if __name__ == "__main__":
    main()
