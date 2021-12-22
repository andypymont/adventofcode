"""
2015 Day 14
https://adventofcode.com/2015/day/14
"""

from dataclasses import dataclass
from typing import Sequence, Tuple
import aocd  # type: ignore


@dataclass(frozen=True)
class Reindeer:
    """
    Object encapsulating a reindeer's name and inherent attributes.
    """

    name: str
    speed: int
    flytime: int
    rest_needed: int

    @classmethod
    def from_description_line(cls, line: str) -> "Reindeer":
        """
        Parse one reindeer from a line in the puzzle description.
        """
        words = line.split()
        return cls(
            name=words[0],
            speed=int(words[3]),
            flytime=int(words[6]),
            rest_needed=int(words[13]),
        )

    @classmethod
    def all_from_description(cls, description: str) -> "Sequence[Reindeer]":
        """
        Parse all reindeer from the puzzle description.
        """
        return tuple(
            cls.from_description_line(line) for line in description.split("\n")
        )


@dataclass
class ReindeerStatus:
    """
    Object containing the reindeer's current status in the race - resting or flying - along with
    how much time until that is due to change again and the total distance travalled and points
    scored so far.
    """

    reindeer: Reindeer
    flying: bool
    time_left: int
    distance_travelled: int
    score: int

    @classmethod
    def from_reindeer(cls, reindeer: Reindeer) -> "ReindeerStatus":
        """
        Create the default status for the first split-second of the race for the given reindeer.
        """
        return cls(
            reindeer=reindeer,
            flying=True,
            time_left=reindeer.flytime,
            distance_travelled=0,
            score=0,
        )

    def progress(self):
        """
        Progress to the next minute, also then changing status to flying or resting if necessary.
        """
        self.time_left -= 1
        if self.flying:
            self.distance_travelled += self.reindeer.speed
        if self.time_left == 0:
            self.flying = not self.flying
            self.time_left = (
                self.reindeer.flytime if self.flying else self.reindeer.rest_needed
            )

    def add_score(self, distance_to_score: int):
        """
        Record a point scored if the reindeer has travelled at least as far as the distance
        provided.
        """
        if self.distance_travelled >= distance_to_score:
            self.score += 1


def race(reindeer: Sequence[Reindeer], seconds: int = 2503) -> Tuple[int, int]:
    """
    Race the provided group of reindeer and return the further distance travelled and the score of
    the winner.
    """
    racers = [ReindeerStatus.from_reindeer(individual) for individual in reindeer]

    for _ in range(seconds):
        for racer in racers:
            racer.progress()
        furthest_travelled = max(racer.distance_travelled for racer in racers)
        for racer in racers:
            racer.add_score(furthest_travelled)
    return (
        max(racer.distance_travelled for racer in racers),
        max(racer.score for racer in racers),
    )


def test_example():
    """
    Example from puzzle description..
    """
    example = "\n".join(
        (
            "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
            "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.",
        )
    )
    example_racers = Reindeer.all_from_description(example)
    assert race(example_racers, 1000) == (1120, 689)


def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=14)
    reindeer = Reindeer.all_from_description(data)
    distance, score = race(reindeer)

    print(f"Part 1: {distance}")
    print(f"Part 2: {score}")


if __name__ == "__main__":
    main()
