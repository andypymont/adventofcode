"""
2015 Day 21
https://adventofcode.com/2015/day/21
"""

from dataclasses import dataclass
from itertools import chain, combinations, product
from typing import Callable, Sequence, Set
import aocd # type: ignore

@dataclass
class Boss:
    """
    The boss, in all its malevolent glory.
    """
    hitpoints: int
    damage: int
    armor: int

    def __init__(self, desc: str):
        for line in desc.split('\n'):
            attribute, value = line.split(': ')
            if attribute == 'Hit Points':
                self.hitpoints = int(value)
            elif attribute == 'Damage':
                self.damage = int(value)
            elif attribute == 'Armor':
                self.armor = int(value)

    def hit(self, damage: int) -> bool:
        """
        Deal the given amount of damage to the boss, reduced appropriately by its armor. Return
        True if this was sufficient to defeat the boss, otherwise False.
        """
        self.hitpoints -= max(1, damage - self.armor)
        return self.hitpoints <= 0

    @classmethod
    def get_boss_factory(cls, data: str) -> 'Callable[[], Boss]':
        """
        Create a factory funtion which will allow for creating new bosses with the same original
        data, to experiment with equipment combinations.
        """
        def factory() -> 'Boss':
            """
            Factory function to return a new boss with the same original stats.
            """
            return cls(data)
        return factory

@dataclass(frozen=True)
class Equipment:
    """
    Equipment that the player can wear for a boss battle.
    """
    name: str
    cost: int
    damage: int
    armor: int

WEAPONS = {
    Equipment(name='Dagger', cost=8, damage=4, armor=0),
    Equipment(name='Shortsword', cost=10, damage=5, armor=0),
    Equipment(name='Warhammer', cost=25, damage=6, armor=0),
    Equipment(name='Longsword', cost=40, damage=7, armor=0),
    Equipment(name='Greataxe', cost=74, damage=8, armor=0),
}
ARMOR = {
    Equipment(name='Leather', cost=13, damage=0, armor=1),
    Equipment(name='Chainmail', cost=31, damage=0, armor=2),
    Equipment(name='Splitnmail', cost=53, damage=0, armor=3),
    Equipment(name='Bandedmail', cost=75, damage=0, armor=4),
    Equipment(name='Platemail', cost=102, damage=0, armor=5),
}
RINGS = {
    Equipment(name='Damage +1', cost=25, damage=1, armor=0),
    Equipment(name='Damage +2', cost=50, damage=2, armor=0),
    Equipment(name='Damage +3', cost=100, damage=3, armor=0),
    Equipment(name='Defense +1', cost=20, damage=0, armor=1),
    Equipment(name='Defense +2', cost=40, damage=0, armor=2),
    Equipment(name='Defense +3', cost=80, damage=0, armor=3),
}

@dataclass
class Player:
    """
    The player, with stats managed via properties which calculate thme automatically from the sum
    of the players' equipment.
    """
    inventory: Set[Equipment]
    hitpoints: int

    @property
    def armor(self) -> int:
        """
        Return the player's armor - equal the sum of the armor given by their equipment.
        """
        return sum(item.armor for item in self.inventory)

    @property
    def damage(self) -> int:
        """
        Return the player's damage - equal the sum of the damage given by their equipment.
        """
        return sum(item.damage for item in self.inventory)

    @property
    def spent(self) -> int:
        """
        Return the total cost of the player's equipment.
        """
        return sum(item.cost for item in self.inventory)

    def hit(self, damage: int) -> bool:
        """
        Deal the given amount of damage to the player, reduced appropriately by their armor.
        Return True if this was sufficient to defeat the player, otherwise False.
        """
        self.hitpoints -= max(1, damage - self.armor)
        return self.hitpoints <= 0

    @classmethod
    def all_possible_loadouts(cls) -> 'Sequence[Player]':
        """
        Calculate and return all possible player loadouts from the predefined equipment.
        """
        weapon_options = tuple(combinations(WEAPONS, 1))
        armor_options = tuple(chain([tuple()], combinations(ARMOR, 1)))
        ring_options = tuple(chain([tuple()], combinations(RINGS, 1), combinations(RINGS, 2)))
        return tuple(
            cls(
                hitpoints=100,
                inventory=set(weapon_option + armor_option + ring_option)
            )
            for weapon_option, armor_option, ring_option
            in product(
                weapon_options, armor_options, ring_options
            )
        )

def fight_won(boss: Boss, player: Player) -> bool:
    """
    Simulate a battle between a given boss and player and determine the winner. Return True if the
    player wins, and False otherwise.
    """
    while True:
        if boss.hit(player.damage):
            return True
        if player.hit(boss.damage):
            return False

def best_win(boss_factory: Callable[[], Boss]) -> Player:
    """
    Calculate the best possible win against a boss from the given factory - i.e. the win that
    involves spending the least on equipment.
    """
    loadouts: Sequence[Player] = Player.all_possible_loadouts()
    return next(
        player
        for player
        in sorted(loadouts, key=lambda p: p.spent)
        if fight_won(boss_factory(), player)
    )

def worst_loss(boss_factory: Callable[[], Boss]) -> Player:
    """
    Calculate the worst possible loss against a boss from the given factory - i.e. the loss that
    involves spending the most on equipment.
    """
    loadouts: Sequence[Player] = Player.all_possible_loadouts()
    return next(
        player
        for player
        in sorted(loadouts, key=lambda p: p.spent, reverse=True)
        if not fight_won(boss_factory(), player)
    )

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=21)
    boss_factory = Boss.get_boss_factory(data)

    print(f'Part 1: {best_win(boss_factory).spent}')
    print(f'Part 2: {worst_loss(boss_factory).spent}')

if __name__ == '__main__':
    main()
