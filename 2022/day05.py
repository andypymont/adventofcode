"""
2022 Day 5
https://adventofcode.com/2022/day/5
"""

from dataclasses import dataclass
from typing import Iterator, Tuple
import re
import aocd  # type: ignore

re_move = re.compile(r"move (\d+) from (\d+) to (\d+)")


@dataclass(frozen=True)
class Move:
    """
    In each step of the procedure, a quantity of crates is moved from one stack to a different
    stack.
    """

    quantity: int
    source: int
    destination: int

    @classmethod
    def all_from_input_section(cls, text: str) -> Iterator["Move"]:
        """
        Read the second section of the puzzle input and yield each necessary move.
        """
        for move in re_move.findall(text):
            yield cls(int(move[0]), int(move[1]) - 1, int(move[2]) - 1)


@dataclass(frozen=True)
class Crane:
    """
    Supplies are stored in stacks of marked crates, but because the needed supplies are buried
    under many other crates, the crates need to be rearranged.

    The ship has a giant cargo crane capable of moving crates between stacks.
    """

    stacks: Tuple[str, ...]

    @classmethod
    def from_input_section(cls, text: str) -> "Crane":
        """
        Read a Crane from the top section of the puzzle input.
        """
        lines = [line[1::4] for line in text.split("\n")[:-1]]
        return cls(
            tuple(
                "".join(line[c] for line in lines).strip() for c in range(len(lines[0]))
            )
        )

    @property
    def top_of_stacks(self) -> str:
        """
        Create a word from the top crate of each stack and return it.
        """
        return "".join(stack[0] for stack in self.stacks if stack)

    def after_move(self, move: Move, multicrate_crane: bool = False) -> "Crane":
        """
        Execute the given move and return the new state of the crane stacks.
        """
        source = self.stacks[move.source][move.quantity :]
        moved = self.stacks[move.source][: move.quantity]
        if not multicrate_crane:
            moved = moved[::-1]
        destination = moved + self.stacks[move.destination]
        return Crane(
            tuple(
                source
                if pos == move.source
                else destination
                if pos == move.destination
                else stack
                for pos, stack in enumerate(self.stacks)
            )
        )

    def after_moves(
        self, moves: Iterator[Move], multicrate_crane: bool = False
    ) -> "Crane":
        """
        Execute all given moves and return the new state of the crane stacks.
        """
        crane = self
        for move in moves:
            crane = crane.after_move(move, multicrate_crane)
        return crane


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    moves = Move.all_from_input_section(
        "\n".join(
            (
                "move 1 from 2 to 1",
                "move 3 from 1 to 3",
                "move 2 from 2 to 1",
                "move 1 from 1 to 2",
            )
        )
    )
    assert next(moves) == Move(1, 1, 0)
    assert next(moves) == Move(3, 0, 2)
    assert next(moves) == Move(2, 1, 0)
    assert next(moves) == Move(1, 0, 1)

    initial = Crane(("NZ", "DCM", "P"))
    one = Crane(("DNZ", "CM", "P"))
    two = Crane(("", "CM", "ZNDP"))
    three = Crane(("MC", "", "ZNDP"))
    four = Crane(("C", "M", "ZNDP"))

    assert (
        Crane.from_input_section(
            "\n".join(
                (
                    "    [D]    ",
                    "[N] [C]    ",
                    "[Z] [M] [P]",
                    " 1   2   3 ",
                )
            )
        )
        == initial
    )

    assert initial.after_move(Move(1, 1, 0)) == one
    assert one.after_move(Move(3, 0, 2)) == two
    assert two.after_move(Move(2, 1, 0)) == three
    assert three.after_move(Move(1, 0, 1)) == four

    moves = Move.all_from_input_section(
        "\n".join(
            (
                "move 1 from 2 to 1",
                "move 3 from 1 to 3",
                "move 2 from 2 to 1",
                "move 1 from 1 to 2",
            )
        )
    )
    assert initial.after_moves(moves) == four

    assert initial.top_of_stacks == "NDP"
    assert four.top_of_stacks == "CMZ"


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    initial = Crane(("NZ", "DCM", "P"))
    one = Crane(("DNZ", "CM", "P"))
    two = Crane(("", "CM", "DNZP"))
    three = Crane(("CM", "", "DNZP"))
    four = Crane(("M", "C", "DNZP"))

    assert initial.after_move(Move(1, 1, 0), True) == one
    assert one.after_move(Move(3, 0, 2), True) == two
    assert two.after_move(Move(2, 1, 0), True) == three
    assert three.after_move(Move(1, 0, 1), True) == four

    moves = Move.all_from_input_section(
        "\n".join(
            (
                "move 1 from 2 to 1",
                "move 3 from 1 to 3",
                "move 2 from 2 to 1",
                "move 1 from 1 to 2",
            )
        )
    )
    assert initial.after_moves(moves, True) == four

    assert four.top_of_stacks == "MCD"


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=5)
    crane_data, move_data = data.split("\n\n")
    crane = Crane.from_input_section(crane_data)

    moves = Move.all_from_input_section(move_data)
    part_one = crane.after_moves(moves).top_of_stacks
    print(f"Part 1: {part_one}")

    moves = Move.all_from_input_section(move_data)
    part_two = crane.after_moves(moves, True).top_of_stacks
    print(f"Part 2: {part_two}")


if __name__ == "__main__":
    main()
