"""
2020 Day 21
https://adventofcode.com/2020/day/21
"""

from functools import reduce
from itertools import chain
from operator import __and__ as intersection
from typing import Dict, Sequence, Set, Tuple
import regex as re  # type: ignore
import aocd  # type: ignore

Recipe = Tuple[Set[str], Set[str]]

RE_RECIPE = re.compile(r"([\w ]+) \(contains ([\w, ]+)\)")


def read_recipes(text: str) -> Sequence[Recipe]:
    return tuple(
        (set(ingredients.split()), set(allergens.replace(",", "").split()))
        for ingredients, allergens in RE_RECIPE.findall(text)
    )


def all_allergens(recipes: Sequence[Recipe]) -> Set[str]:
    return set(chain(*[allergens for ingredients, allergens in recipes]))


def all_ingredients(recipes: Sequence[Recipe]) -> Set[str]:
    return set(chain(*[ingredients for ingredients, allergens in recipes]))


def potential_allergen_ingredients(
    recipes: Sequence[Recipe], allergen: str
) -> Set[str]:
    return reduce(
        intersection,
        [ingredients for ingredients, allergens in recipes if allergen in allergens],
    )


def find_non_allergen_ingredients(recipes: Sequence[Recipe]) -> Set[str]:
    return all_ingredients(recipes) - set(
        chain(
            *[
                potential_allergen_ingredients(recipes, allergen)
                for allergen in all_allergens(recipes)
            ]
        )
    )


def count_ingredient_occurrences(recipes: Sequence[Recipe], ingredient: str) -> int:
    return sum(1 for ingredients, allergens in recipes if ingredient in ingredients)


def total_non_allergen_ingredient_occurrences(recipes: Sequence[Recipe]) -> int:
    return sum(
        count_ingredient_occurrences(recipes, ingredient)
        for ingredient in find_non_allergen_ingredients(recipes)
    )


def find_allergen_ingredients(recipes: Sequence[Recipe]) -> Dict[str, str]:
    allergen_ingredients = dict(
        (allergen, potential_allergen_ingredients(recipes, allergen))
        for allergen in all_allergens(recipes)
    )
    while max(len(ingredients) for ingredients in allergen_ingredients.values()) > 1:
        identified = set(
            chain(
                *[
                    ingredients
                    for ingredients in allergen_ingredients.values()
                    if len(ingredients) == 1
                ]
            )
        )
        for allergen, ingredients in allergen_ingredients.items():
            if len(ingredients) > 1:
                allergen_ingredients[allergen] = ingredients - identified

    return {
        allergen: tuple(ingredients)[0]
        for allergen, ingredients in allergen_ingredients.items()
    }


def dangerous_ingredient_list(recipes: Sequence[Recipe]) -> str:
    dangerous_ingredients = find_allergen_ingredients(recipes)
    return ",".join(
        dangerous_ingredients[allergen]
        for allergen in sorted(dangerous_ingredients.keys())
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2020, day=21)
    recipes = read_recipes(data)

    print(f"Part 1: {total_non_allergen_ingredient_occurrences(recipes)}")
    print(f"Part 2: {dangerous_ingredient_list(recipes)}")


if __name__ == "__main__":
    main()
