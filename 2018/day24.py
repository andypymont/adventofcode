"""
2018 Day 24
https://adventofcode.com/2018/day/24
"""

from dataclasses import dataclass
from enum import Enum
from itertools import count
from typing import Dict, List, Optional, Set, Tuple
import re
import aocd  # type: ignore


class Team(Enum):
    IMMUNE = 0
    INFECTION = 1


@dataclass(frozen=True)
class Attack:
    damage: int
    type: str
    initiative: int


RE_GROUP = re.compile(
    r"(\d+) units each with (\d+) hit points (\([^)]*\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)"
)
RE_IMMUNE = re.compile(r"immune to ([\w, ]+)")
RE_WEAK = re.compile(r"weak to ([\w, ]+)")


@dataclass
class Group:
    team: Team
    units: int
    hit_points: int
    weaknesses: Set[str]
    immunities: Set[str]
    attack: Attack

    @property
    def effective_power(self) -> int:
        return self.units * self.attack.damage

    def damage_dealt(self, defender: "Group") -> int:
        if self.attack.type in defender.immunities:
            return 0
        multiplier = 2 if self.attack.type in defender.weaknesses else 1
        return self.effective_power * multiplier

    def take_damage(self, damage: int) -> None:
        lost_units = damage // self.hit_points
        self.units = max(self.units - lost_units, 0)

    @classmethod
    def all_from_description(cls, text: str) -> List["Group"]:
        groups: List["Group"] = []

        for section in text.split("\n\n"):
            heading, *groupdescs = section.split("\n")
            team = Team.IMMUNE if heading == "Immune System:" else Team.INFECTION

            for group in groupdescs:
                groups.append(cls.from_description(team, group))

        return groups

    @classmethod
    def from_description(cls, team: Team, desc: str) -> "Group":
        match = RE_GROUP.match(desc)
        if not match:
            raise ValueError

        units, hit_points, types, damage, damage_type, initiative = match.groups()

        weak_match = RE_WEAK.search(types) if types else None
        weak = set(weak_match.group(1).split(", ")) if weak_match else set()

        immune_match = RE_IMMUNE.search(types) if types else None
        immune = set(immune_match.group(1).split(", ")) if immune_match else set()

        return cls(
            team,
            int(units),
            int(hit_points),
            weak,
            immune,
            Attack(int(damage), damage_type, int(initiative)),
        )


def target_selection(groups: List[Group]) -> Dict[int, int]:
    results: Dict[int, int] = {}
    targeted: Set[int] = set()

    for attacker_no, attacker in sorted(
        enumerate(groups),
        key=lambda g: (g[1].effective_power, g[1].attack.initiative),
        reverse=True,
    ):
        potential_targets: Dict[int, Tuple[int, int, int]] = {
            defender_no: (
                attacker.damage_dealt(groups[defender_no]),
                groups[defender_no].effective_power,
                groups[defender_no].attack.initiative,
            )
            for defender_no, defender in enumerate(groups)
            if defender.team != attacker.team and defender_no not in targeted
        }
        if (
            len(potential_targets) > 0
            and max(v[0] for v in potential_targets.values()) > 0
        ):
            defender_no = max(potential_targets, key=potential_targets.get)
            results[attacker_no] = defender_no
            targeted.add(defender_no)

    return results


def fight(groups: List[Group]) -> List[Group]:
    """
    Process a single round of combat.
    """
    targeting = target_selection(groups)

    for attacker_no, attacker in sorted(
        enumerate(groups), key=lambda g: g[1].attack.initiative, reverse=True
    ):
        if attacker_no in targeting and attacker.units > 0:
            defender_no = targeting[attacker_no]
            defender = groups[defender_no]
            damage = attacker.damage_dealt(defender)
            defender.take_damage(damage)

    return [group for group in groups if group.units > 0]


def battle(groups: List[Group]) -> Tuple[Optional[Team], int]:
    """
    Process an entire battle, by running rounds of combat until only one side survives. Then return
    the result (total units on the surviving side)
    """
    while True:
        teams = {group.team for group in groups}
        units = sum(group.units for group in groups)

        if len(teams) == 0:
            return (None, 0)
        if len(teams) == 1:
            winner = Team.IMMUNE if Team.IMMUNE in teams else Team.INFECTION
            return (winner, units)

        groups = fight(groups)
        if (
            sum(group.units for group in groups) == units
        ):  # stalemate as no units are being killed
            return (None, units)


def boost(groups: List[Group], amount: int) -> List[Group]:
    return [
        Group(
            g.team,
            g.units,
            g.hit_points,
            g.weaknesses,
            g.immunities,
            Attack(
                g.attack.damage + (amount if g.team == Team.IMMUNE else 0),
                g.attack.type,
                g.attack.initiative,
            ),
        )
        for g in groups
    ]


def smallest_boosted_win(groups: List[Group]) -> int:
    for amount in count(1):
        boosted_groups = boost(groups, amount)
        winner, survivors = battle(boosted_groups)
        if winner == Team.IMMUNE:
            return survivors
    return -1


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    eg1 = "".join(
        (
            "18 units each with 729 hit points (weak to fire; immune to cold, slashing) ",
            "with an attack that does 8 radiation damage at initiative 10",
        )
    )
    ex1 = Group(
        team=Team.IMMUNE,
        units=18,
        hit_points=729,
        weaknesses={"fire"},
        immunities={"cold", "slashing"},
        attack=Attack(damage=8, type="radiation", initiative=10),
    )
    assert Group.from_description(Team.IMMUNE, eg1) == ex1

    eg2 = "\n".join(
        (
            "Immune System:",
            "".join(
                (
                    "17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack ",
                    "that does 4507 fire damage at initiative 2",
                )
            ),
            "".join(
                (
                    "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) ",
                    "with an attack that does 25 slashing damage at initiative 3",
                )
            ),
            "",
            "Infection:",
            "".join(
                (
                    "801 units each with 4706 hit points (weak to radiation) with an attack that does 116",
                    " bludgeoning damage at initiative 1",
                )
            ),
            "".join(
                (
                    "4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with ",
                    "an attack that does 12 slashing damage at initiative 4",
                )
            ),
        )
    )
    ex2 = [
        Group(
            team=Team.IMMUNE,
            units=17,
            hit_points=5390,
            weaknesses={"radiation", "bludgeoning"},
            immunities=set(),
            attack=Attack(damage=4507, type="fire", initiative=2),
        ),
        Group(
            team=Team.IMMUNE,
            units=989,
            hit_points=1274,
            weaknesses={"bludgeoning", "slashing"},
            immunities={"fire"},
            attack=Attack(damage=25, type="slashing", initiative=3),
        ),
        Group(
            team=Team.INFECTION,
            units=801,
            hit_points=4706,
            weaknesses={"radiation"},
            immunities=set(),
            attack=Attack(damage=116, type="bludgeoning", initiative=1),
        ),
        Group(
            team=Team.INFECTION,
            units=4485,
            hit_points=2961,
            weaknesses={"fire", "cold"},
            immunities={"radiation"},
            attack=Attack(damage=12, type="slashing", initiative=4),
        ),
    ]
    assert Group.all_from_description(eg2) == ex2
    assert ex2[0].effective_power == 76619
    assert ex2[1].effective_power == 24725
    assert ex2[2].effective_power == 92916
    assert ex2[3].effective_power == 53820
    assert ex2[0].damage_dealt(ex2[2]) == 76619
    assert ex2[0].damage_dealt(ex2[3]) == 153238
    assert ex2[1].damage_dealt(ex2[2]) == 24725
    assert ex2[2].damage_dealt(ex2[0]) == 185832
    assert ex2[2].damage_dealt(ex2[1]) == 185832
    assert ex2[3].damage_dealt(ex2[1]) == 107640
    assert target_selection(ex2) == {2: 0, 0: 3, 3: 1, 1: 2}

    ex3 = [
        Group(
            team=Team.IMMUNE,
            units=905,
            hit_points=1274,
            weaknesses={"bludgeoning", "slashing"},
            immunities={"fire"},
            attack=Attack(damage=25, type="slashing", initiative=3),
        ),
        Group(
            team=Team.INFECTION,
            units=797,
            hit_points=4706,
            weaknesses={"radiation"},
            immunities=set(),
            attack=Attack(damage=116, type="bludgeoning", initiative=1),
        ),
        Group(
            team=Team.INFECTION,
            units=4434,
            hit_points=2961,
            weaknesses={"fire", "cold"},
            immunities={"radiation"},
            attack=Attack(damage=12, type="slashing", initiative=4),
        ),
    ]
    assert fight(ex2) == ex3
    assert ex3[0].damage_dealt(ex3[1]) == 22625
    assert ex3[0].damage_dealt(ex3[2]) == 22625
    assert ex3[1].damage_dealt(ex3[0]) == 184904
    assert target_selection(ex3) == {0: 1, 1: 0}
    assert battle(ex2) == (Team.INFECTION, 5216)


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    ex1 = [
        Group(
            team=Team.IMMUNE,
            units=17,
            hit_points=5390,
            weaknesses={"radiation", "bludgeoning"},
            immunities=set(),
            attack=Attack(damage=4507, type="fire", initiative=2),
        ),
        Group(
            team=Team.IMMUNE,
            units=989,
            hit_points=1274,
            weaknesses={"bludgeoning", "slashing"},
            immunities={"fire"},
            attack=Attack(damage=25, type="slashing", initiative=3),
        ),
        Group(
            team=Team.INFECTION,
            units=801,
            hit_points=4706,
            weaknesses={"radiation"},
            immunities=set(),
            attack=Attack(damage=116, type="bludgeoning", initiative=1),
        ),
        Group(
            team=Team.INFECTION,
            units=4485,
            hit_points=2961,
            weaknesses={"fire", "cold"},
            immunities={"radiation"},
            attack=Attack(damage=12, type="slashing", initiative=4),
        ),
    ]
    ex2 = [
        Group(
            team=Team.IMMUNE,
            units=17,
            hit_points=5390,
            weaknesses={"radiation", "bludgeoning"},
            immunities=set(),
            attack=Attack(damage=6077, type="fire", initiative=2),
        ),
        Group(
            team=Team.IMMUNE,
            units=989,
            hit_points=1274,
            weaknesses={"bludgeoning", "slashing"},
            immunities={"fire"},
            attack=Attack(damage=1595, type="slashing", initiative=3),
        ),
        Group(
            team=Team.INFECTION,
            units=801,
            hit_points=4706,
            weaknesses={"radiation"},
            immunities=set(),
            attack=Attack(damage=116, type="bludgeoning", initiative=1),
        ),
        Group(
            team=Team.INFECTION,
            units=4485,
            hit_points=2961,
            weaknesses={"fire", "cold"},
            immunities={"radiation"},
            attack=Attack(damage=12, type="slashing", initiative=4),
        ),
    ]
    assert boost(ex1, 1570) == ex2
    assert battle(ex2) == (Team.IMMUNE, 51)


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=24)
    groups = Group.all_from_description(data)

    _, part1 = battle(boost(groups, 0))
    print(f"Part 1: {part1}")

    print(f"Part 2: {smallest_boosted_win(groups)}")


if __name__ == "__main__":
    main()
