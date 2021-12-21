"""
2021 Day 21
https://adventofcode.com/2021/day/21
"""

from functools import lru_cache
from itertools import cycle
from typing import Tuple
import aocd # type: ignore

def read_starting_positions(text: str) -> Tuple[int, int]:
    lines = text.split('\n')
    return (
        int(lines[0].split(': ')[-1]) - 1,
        int(lines[1].split(': ')[-1]) - 1,
    )

def play_deterministic_game(p1_pos: int, p2_pos: int) -> Tuple[int, int, int]:
    positions = [p1_pos, p2_pos]
    scores = [0, 0]
    player = 0

    die = cycle(range(1, 101))
    roll_count = 0

    while scores[0] < 1000 and scores[1] < 1000:
        positions[player] = (positions[player] + next(die) + next(die) + next(die)) % 10
        roll_count += 3
        scores[player] += positions[player] + 1
        player = 1 if player == 0 else 0

    return scores[0], scores[1], roll_count

ROLLS = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}

@lru_cache
def play_all_games(p1_pos: int, p2_pos: int, p1_score: int, p2_score: int) -> Tuple[int, int]:
    if p1_score >= 21:
        return 1, 0
    if p2_score >= 21:
        return 0, 1

    p1_wins = p2_wins = 0

    for p1_roll, p1_rollqty in ROLLS.items():
        p1_newpos = (p1_pos + p1_roll) % 10
        p1_newscore = p1_score + p1_newpos + 1
        if p1_newscore >= 21:
            p1_wins += p1_rollqty
            continue
        for p2_roll, p2_rollqty in ROLLS.items():
            p2_newpos = (p2_pos + p2_roll) % 10
            p1_won, p2_won = play_all_games(
                p1_newpos,
                p2_newpos,
                p1_newscore,
                p2_score + p2_newpos + 1
            )
            p1_wins += (p1_won * p1_rollqty * p2_rollqty)
            p2_wins += (p2_won * p1_rollqty * p2_rollqty)

    return p1_wins, p2_wins

def test_part1() -> None:
    """
    Examples for Part 1.
    """
    assert read_starting_positions('\n'.join((
        'Player 1 starting position: 4',
        'Player 2 starting position: 8',
    ))) == (3, 7)
    assert play_deterministic_game(3, 7) == (1000, 745, 993)

def test_part2() -> None:
    """
    Examples for Part 2.
    """
    assert play_all_games(3, 7, 0, 0) == (444356092776315, 341960390180808)

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2021, day=21)
    p1_pos, p2_pos = read_starting_positions(data)

    p1_score, p2_score, rolls = play_deterministic_game(p1_pos, p2_pos)
    part1 = min(p1_score, p2_score) * rolls
    print(f'Part 1: {part1}')

    p1_wins, p2_wins = play_all_games(p1_pos, p2_pos, 0, 0)
    part2 = max(p1_wins, p2_wins)
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
