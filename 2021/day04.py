"""
2021 Day 4
https://adventofcode.com/2021/day/4
"""

from typing import Iterator, List, Set, Tuple
import aocd  # type: ignore
import numpy as np


class BingoBoard:
    def __init__(self, text: str):
        self.board: np.ndarray = np.array(
            [[int(number) for number in line.split()] for line in text.split("\n")]
        )
        self.marked: Set[int] = set()

    def mark(self, number: int) -> None:
        self.marked.add(number)

    @property
    def is_won(self) -> bool:
        for row in self.board:
            marked = self.marked.intersection(row)
            if len(marked) == len(row):
                return True
        for row in np.rot90(self.board):
            marked = self.marked.intersection(row)
            if len(marked) == len(row):
                return True
        return False

    @property
    def unmarked_sum(self) -> int:
        return sum(set(self.board.flatten()) - self.marked)


def read_data(text: str) -> Tuple[List[int], List[BingoBoard]]:
    sections = text.split("\n\n")
    return (
        [int(number) for number in sections[0].split(",")],
        [BingoBoard(board) for board in sections[1:]],
    )


def play_game(numbers: List[int], boards: List[BingoBoard]) -> Iterator[int]:
    won = set()
    for number in numbers:
        for board_no, board in enumerate(boards):
            if board_no not in won:
                board.mark(number)
                if board.is_won:
                    won.add(board_no)
                    yield number * board.unmarked_sum
        if len(won) == len(boards):
            break


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    board = BingoBoard(
        "\n".join(
            (
                "22 13 17 11  0",
                " 8  2 23  4 24",
                "21  9 14 16  7",
                " 6 10  3 18  5",
                " 1 12 20 15 19",
            )
        )
    )
    assert board.marked == set()
    assert not board.is_won
    assert board.unmarked_sum == 300
    board.mark(22)
    assert board.marked == {22}
    board.mark(3)
    assert board.marked == {3, 22}
    board.mark(6)
    board.mark(10)
    board.mark(18)
    board.mark(5)
    assert board.is_won
    assert board.unmarked_sum == 236

    numbers, boards = read_data(
        "\n".join(
            (
                "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",
                "",
                "22 13 17 11  0",
                " 8  2 23  4 24",
                "21  9 14 16  7",
                " 6 10  3 18  5",
                " 1 12 20 15 19",
                "",
                " 3 15  0  2 22",
                " 9 18 13 17  5",
                "19  8  7 25 23",
                "20 11 10 24  4",
                "14 21 16 12  6",
                "",
                "14 21 17 24  4",
                "10 16 15  9 19",
                "18  8 23 26 20",
                "22 11 13  6  5",
                " 2  0 12  3  7",
            )
        )
    )
    assert numbers == [
        7,
        4,
        9,
        5,
        11,
        17,
        23,
        2,
        0,
        14,
        21,
        24,
        10,
        16,
        13,
        6,
        15,
        25,
        12,
        22,
        18,
        20,
        8,
        19,
        3,
        26,
        1,
    ]
    assert next(play_game(numbers, boards)) == 4512


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    numbers, boards = read_data(
        "\n".join(
            (
                "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",
                "",
                "22 13 17 11  0",
                " 8  2 23  4 24",
                "21  9 14 16  7",
                " 6 10  3 18  5",
                " 1 12 20 15 19",
                "",
                " 3 15  0  2 22",
                " 9 18 13 17  5",
                "19  8  7 25 23",
                "20 11 10 24  4",
                "14 21 16 12  6",
                "",
                "14 21 17 24  4",
                "10 16 15  9 19",
                "18  8 23 26 20",
                "22 11 13  6  5",
                " 2  0 12  3  7",
            )
        )
    )
    game = list(play_game(numbers, boards))
    assert game[-1] == 1924


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=4)

    numbers, boards = read_data(data)
    game = play_game(numbers, boards)
    print(f"Part 1: {next(game)}")

    print(f"Part 2: {list(game)[-1]}")


if __name__ == "__main__":
    main()
