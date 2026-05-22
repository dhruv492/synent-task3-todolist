"""Reusable to-do list storage and operations."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


class TodoList:
    def __init__(self, storage_path: str | Path = "tasks.json") -> None:
        self.storage_path = Path(storage_path)
        self.tasks: list[Task] = []
        self.load()

    def load(self) -> None:
        if not self.storage_path.exists():
            self.tasks = []
            return

        with self.storage_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        self.tasks = [Task(**item) for item in data]

    def save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump([asdict(task) for task in self.tasks], file, indent=2)

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")

        next_id = max((task.id for task in self.tasks), default=0) + 1
        task = Task(id=next_id, title=title)
        self.tasks.append(task)
        self.save()
        return task

    def list_all(self) -> list[Task]:
        return list(self.tasks)

    def complete(self, task_id: int) -> Task:
        task = self._find(task_id)
        task.done = True
        self.save()
        return task

    def delete(self, task_id: int) -> Task:
        task = self._find(task_id)
        self.tasks = [item for item in self.tasks if item.id != task_id]
        self.save()
        return task

    def _find(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"No task found with id {task_id}.")
