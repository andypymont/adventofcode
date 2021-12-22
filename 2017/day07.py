"""
2017 Day 7
https://adventofcode.com/2017/day/7
"""

from dataclasses import dataclass
from typing import Dict, Sequence, Set, Tuple
import aocd  # type: ignore
import regex as re  # type: ignore


@dataclass(frozen=True)
class Node:
    name: str
    weight: int
    children: Tuple["Node", ...]

    @classmethod
    def from_node_info(
        cls, weights: Dict[str, int], children: Dict[str, Sequence[str]], name: str
    ) -> "Node":
        directchildren = tuple(
            cls.from_node_info(weights, children, childname)
            for childname in children.get(name, [])
        )
        return cls(name, weights.get(name, 0), directchildren)

    @property
    def child_weights(self) -> Sequence[int]:
        return [child.total_weight for child in self.children]

    @property
    def total_weight(self) -> int:
        return self.weight + sum(self.child_weights)


def find_bottom(weights: Dict[str, int], children: Dict[str, Sequence[str]]) -> str:
    all_children: Set[str] = set()
    for directchildren in children.values():
        all_children = all_children.union(directchildren)

    all_nodes = set(weights.keys())

    return next(iter(all_nodes.difference(all_children)))


RE_WEIGHTS = re.compile(r"(\w+) \((\d+)\)")
RE_CHILDREN = re.compile(r"(\w+) \(\d+\) -> ([\w, ]+)")


def read_tower(text: str) -> Node:
    weights: Dict[str, int] = {
        str(name): int(weight) for name, weight in RE_WEIGHTS.findall(text)
    }
    children: Dict[str, Sequence[str]] = {
        str(name): str(children).split(", ")
        for name, children in RE_CHILDREN.findall(text)
    }
    bottom = find_bottom(weights, children)
    return Node.from_node_info(weights, children, bottom)


def correct_weight(node: Node, correction: int = 0) -> int:
    child_weights = node.child_weights

    def is_standard_weight(weight: int) -> bool:
        return sum(1 for cw in child_weights if cw == weight) > 1

    standard_weights = [cw for cw in child_weights if is_standard_weight(cw)]
    non_standard_weights = [cw for cw in child_weights if not is_standard_weight(cw)]

    if len(non_standard_weights) == 0:
        return node.weight + correction

    node_to_correct = next(
        child
        for ix, child in enumerate(node.children)
        if child_weights[ix] == non_standard_weights[0]
    )

    return correct_weight(
        node_to_correct, standard_weights[0] - non_standard_weights[0]
    )


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2017, day=7)
    base = read_tower(data)

    print(f"Part 1: {base.name}")
    print(f"Part 2: {correct_weight(base)}")


if __name__ == "__main__":
    main()
