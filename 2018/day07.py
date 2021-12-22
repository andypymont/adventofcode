"""
2018 Day 7
https://adventofcode.com/2018/day/7
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple
import re
import aocd  # type: ignore

RE_TASK = re.compile(r"Step (\w) must be finished before step (\w) can begin.")


@dataclass(frozen=True, order=True)
class Task:
    name: str
    prerequisites: frozenset[str]

    @property
    def time_to_complete(self) -> int:
        return ord(self.name) - 4

    def can_begin(self, completed: Iterable[str]) -> bool:
        return all(prereq in completed for prereq in self.prerequisites)

    @classmethod
    def all_from_text(cls, text: str) -> List["Task"]:
        prereqs: Dict[str, Set[str]] = {}
        for (prereq, step) in RE_TASK.findall(text):
            if prereq not in prereqs:
                prereqs[prereq] = set()
            if step not in prereqs:
                prereqs[step] = set()
            prereqs[step].add(prereq)
        return sorted(
            [Task(name, frozenset(prereqset)) for (name, prereqset) in prereqs.items()]
        )


@dataclass
class Worker:
    task: Optional[Task]
    time_spent: int

    def __init__(self) -> None:
        self.assign(None)

    def assign(self, task: Optional[Task]) -> None:
        self.task = task
        self.time_spent = 0

    def progress(self) -> Optional[Task]:
        if self.task:
            self.time_spent += 1
            if self.time_spent == self.task.time_to_complete:
                completed = self.task
                self.assign(None)
                return completed
        return None


def complete_all_tasks(tasklist: List[Task], workercount: int) -> Tuple[int, str]:
    time = 0
    order: List[str] = []
    workers = [Worker() for w in range(workercount)]

    while len(order) < len(tasklist):
        # assign idle workers to ready tasks
        unassigned = [worker for worker in workers if worker.task is None]
        in_progress = {worker.task for worker in workers}
        ready = sorted(
            task
            for task in tasklist
            if task not in in_progress
            and task.name not in order
            and task.can_begin(order)
        )
        for (worker, task) in zip(unassigned, ready):
            worker.assign(task)

        # advance time on all tasks
        time += 1
        for completed_task in [worker.progress() for worker in workers]:
            if completed_task:
                order.append(completed_task.name)

    return (time, "".join(order))


def main() -> None:
    """
    Calculate and output the solutions based on the real puzzle input.
    """
    data = aocd.get_data(year=2018, day=7)
    tasks = Task.all_from_text(data)

    _, part1 = complete_all_tasks(tasks, 1)
    print(f"Part 1: {part1}")

    part2, _ = complete_all_tasks(tasks, 5)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
