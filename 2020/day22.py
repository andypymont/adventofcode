"""
2020 Day 22
https://adventofcode.com/2020/day/22
"""

from typing import List, Sequence, Tuple
import aocd # type: ignore

Deck = List[int]

def read_decks(text: str) -> Sequence[Deck]:
    return [[int(card) for card in deck.split('\n')[1:]] for deck in text.split('\n\n')]

def play_game(decks: Sequence[Deck]) -> Tuple[Deck, Deck]:
    one, two = decks

    while len(one) > 0 and len(two) > 0:
        if one[0] > two[0]:
            one, two = one[1:] + [one[0], two[0]], two[1:]
        else:
            one, two = one[1:], two[1:] + [two[0], one[0]]

    return one, two

def score(deck: Deck) -> int:
    return sum(card*(len(deck)-position) for position, card in enumerate(deck))

def play_recursive_game(decks: Sequence[Deck]) -> Tuple[Tuple[Deck, Deck], int]:
    one, two = decks
    rounds = set()

    while len(one) > 0 and len(two) > 0:

        # if we've been in this state before in this game, player 1 wins
        state = (tuple(one), tuple(two))
        if state in rounds:
            return (one, two), 1
        rounds.add(state)

        # if players have large enough decks to recurse, then we do
        card_one, card_two = one[0], two[0]
        if len(one) > card_one and len(two) > card_two:
            _, winner = play_recursive_game((one[1:card_one+1], two[1:card_two+1]))

        # and if not, we just compare the cards as usual
        else:
            winner = 1 if card_one > card_two else 2

        # ...and either way, we update the decks accordingly
        winning_card = card_one if winner == 1 else card_two
        non_winning_card = card_one if winner == 2 else card_two

        if winner == 1:
            one, two = one[1:] + [winning_card, non_winning_card], two[1:]
        else:
            one, two = one[1:], two[1:] + [winning_card, non_winning_card]

    return (one, two), 1 if len(one) > 0 else 2

def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=22)

    decks = read_decks(data)
    result = play_game(decks)
    print(f'Part 1: {sum(score(deck) for deck in result)}')

    decks2, _ = play_recursive_game(decks)
    print(f'Part 2: {sum(score(deck) for deck in decks2)}')

if __name__ == '__main__':
    main()
