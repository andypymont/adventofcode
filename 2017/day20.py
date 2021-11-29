"""
2017 Day 20
https://adventofcode.com/2017/day/20
"""

from collections import Counter
from dataclasses import dataclass
from typing import Sequence, Tuple
import aocd # type: ignore
import regex as re # type: ignore

@dataclass(frozen=True)
class Point():
    x_coord: int
    y_coord: int
    z_coord: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(
            self.x_coord + other.x_coord,
            self.y_coord + other.y_coord,
            self.z_coord + other.z_coord
        )

    @property
    def distance(self) -> int:
        return abs(self.x_coord) + abs(self.y_coord) + abs(self.z_coord)

@dataclass
class Particle():
    number: int
    position: Point
    velocity: Point
    acceleration: Point

    @classmethod
    def from_regex_groups(cls, number: int, groups: Sequence[str]) -> 'Particle':
        pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, acc_x, acc_y, acc_z = map(int, groups)
        return cls(
            number,
            Point(pos_x, pos_y, pos_z),
            Point(vel_x, vel_y, vel_z),
            Point(acc_x, acc_y, acc_z)
        )

    def advance(self) -> None:
        self.velocity += self.acceleration
        self.position += self.velocity

def simulate(particles: Sequence[Particle]) -> Tuple[int, int]:
    collided = set()
    for _ in range(1000):
        positions = Counter(particle.position for particle in particles)
        for particle in particles:
            if positions[particle.position] > 1:
                collided.add(particle.number)
            particle.advance()
    closest = next(iter(sorted(particles, key=lambda p: p.position.distance)))
    uncollided = len(particles) - len(collided)
    return (closest.number, uncollided)

def find_closest_particle(particles: Sequence[Particle]) -> Particle:
    for _ in range(1000):
        for particle in particles:
            particle.advance()
    return next(iter(sorted(particles, key=lambda p: p.position.distance)))

RE_PARTICLE = re.compile(
r'p=<([-\d]+),([-\d]+),([-\d]+)>, v=<([-\d]+),([-\d]+),([-\d]+)>, a=<([-\d]+),([-\d]+),([-\d]+)>'
)
def read_particles(text: str) -> Sequence[Particle]:
    return tuple(Particle.from_regex_groups(number, groups)
                 for number, groups in enumerate(RE_PARTICLE.findall(text)))

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=20)

    particles = read_particles(data)
    part1, part2 = simulate(particles)

    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
