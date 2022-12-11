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


def run_program(program: tuple[Command, ...]) -> dict[int, int]:
    """
    Run the given program and return the register values at each cycle during execution.
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

    return values


def signal_strengths(
    program_results: dict[int, int]
) -> tuple[int, int, int, int, int, int]:
    """
    Return the sum of the signal strengths from the given program results.
    """
    return (
        program_results.get(20, 0) * 20,
        program_results.get(60, 0) * 60,
        program_results.get(100, 0) * 100,
        program_results.get(140, 0) * 140,
        program_results.get(180, 0) * 180,
        program_results.get(220, 0) * 220,
    )


def sprite_in_position(pos: int, value: int) -> bool:
    """
    Return True/False whether a program value (value) includes the given horizontal position.
    """
    hpos = (pos % 40) or 40
    return value in (hpos, hpos - 1, hpos - 2)


def crt_image(values: dict[int, int]) -> str:
    """
    Create the CRT image from the given values-at-each-cycle.
    """
    image = "".join(
        "█" if sprite_in_position(pos, values.get(pos, 0)) else " "
        for pos in range(1, 241)
    )
    return "\n".join(
        (
            image[:40],
            image[40:80],
            image[80:120],
            image[120:160],
            image[160:200],
            image[200:240],
        )
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
    assert signal_strengths(run_program(large_example)) == (
        420,
        1140,
        1800,
        2940,
        2880,
        3960,
    )


def test_part2() -> None:
    """
    Examples for Part 2.
    """
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
    results = run_program(large_example)

    assert sprite_in_position(200, 38)
    assert crt_image(results) == "\n".join(
        (
            "██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ",
            "███   ███   ███   ███   ███   ███   ███ ",
            "████    ████    ████    ████    ████    ",
            "█████     █████     █████     █████     ",
            "██████      ██████      ██████      ████",
            "███████       ███████       ███████     ",
        )
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2022, day=10)
    program = Command.all_from_text(data)
    results = run_program(program)
    strengths = signal_strengths(results)

    print(f"Part 1: {sum(strengths)}")
    print(f"Part 2:\n{crt_image(results)}")


if __name__ == "__main__":
    main()
