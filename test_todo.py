import tempfile
import unittest
from pathlib import Path

from todo import TodoList


class TodoListTests(unittest.TestCase):
    def test_add_complete_delete_task(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd(), prefix=".test-") as temp_dir:
            todo = TodoList(Path(temp_dir) / "tasks.json")

            task = todo.add("Submit internship project")
            self.assertEqual(task.id, 1)
            self.assertFalse(task.done)

            completed = todo.complete(task.id)
            self.assertTrue(completed.done)

            deleted = todo.delete(task.id)
            self.assertEqual(deleted.title, "Submit internship project")
            self.assertEqual(todo.list_all(), [])

    def test_persists_tasks_to_json(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd(), prefix=".test-") as temp_dir:
            storage = Path(temp_dir) / "tasks.json"
            TodoList(storage).add("Record demo video")

            reloaded = TodoList(storage)
            self.assertEqual(len(reloaded.list_all()), 1)
            self.assertEqual(reloaded.list_all()[0].title, "Record demo video")

    def test_empty_title_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd(), prefix=".test-") as temp_dir:
            todo = TodoList(Path(temp_dir) / "tasks.json")
            with self.assertRaises(ValueError):
                todo.add("   ")


if __name__ == "__main__":
    unittest.main()
