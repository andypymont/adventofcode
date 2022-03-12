"""
2019 Day 22
https://adventofcode.com/2019/day/22
"""

from typing import Iterable
import aocd  # type: ignore


def track_card(card: int, deck_size: int, instructions: Iterable[str]) -> int:
    """
    Track the given card number through the given set of instructions and return its
    final position.
    """
    for instruction in instructions:
        if instruction == "deal into new stack":
            card = deck_size - 1 - card
        elif instruction.startswith("deal with increment"):
            increment = int(instruction.split(" ")[-1])
            card = (card * increment) % deck_size
        elif instruction.startswith("cut"):
            quantity = int(instruction.split(" ")[-1])
            if quantity > 0:
                # positive cut: move cards from top to bottom
                if card < quantity:
                    card += deck_size - quantity
                else:
                    card -= quantity
            elif quantity < 0:
                # negative cut: move cards from bottom to top
                quantity *= -1
                remainder = deck_size - quantity
                if card >= remainder:
                    card -= remainder
                else:
                    card += quantity

    return card


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert (
        track_card(
            3,
            10,
            (
                "deal with increment 7",
                "deal into new stack",
                "deal into new stack",
            ),
        )
        == 1
    )
    assert (
        track_card(
            4,
            10,
            (
                "cut 6",
                "deal with increment 7",
                "deal into new stack",
            ),
        )
        == 3
    )
    assert (
        track_card(
            5,
            10,
            (
                "deal with increment 7",
                "deal with increment 9",
                "cut -2",
            ),
        )
        == 7
    )
    assert (
        track_card(
            1,
            10,
            (
                "deal into new stack",
                "cut -2",
                "deal with increment 7",
                "cut 8",
                "cut -4",
                "deal with increment 7",
                "cut 3",
                "deal with increment 9",
                "deal with increment 3",
                "cut -1",
            ),
        )
        == 4
    )


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=22)

    instructions = data.split("\n")
    print(f"Part 1: {track_card(2019, 10_007, instructions)}")


if __name__ == "__main__":
    main()
