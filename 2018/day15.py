"""
2018 Day 15
https://adventofcode.com/2018/day/15
"""

import math
from collections import deque, namedtuple
from itertools import chain, count
from typing import Dict, Iterable, Optional, Set, Tuple
import aocd  # type: ignore

Combatant = namedtuple("Combatant", "position team hp attack")
Combatants = Tuple[Combatant, ...]


def read_units(text: str) -> Combatants:
    return tuple(
        chain.from_iterable(
            (
                Combatant(
                    position=complex(x, y),
                    team="elf" if char == "E" else "goblin",
                    hp=200,
                    attack=3,
                )
                for x, char in enumerate(row)
                if char in ("E", "G")
            )
            for y, row in enumerate(text.split("\n"))
        )
    )


def read_walls(text: str) -> Set[complex]:
    return set(
        chain.from_iterable(
            (complex(x, y) for x, char in enumerate(row) if char == "#")
            for y, row in enumerate(text.split("\n"))
        )
    )


def adjacent(first: complex, second: complex) -> bool:
    return second in (first + 1, first - 1, first + 1j, first - 1j)


def free_spaces_next_to_targets(
    targets: Iterable[Combatant], occupied: Set[complex]
) -> Set[complex]:
    spaces_next_to_targets = chain.from_iterable(
        (
            target.position + 1,
            target.position - 1,
            target.position + 1j,
            target.position - 1j,
        )
        for target in targets
    )
    return set(space for space in spaces_next_to_targets if space not in occupied)


def potential_targets(actor: Combatant, units: Iterable[Combatant]) -> Set[Combatant]:
    return set(unit for unit in units if unit.team != actor.team and unit.hp > 0)


def distance_to_spaces(position: complex, occupied: Set[complex]) -> Dict[complex, int]:
    compass = (1, -1, 1j, -1j)
    distances: Dict[complex, int] = {}
    consider = deque([(0, position)])

    while consider:
        dist, pos = consider.popleft()
        distances[pos] = dist
        for direction in compass:
            adj = pos + direction
            if (adj not in occupied) and (adj not in distances):
                if not any(c[1] == adj for c in consider):
                    consider.append((dist + 1, adj))

    return distances


def damage(unit: Combatant, power: int) -> Combatant:
    return Combatant(
        position=unit.position,
        team=unit.team,
        hp=max(0, unit.hp - power),
        attack=unit.attack,
    )


def moved(unit: Combatant, position: complex) -> Combatant:
    return Combatant(position=position, team=unit.team, hp=unit.hp, attack=unit.attack)


def identify_movement_target(
    position: complex, enemies: Iterable[Combatant], occupied: Set[complex]
) -> Optional[complex]:
    distances = distance_to_spaces(position, occupied)
    reachable_fsntt = {
        space
        for space in free_spaces_next_to_targets(enemies, occupied)
        if space in distances
    }
    if reachable_fsntt:
        return sorted(
            reachable_fsntt, key=lambda t: (distances.get(t, math.inf), t.imag, t.real)
        )[0]
    return None


def next_step_toward_movement_target(
    position: complex, target: complex, occupied: Set[complex]
) -> complex:
    distances = distance_to_spaces(target, occupied)
    adj = [
        loc
        for loc in (position + 1, position - 1, position + 1j, position - 1j)
        if loc not in occupied
    ]
    sort_candidates = lambda c: (distances.get(c, math.inf), c.imag, c.real)
    return sorted(adj, key=sort_candidates)[0]


def advance(
    rounds: int, units: Iterable[Combatant], walls: Set[complex]
) -> Tuple[int, Set[Combatant]]:
    sort_units = lambda x: (x.position.imag, x.position.real)

    units = list(sorted(units, key=sort_units))
    victory_before_end = False

    for unit_ix, unit in enumerate(units):
        if unit.hp > 0:
            occupied = walls | {
                unit.position
                for id, unit in enumerate(units)
                if unit.hp > 0 and id != unit_ix
            }
            adj = [
                loc
                for loc in (
                    unit.position + 1,
                    unit.position - 1,
                    unit.position + 1j,
                    unit.position - 1j,
                )
                if loc not in walls
            ]

            targets = [
                other for other in units if other.team != unit.team and other.hp > 0
            ]
            if not targets:  # no enemies, so early victory needs recording
                victory_before_end = True
            if sum(1 for targ in targets if targ.position in adj) == 0 and adj:
                target = identify_movement_target(unit.position, targets, occupied)
                if target:
                    move_to = next_step_toward_movement_target(
                        unit.position, target, occupied
                    )
                    unit = moved(unit, move_to)
                    units[unit_ix] = unit

            adj = [
                loc
                for loc in (
                    unit.position + 1,
                    unit.position - 1,
                    unit.position + 1j,
                    unit.position - 1j,
                )
                if loc not in walls
            ]
            victims = [
                (id, v)
                for id, v in enumerate(units)
                if v.team != unit.team and units[id].hp > 0 and v.position in adj
            ]
            if victims:

                def sort_victims(
                    victim_details: Tuple[int, Combatant]
                ) -> Tuple[int, int, int]:
                    _, victim = victim_details
                    return (victim.hp, victim.position.imag, victim.position.real)

                victid, victim = sorted(victims, key=sort_victims)[0]
                units[victid] = damage(victim, unit.attack)

    rounds = rounds + (0 if victory_before_end else 1)

    return rounds, set(unit for unit in units if unit.hp > 0)


def outcome(rounds: int, units: Iterable[Combatant]) -> Tuple[int, int]:
    hit_points = sum(unit.hp for unit in units)
    return (rounds, hit_points)


def battle(
    walls: Set[complex],
    units: Iterable[Combatant],
    end_on_first_elf_death: bool = False,
) -> Tuple[int, Iterable[Combatant]]:
    rounds = 0
    if end_on_first_elf_death:
        elves_needed = sum(1 for unit in units if unit.team == "elf")
    else:
        elves_needed = 0

    while (
        len(set(unit.team for unit in units)) > 1
        and sum(1 for unit in units if unit.team == "elf") >= elves_needed
    ):
        rounds, units = advance(rounds, units, walls)

    return (rounds, units)


def find_perfect_battle(
    walls: Set[complex], units: Iterable[Combatant]
) -> Tuple[int, Iterable[Combatant]]:
    elves = {unit for unit in units if unit.team == "elf"}
    goblins = {unit for unit in units if unit.team == "goblin"}
    for power in count(4):
        stronger_elves = {
            Combatant(position=elf.position, team=elf.team, hp=elf.hp, attack=power)
            for elf in elves
        }
        rounds, units = battle(walls, stronger_elves | goblins, True)

        if {unit.team for unit in units} == {"elf"}:
            return rounds, units

    return (-1, set())


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=15)

    walls = read_walls(data)
    units = read_units(data)

    rd1, hp1 = outcome(*battle(walls, units))
    print(f"Part 1: {rd1} rounds x {hp1} hp = {rd1*hp1}")

    rd2, hp2 = outcome(*find_perfect_battle(walls, units))
    print(f"Part 2: {rd2} rounds x {hp2} hp = {rd2*hp2}")


if __name__ == "__main__":
    main()
