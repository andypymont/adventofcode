"""
2022 Day 2
https://adventofcode.com/2022/day/2
"""

from dataclasses import dataclass
from enum import Enum
import aocd  # type: ignore


class Shape(Enum):
    """
    A shape made in a game of rock-paper-scissors.
    """

    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def from_char(cls, char: str) -> "Shape":
        """
        Translate a character from the written strategy guide into a shape.
        """
        if char in ("A", "X"):
            return cls.ROCK
        if char in ("B", "Y"):
            return cls.PAPER
        if char in ("C", "Z"):
            return cls.SCISSORS
        raise NotImplementedError


class Outcome(Enum):
    """
    The outcome of a single rock-papers-scissor game.
    """

    LOSS = 0
    DRAW = 3
    WIN = 6

    @classmethod
    def from_char(cls, char: str) -> "Outcome":
        """
        Translate a character from the written strategy guide into a shape.
        """
        if char == "X":
            return cls.LOSS
        if char == "Y":
            return cls.DRAW
        if char == "Z":
            return cls.WIN
        raise NotImplementedError


@dataclass(frozen=True)
class Game:
    """
    A single game of rock-paper-scissors, consisting of a move by each player.
    """

    opponent: Shape
    move: Shape

    @classmethod
    def from_line(cls, line: str) -> "Game":
        """
        Create a Game instance from a single line of the strategy guide.
        """
        return cls(*(Shape.from_char(char) for char in line.split(" ")))

    @property
    def outcome(self) -> Outcome:
        """
        Determine the outcome of this particular Game.
        """
        if self.move == self.opponent:
            return Outcome.DRAW
        if self.move == {
            Shape.SCISSORS: Shape.ROCK,
            Shape.ROCK: Shape.PAPER,
            Shape.PAPER: Shape.SCISSORS,
        }[self.opponent]:
            return Outcome.WIN
        return Outcome.LOSS

    @property
    def score(self) -> int:
        """
        Calculate the game score by adding the points values of the move used and the game outcome.
        """
        return self.move.value + self.outcome.value


@dataclass(frozen=True)
class OutcomeGame:
    """
    A single game of rock-paper-scissors, consisting of the opponent's shape and an outcome.
    """

    shape: Shape
    outcome: Outcome

    @classmethod
    def from_line(cls, line: str) -> "OutcomeGame":
        """
        Create an OutcomeGame instance from a single line of the strategy guide.
        """
        parts = line.split(" ")
        return cls(Shape.from_char(parts[0]), Outcome.from_char(parts[1]))

    @property
    def move(self) -> "Shape":
        """
        Determine which shape to use yourself to get the intended outcome in this game.
        """
        if self.outcome == Outcome.WIN:
            return {
                Shape.SCISSORS: Shape.ROCK,
                Shape.ROCK: Shape.PAPER,
                Shape.PAPER: Shape.SCISSORS,
            }[self.shape]
        if self.outcome == Outcome.LOSS:
            return {
                Shape.ROCK: Shape.SCISSORS,
                Shape.PAPER: Shape.ROCK,
                Shape.SCISSORS: Shape.PAPER,
            }[self.shape]
        return self.shape

    @property
    def score(self) -> int:
        """
        Calculate the game score by adding the points value of the move used and the game outcome.
        """
        return self.move.value + self.outcome.value


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert Shape.ROCK.value == 1
    assert Shape.PAPER.value == 2
    assert Shape.SCISSORS.value == 3
    assert Shape.from_char("A") == Shape.ROCK
    assert Shape.from_char("B") == Shape.PAPER
    assert Shape.from_char("C") == Shape.SCISSORS
    assert Shape.from_char("X") == Shape.ROCK
    assert Shape.from_char("Y") == Shape.PAPER
    assert Shape.from_char("Z") == Shape.SCISSORS
    assert Game.from_line("A Y") == Game(Shape.ROCK, Shape.PAPER)
    assert Game.from_line("B X") == Game(Shape.PAPER, Shape.ROCK)
    assert Game.from_line("C Z") == Game(Shape.SCISSORS, Shape.SCISSORS)
    assert Game(Shape.ROCK, Shape.PAPER).score == 8
    assert Game(Shape.PAPER, Shape.ROCK).score == 1
    assert Game(Shape.SCISSORS, Shape.SCISSORS).score == 6


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert Outcome.from_char("X") == Outcome.LOSS
    assert Outcome.from_char("Y") == Outcome.DRAW
    assert Outcome.from_char("Z") == Outcome.WIN
    assert OutcomeGame.from_line("A Y") == OutcomeGame(Shape.ROCK, Outcome.DRAW)
    assert OutcomeGame.from_line("B X") == OutcomeGame(Shape.PAPER, Outcome.LOSS)
    assert OutcomeGame.from_line("C Z") == OutcomeGame(Shape.SCISSORS, Outcome.WIN)
    assert OutcomeGame(Shape.ROCK, Outcome.DRAW).score == 4
    assert OutcomeGame(Shape.PAPER, Outcome.LOSS).score == 1
    assert OutcomeGame(Shape.SCISSORS, Outcome.WIN).score == 7


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=2)

    part_one = sum(Game.from_line(line).score for line in data.split("\n"))
    print(f"Part 1: {part_one}")

    part_two = sum(OutcomeGame.from_line(line).score for line in data.split("\n"))
    print(f"Part 2: {part_two}")


if __name__ == "__main__":
    main()
