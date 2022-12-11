"""
2022 Day 10
https://adventofcode.com/2022/day/10
"""

from dataclasses import dataclass
import aocd  # type: ignore


@dataclass(frozen=True)
class Command:
    """
    A single command in the program, which takes a certain number of cycles to have the given
    effect on the register.
    """

    cycles: int
    effect: int

    @classmethod
    def from_line(cls, line: str) -> "Command":
        """
        Convert a line of the puzzle input into the corresponding Command object.
        """
        if line == "noop":
            return cls(1, 0)
        return cls(2, int(line.split(" ")[1]))

    @classmethod
    def all_from_text(cls, text: str) -> tuple["Command", ...]:
        """
        Return a tuple containing all of the commands in the given input text.
        """
        return tuple(cls.from_line(line) for line in text.split("\n"))


def signal_strengths(
    program: tuple[Command, ...]
) -> tuple[int, int, int, int, int, int]:
    """
    Run the given program, and return the sum of the signal
    """
    values = {}
    cycles = 1
    value = 1

    for command in program:
        for _ in range(command.cycles):
            cycles += 1
            values[cycles] = value
        value += command.effect
        values[cycles] = value

    return (
        values.get(20, 0) * 20,
        values.get(60, 0) * 60,
        values.get(100, 0) * 100,
        values.get(140, 0) * 140,
        values.get(180, 0) * 180,
        values.get(220, 0) * 220,
    )


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert Command.all_from_text("\n".join(("noop", "addx 3", "addx -5",))) == (
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=3),
        Command(cycles=2, effect=-5),
    )

    large_example = (
        Command(cycles=2, effect=15),
        Command(cycles=2, effect=-11),
        Command(cycles=2, effect=6),
        Command(cycles=2, effect=-3),
        Command(cycles=2, effect=5),
        Command(cycles=2, effect=-1),
        Command(cycles=2, effect=-8),
        Command(cycles=2, effect=13),
        Command(cycles=2, effect=4),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=-1),
        Command(cycles=2, effect=5),
        Command(cycles=2, effect=-1),
        Command(cycles=2, effect=5),
        Command(cycles=2, effect=-1),
        Command(cycles=2, effect=5),
        Command(cycles=2, effect=-1),
        Command(cycles=2, effect=5),
        Command(cycles=2, effect=-1),
        Command(cycles=2, effect=-35),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=24),
        Command(cycles=2, effect=-19),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=16),
        Command(cycles=2, effect=-11),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=21),
        Command(cycles=2, effect=-15),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=-3),
        Command(cycles=2, effect=9),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=-3),
        Command(cycles=2, effect=8),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=5),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=-36),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=7),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=2),
        Command(cycles=2, effect=6),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=1),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=7),
        Command(cycles=2, effect=1),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=-13),
        Command(cycles=2, effect=13),
        Command(cycles=2, effect=7),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=-33),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=2),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=8),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=-1),
        Command(cycles=2, effect=2),
        Command(cycles=2, effect=1),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=17),
        Command(cycles=2, effect=-9),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=-3),
        Command(cycles=2, effect=11),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=1),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=1),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=-13),
        Command(cycles=2, effect=-19),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=3),
        Command(cycles=2, effect=26),
        Command(cycles=2, effect=-30),
        Command(cycles=2, effect=12),
        Command(cycles=2, effect=-1),
        Command(cycles=2, effect=3),
        Command(cycles=2, effect=1),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=-9),
        Command(cycles=2, effect=18),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=2),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=9),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=-1),
        Command(cycles=2, effect=2),
        Command(cycles=2, effect=-37),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=3),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=15),
        Command(cycles=2, effect=-21),
        Command(cycles=2, effect=22),
        Command(cycles=2, effect=-6),
        Command(cycles=2, effect=1),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=2),
        Command(cycles=2, effect=1),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=-10),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=2, effect=20),
        Command(cycles=2, effect=1),
        Command(cycles=2, effect=2),
        Command(cycles=2, effect=2),
        Command(cycles=2, effect=-6),
        Command(cycles=2, effect=-11),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
        Command(cycles=1, effect=0),
    )
    assert signal_strengths(large_example) == (420, 1140, 1800, 2940, 2880, 3960)


# def test_part2() -> None:
#     """
#     Examples for Part 2.
#     """
#     assert False


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=10)
    program = Command.all_from_text(data)

    strengths = signal_strengths(program)
    print(f"Part 1: {sum(strengths)}")
    # print(f'Part 2: {p2}')


if __name__ == "__main__":
    main()
