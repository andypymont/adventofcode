"""
2015 Day 22
https://adventofcode.com/2015/day/22
"""

from dataclasses import dataclass
from typing import Dict, Set
import aocd # type: ignore

@dataclass(frozen=True)
class Effects:
    """
    Effects which are currently active in a battle situation.
    """
    shield: int
    poison: int
    recharge: int

    def __add__(self, other: 'Effects') -> 'Effects':
        return self.__class__(
            self.shield + other.shield,
            self.poison + other.poison,
            self.recharge + other.recharge
        )

    def progress(self) -> 'Effects':
        """
        Progress to the next turn by reducing all effects by 1, to a minimum of 0.
        """
        return self.__class__(
            max(0, self.shield - 1),
            max(0, self.poison - 1),
            max(0, self.recharge - 1)
        )
NO_EFFECTS = Effects(0, 0, 0)

@dataclass(frozen=True)
class Spell:
    """
    Simple container class for properties of a spell.
    """
    cost: int
    damage: int
    heal: int
    shield: int
    poison: int
    recharge: int

    def is_castable(self, situation: 'Situation') -> bool:
        """
        Return True if this spell is castable in the given situation, and False otherwise.
        """
        return (
            situation.available_mana >= self.cost
            and not (situation.effects.shield > 1 and self.shield > 0)
            and not (situation.effects.poison > 1 and self.poison > 0)
            and not (situation.effects.recharge > 1 and self.recharge > 0)
        )

    @property
    def effects(self) -> Effects:
        """
        Return an Effects object with the special (non-direct-damage) effects of this spell.
        """
        return Effects(self.shield, self.poison, self.recharge)

@dataclass(frozen=True)
class Situation:
    """
    Current situation in a boss battle.
    """
    player_hp: int
    boss_hp: int
    boss_damage: int
    mana: int
    mana_spent: int
    effects: Effects

    @classmethod
    def read_from_input(cls, text: str) -> 'Situation':
        """
        Read the initial situation from the puzzle input.
        """
        from_text: Dict[str, int] = {
            first.lower(): int(second)
            for first, second
            in (
                line.split(': ') for line in text.split('\n')
            )
        }
        return cls(
            player_hp=50,
            boss_hp=from_text.get('hit points', 0),
            boss_damage=from_text.get('damage', 0),
            mana=500,
            mana_spent=0,
            effects=Effects(shield=0, recharge=0, poison=0)
        )

    @property
    def game_over(self) -> bool:
        """
        Return True if either the boss or player has been reduced to 0 HP, otherwise False.
        """
        return self.boss_hp <= 0 or self.player_hp <= 0

    @property
    def game_won(self) -> bool:
        """
        Return True if the player has won - i.e. the boss has 0 HP and the player still has HP
        remaining.
        """
        return self.boss_hp <= 0 < self.player_hp

    @property
    def game_lost(self) -> bool:
        """
        Return True if the player has lost - i.e. has 0 HP remaining.
        """
        return self.player_hp <= 0

    @property
    def armor(self) -> int:
        """
        Return the player's current armor value, based on whether a shield effect is active.
        """
        return 7 if self.effects.shield > 0 else 0

    @property
    def poison(self) -> int:
        """
        Return the amount of poison damage to deal this turn, based on whether a poison effect is
        active.
        """
        return 3 if self.effects.poison > 0 else 0

    @property
    def recharge(self) -> int:
        """
        Return the amount of mana to recharge this turn, based on whether a recharge effect is
        active.
        """
        return 101 if self.effects.recharge > 0 else 0

    @property
    def available_mana(self) -> int:
        """
        Return the amount of mana available to spend this turn - i.e. the current mana plus any
        that will be recharged by an active effect.
        """
        return self.mana + self.recharge

def turn(
    situation: Situation,
    damage_player: int = 0,
    damage_boss: int = 0,
    spend_mana: int = 0,
    new_effects: Effects = NO_EFFECTS
) -> Situation:
    """
    Resolve a turn in the battle, returning the new situation.
    """
    # start of turn effects resolve:
    boss_hp = situation.boss_hp - situation.poison
    damage_player = 0 if boss_hp <= 0 else damage_player

    # then resolve the boss attack or spell:
    return Situation(
        situation.player_hp - damage_player,
        boss_hp - damage_boss,
        situation.boss_damage,
        situation.mana + situation.recharge - spend_mana,
        situation.mana_spent + spend_mana,
        situation.effects.progress() + new_effects
    )

def boss_turn(situation: Situation) -> Situation:
    """
    Calculate and resolve the boss's next turn for the given situation, returning the new
    situation.
    """
    damage_dealt = max(1, situation.boss_damage - situation.armor)
    return turn(situation, damage_player=damage_dealt)

def player_turn(situation: Situation, spell: Spell, difficulty: int) -> Situation:
    """
    Calculate and resolve the player's next turn for the given situation, returning the new
    situation.
    """
    return turn(
        situation,
        damage_player=(difficulty - spell.heal),
        damage_boss=spell.damage,
        spend_mana=spell.cost,
        new_effects=spell.effects
    )

SPELLBOOK: Dict[str, Spell] = {
    'missile': Spell(cost=53, damage=4, heal=0, shield=0, poison=0, recharge=0),
    'drain': Spell(cost=73, damage=2, heal=2, shield=0, poison=0, recharge=0),
    'shield': Spell(cost=113, damage=0, heal=0, shield=6, poison=0, recharge=0),
    'poison': Spell(cost=173, damage=0, heal=0, shield=0, poison=6, recharge=0),
    'recharge': Spell(cost=229, damage=0, heal=0, shield=0, poison=0, recharge=5),
}

def available_moves(situation: Situation, difficulty: int) -> Set[Situation]:
    """
    Calculate and return the set of all possible moves from the given situation.
    """
    return set(
        player_turn(situation, spell, difficulty)
        for spell in SPELLBOOK.values()
        if spell.is_castable(situation)
    )

def find_cheapest_win(initial_situation: Situation, difficulty: int = 0) -> int:
    """
    Find the least amount of mana that can be spent whilst still achieving victory, given the
    provided starting situation.
    """
    candidates = list(available_moves(initial_situation, difficulty))
    visited = set(candidates)

    while candidates:
        candidates.sort(key=lambda sit: sit.mana_spent, reverse=True)
        candidate = candidates.pop()

        if candidate.game_won:
            return candidate.mana_spent

        if not candidate.game_lost:
            after_boss = boss_turn(candidate)

            if after_boss.game_won: # e.g. due to poison damage
                return after_boss.mana_spent

            if not after_boss.game_lost:
                for move in available_moves(after_boss, difficulty):
                    if move not in visited:
                        visited.add(move)
                        candidates.append(move)

    return -1

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=22)
    initial = Situation.read_from_input(data)

    print(f'Part 1: {find_cheapest_win(initial)}')
    print(f'Part 2: {find_cheapest_win(initial, difficulty=1)}')

if __name__ == '__main__':
    main()
