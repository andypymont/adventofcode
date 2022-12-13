"""
2022 Day 13
https://adventofcode.com/2022/day/13
"""

from functools import reduce
from operator import add
from typing import Any, Iterator
import json
import aocd  # type: ignore

Pair = tuple[Any, Any]


def read_pair(text: str) -> Pair:
    """
    Read a single pair of signals from the puzzle input.
    """
    pair = [json.loads(line) for line in text.split("\n")]
    return pair[0], pair[1]


def read_pairs(text: str) -> tuple[Pair, ...]:
    """
    Read all of the pairs of signals from the puzzle input.
    """
    return tuple(read_pair(pair) for pair in text.split("\n\n"))


def compare_signals(first: Any, second: Any) -> int:
    """
    Comparison function (for use in sorting) for two signals: return -1, 0, or 1 by comparing them.

    If both values are integers, the lower integer is lower.

    If both values are lists, compare the first value of each list, then the second value, and so
    on. If the left list runs out of items first, it is lower.

    If exactly one value is an integer, convert the integer to a list which contains that integer
    as its only value, then retry the comparison.
    """
    if isinstance(first, int) and isinstance(second, int):
        return 0 if first == second else -1 if first < second else 1

    first = [first] if isinstance(first, int) else first
    second = [second] if isinstance(second, int) else second

    for index, one in enumerate(first):
        if index >= len(second):
            return 1

        two = second[index]
        if (comparison := compare_signals(one, two)) != 0:
            return comparison

    return -1 if len(first) < len(second) else 0


def pairs_in_right_order(pairs: tuple[Pair, ...]) -> Iterator[int]:
    """
    From the given set of pairs, yield the index (first item = 1) for each pair which is already in
    ascending order.
    """
    for index, pair in enumerate(pairs):
        if compare_signals(*pair) <= 0:
            yield index + 1


def all_packets(pairs: tuple[Pair, ...]) -> tuple[Any, ...]:
    """
    Concatenate the given set of pairs into a single iterable containing all of the packets.
    """
    return reduce(add, pairs)


def divide_packets(packets: tuple[Any, ...]) -> tuple[int, int, int]:
    """
    Using the divider packets [[2]] and [[6]], divide up the given set of packets into three
    separate sections: less than the lower-divider, between the two dividers, and greater than the
    higher-divider. Return a tuple containing the count of packets in the three sections.
    """
    lower = [[2]]
    higher = [[6]]

    low = 0
    middle = 0
    high = 0

    for packet in packets:
        if compare_signals(packet, lower) < 0:
            low += 1
        elif compare_signals(packet, higher) < 0:
            middle += 1
        else:
            high += 1

    return (low, middle, high)


def decoder_key(packets: tuple[Any, ...]) -> int:
    """
    Using the divider packets [[2]] and [[6]], divide up the given set of packets, determine the
    locations of the divider packets in a sorted list of all packets, and return the product of
    their indices (counting from 1).
    """
    low, middle, _ = divide_packets(packets)
    return (low + 1) * (low + middle + 2)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert read_pair("\n".join(("[1,1,3,1,1]", "[1,1,5,1,1]",))) == (
        [1, 1, 3, 1, 1],
        [1, 1, 5, 1, 1],
    )
    assert read_pair("\n".join(("[[1],[2,3,4]]", "[[1],4]",))) == (
        [[1], [2, 3, 4]],
        [[1], 4],
    )
    pairs: tuple[Pair, ...] = (
        (
            [1, 1, 3, 1, 1],
            [1, 1, 5, 1, 1],
        ),
        (
            [[1], [2, 3, 4]],
            [[1], 4],
        ),
        (
            [9],
            [[8, 7, 6]],
        ),
        (
            [[4, 4], 4, 4],
            [[4, 4], 4, 4, 4],
        ),
        (
            [7, 7, 7, 7],
            [7, 7, 7],
        ),
        (
            [],
            [3],
        ),
        (
            [[[]]],
            [[]],
        ),
        (
            [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
            [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        ),
    )
    assert (
        read_pairs(
            "\n".join(
                (
                    "[1,1,3,1,1]",
                    "[1,1,5,1,1]",
                    "",
                    "[[1],[2,3,4]]",
                    "[[1],4]",
                    "",
                    "[9]",
                    "[[8,7,6]]",
                    "",
                    "[[4,4],4,4]",
                    "[[4,4],4,4,4]",
                    "",
                    "[7,7,7,7]",
                    "[7,7,7]",
                    "",
                    "[]",
                    "[3]",
                    "",
                    "[[[]]]",
                    "[[]]",
                    "",
                    "[1,[2,[3,[4,[5,6,7]]]],8,9]",
                    "[1,[2,[3,[4,[5,6,0]]]],8,9]",
                )
            )
        )
        == pairs
    )

    # Examples:
    assert compare_signals(1, 3) == -1
    assert compare_signals([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]) == -1
    assert compare_signals([9], [[8, 7, 6]]) == 1
    assert compare_signals([[4, 4], 4, 4], [[4, 4], 4, 4, 4]) == -1
    assert compare_signals([7, 7, 7, 7], [7, 7, 7]) == 1
    assert compare_signals([], [3]) == -1
    assert compare_signals([[[]]], [[]]) == 1
    assert (
        compare_signals(
            [1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
        )
        == 1
    )
    assert sum(pairs_in_right_order(pairs)) == 13

    # Problematic example from my actual input - empty lists are equal:
    assert compare_signals([[], [1, 2, 3]], [[], [0]]) == 1


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    pairs: tuple[Pair, ...] = (
        (
            [1, 1, 3, 1, 1],
            [1, 1, 5, 1, 1],
        ),
        (
            [[1], [2, 3, 4]],
            [[1], 4],
        ),
        (
            [9],
            [[8, 7, 6]],
        ),
        (
            [[4, 4], 4, 4],
            [[4, 4], 4, 4, 4],
        ),
        (
            [7, 7, 7, 7],
            [7, 7, 7],
        ),
        (
            [],
            [3],
        ),
        (
            [[[]]],
            [[]],
        ),
        (
            [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
            [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        ),
    )
    packets: tuple[Any, ...] = (
        [1, 1, 3, 1, 1],
        [1, 1, 5, 1, 1],
        [[1], [2, 3, 4]],
        [[1], 4],
        [9],
        [[8, 7, 6]],
        [[4, 4], 4, 4],
        [[4, 4], 4, 4, 4],
        [7, 7, 7, 7],
        [7, 7, 7],
        [],
        [3],
        [[[]]],
        [[]],
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
    )
    assert all_packets(pairs) == packets
    assert divide_packets(packets) == (9, 3, 4)
    assert decoder_key(packets) == 140


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=13)
    pairs = read_pairs(data)

    print(f"Part 1: {sum(pairs_in_right_order(pairs))}")

    packets = all_packets(pairs)
    print(f"Part 2: {decoder_key(packets)}")


if __name__ == "__main__":
    main()
