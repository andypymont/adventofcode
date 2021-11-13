"""
2015 Day 15
https://adventofcode.com/2015/day/15
"""

from itertools import combinations_with_replacement
from math import prod
from typing import Dict, Iterable, Sequence
import aocd # type: ignore

Ingredient = Dict[str, int]
AvailableIngredients = Dict[str, Ingredient]
Cookie = Sequence[Ingredient]

def read_ingredients(description: str) -> AvailableIngredients:
    """
    Read the set of available ingredients and their properties from the puzzle description.
    """
    ingredients: AvailableIngredients = {}

    for line in description.split('\n'):
        name, properties = line.split(': ')
        ingredient: Ingredient = {}
        for prop in properties.split(', '):
            words = prop.split(' ')
            ingredient[words[0]] = int(words[1])
        ingredients[name] = ingredient

    return ingredients

PROPS: Sequence[str] = ('calories', 'capacity', 'durability', 'flavor', 'texture')
def score_cookie(cookie: Cookie, exact_calories: int = -1) -> int:
    """
    Calculate the score of a cookie containing the given teaspoons of ingredient.
    """
    totals = {}
    for prop in PROPS:
        total = sum(teaspoon.get(prop, 0) for teaspoon in cookie)
        totals[prop] = total if total > 0 else 0
    if exact_calories >= 0 and totals['calories'] != exact_calories:
        return 0
    return prod(totals[prop] for prop in PROPS if prop != 'calories')

def all_possible_cookies(ingredients: AvailableIngredients) -> Iterable[Cookie]:
    """
    Calculate all possible cookie recipes using a given sequence of available ingredients.
    """
    return combinations_with_replacement(ingredients.values(), 100)

def best_possible_cookie_score(ingredients: AvailableIngredients, exact_calories: int = -1) -> int:
    """
    Calculate the best possible cookie score given the available ingredients.
    """
    return max(
        score_cookie(cookie, exact_calories)
        for cookie
        in all_possible_cookies(ingredients)
    )

def test_example():
    """
    Example from the puzzle description.
    """
    example_description = '\n'.join((
        'Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8',
        'Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3',
    ))
    example_ingredients: AvailableIngredients = {
        'Butterscotch': {
            'capacity': -1,
            'durability': -2,
            'flavor': 6,
            'texture': 3,
            'calories': 8
        },
        'Cinnamon': {
            'capacity': 2,
            'durability': 3,
            'flavor': -2,
            'texture': -1,
            'calories': 3
        }
    }
    assert read_ingredients(example_description) == example_ingredients
    assert best_possible_cookie_score(example_ingredients) == 62_842_880

def main():
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2015, day=15)
    ingredients = read_ingredients(data)

    print(f'Part 1: {best_possible_cookie_score(ingredients)}')
    print(f'Part 2: {best_possible_cookie_score(ingredients, exact_calories=500)}')

if __name__ == '__main__':
    main()
