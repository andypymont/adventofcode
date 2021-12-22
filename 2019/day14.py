"""
2019 Day 14
https://adventofcode.com/2019/day/14
"""

from functools import partial
from math import ceil, floor
from typing import Callable, Dict, List, Set, Tuple
import aocd  # type: ignore

MaterialQty = Tuple[str, int]
Recipes = Dict[str, Tuple[int, Set[MaterialQty]]]


def read_ingredient(ingredient: str) -> MaterialQty:
    parts = ingredient.split(" ")
    return parts[1], int(parts[0])


def read_recipe_side(side: str) -> List[MaterialQty]:
    return [read_ingredient(ing) for ing in side.split(", ")]


def read_recipe_line(line: str) -> Tuple[List[MaterialQty], List[MaterialQty]]:
    sides = [read_recipe_side(side) for side in line.split(" => ")]
    return sides[0], sides[1]


def read_recipes(text: str) -> Recipes:
    return {
        right[0][0]: (right[0][1], set(left))
        for left, right in [read_recipe_line(line) for line in text.split("\n")]
    }


def resolve_need(
    element: str, inventory: Dict[str, int], recipes: Recipes
) -> Dict[str, int]:
    reacted = dict(inventory)
    need = -inventory[element]

    if need > 0 and element in recipes:
        qty, ingredients = recipes[element]
        repetitions = ceil(need / qty)
        reacted[element] = reacted.get(element, 0) + (repetitions * qty)
        for (ing_element, ing_qty) in ingredients:
            reacted[ing_element] = reacted.get(ing_element, 0) - (repetitions * ing_qty)

    return reacted


def ore_required(recipes: Recipes, fuel: int = 1) -> int:
    inventory = {"FUEL": -fuel}
    needs = ["FUEL"]
    while len(needs) > 0:
        inventory = resolve_need(needs[0], inventory, recipes)
        needs = [
            element
            for element, qty in inventory.items()
            if element != "ORE" and qty < 0
        ]
    return -inventory["ORE"]


def binary_search(
    func: Callable[[int], int], target: int, lower: int, upper: int
) -> int:
    while lower <= upper:
        mid = floor((lower + upper) / 2)
        attempt = func(mid)
        if attempt < target:
            lower = mid + 1
        elif attempt > target:
            upper = mid - 1
        else:
            return mid
    return upper


def exponential_search(func: Callable[[int], int], target: int) -> int:
    bound = 1
    while func(bound) < target:
        bound *= 2
    return binary_search(func, target, bound // 2, bound + 1)


def fuel_from_trillion_ore(recipes: Recipes) -> int:
    return exponential_search(partial(ore_required, recipes), 1_000_000_000_000)


def test_part1() -> None:
    """
    Examples for Part 1.
    """
    text = "\n".join(
        (
            "10 ORE => 10 A",
            "1 ORE => 1 B",
            "7 A, 1 B => 1 C",
            "7 A, 1 C => 1 D",
            "7 A, 1 D => 1 E",
            "7 A, 1 E => 1 FUEL",
        )
    )
    eg1 = {
        "A": (10, {("ORE", 10)}),
        "B": (1, {("ORE", 1)}),
        "C": (1, {("A", 7), ("B", 1)}),
        "D": (1, {("A", 7), ("C", 1)}),
        "E": (1, {("A", 7), ("D", 1)}),
        "FUEL": (1, {("A", 7), ("E", 1)}),
    }
    assert read_recipes(text) == eg1
    assert ore_required(eg1) == 31
    eg2 = {
        "A": (2, {("ORE", 9)}),
        "B": (3, {("ORE", 8)}),
        "C": (5, {("ORE", 7)}),
        "AB": (1, {("A", 3), ("B", 4)}),
        "BC": (1, {("B", 5), ("C", 7)}),
        "CA": (1, {("C", 4), ("A", 1)}),
        "FUEL": (1, {("AB", 2), ("BC", 3), ("CA", 4)}),
    }
    assert ore_required(eg2) == 165
    eg3 = {
        "STKFG": (1, {("VPVL", 2), ("FWMGM", 7), ("CXFTF", 2), ("MNCFX", 11)}),
        "VPVL": (8, {("NVRVD", 17), ("JNWZP", 3)}),
        "FUEL": (
            1,
            {
                ("STKFG", 53),
                ("MNCFX", 6),
                ("VJHF", 46),
                ("HVMC", 81),
                ("CXFTF", 68),
                ("GNMV", 25),
            },
        ),
        "FWMGM": (5, {("VJHF", 22), ("MNCFX", 37)}),
        "NVRVD": (4, {("ORE", 139)}),
        "JNWZP": (7, {("ORE", 144)}),
        "HVMC": (
            3,
            {("MNCFX", 5), ("RFSQX", 7), ("FWMGM", 2), ("VPVL", 2), ("CXFTF", 19)},
        ),
        "GNMV": (6, {("VJHF", 5), ("MNCFX", 7), ("VPVL", 9), ("CXFTF", 37)}),
        "MNCFX": (6, {("ORE", 145)}),
        "CXFTF": (8, {("NVRVD", 1)}),
        "RFSQX": (4, {("VJHF", 1), ("MNCFX", 6)}),
        "VJHF": (6, {("ORE", 176)}),
    }
    assert ore_required(eg3) == 180697


def test_part2() -> None:
    """
    Examples for Part 2.
    """
    eg3 = {
        "STKFG": (1, {("VPVL", 2), ("FWMGM", 7), ("CXFTF", 2), ("MNCFX", 11)}),
        "VPVL": (8, {("NVRVD", 17), ("JNWZP", 3)}),
        "FUEL": (
            1,
            {
                ("STKFG", 53),
                ("MNCFX", 6),
                ("VJHF", 46),
                ("HVMC", 81),
                ("CXFTF", 68),
                ("GNMV", 25),
            },
        ),
        "FWMGM": (5, {("VJHF", 22), ("MNCFX", 37)}),
        "NVRVD": (4, {("ORE", 139)}),
        "JNWZP": (7, {("ORE", 144)}),
        "HVMC": (
            3,
            {("MNCFX", 5), ("RFSQX", 7), ("FWMGM", 2), ("VPVL", 2), ("CXFTF", 19)},
        ),
        "GNMV": (6, {("VJHF", 5), ("MNCFX", 7), ("VPVL", 9), ("CXFTF", 37)}),
        "MNCFX": (6, {("ORE", 145)}),
        "CXFTF": (8, {("NVRVD", 1)}),
        "RFSQX": (4, {("VJHF", 1), ("MNCFX", 6)}),
        "VJHF": (6, {("ORE", 176)}),
    }
    assert fuel_from_trillion_ore(eg3) == 5586022


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2019, day=14)
    recipes = read_recipes(data)

    print(f"Part 1: {ore_required(recipes)}")
    print(f"Part 2: {fuel_from_trillion_ore(recipes)}")


if __name__ == "__main__":
    main()
