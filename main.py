"""Menu-driven CLI for Synent Task 3."""

from todo import TodoList


def read_task_id() -> int | None:
    value = input("Enter task id: ").strip()
    try:
        return int(value)
    except ValueError:
        print("Please enter a valid numeric task id.")
        return None


def show_tasks(todo: TodoList) -> None:
    tasks = todo.list_all()
    if not tasks:
        print("No tasks yet.")
        return

    print("\nTasks")
    for task in tasks:
        status = "done" if task.done else "pending"
        print(f"{task.id}. [{status}] {task.title}")


def main() -> None:
    todo = TodoList()

    while True:
        print("\nTo-Do List")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark task complete")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Task title: ")
            try:
                task = todo.add(title)
            except ValueError as exc:
                print(exc)
            else:
                print(f"Added task #{task.id}.")
        elif choice == "2":
            show_tasks(todo)
        elif choice == "3":
            task_id = read_task_id()
            if task_id is None:
                continue
            try:
                task = todo.complete(task_id)
            except ValueError as exc:
                print(exc)
            else:
                print(f"Marked task #{task.id} complete.")
        elif choice == "4":
            task_id = read_task_id()
            if task_id is None:
                continue
            try:
                task = todo.delete(task_id)
            except ValueError as exc:
                print(exc)
            else:
                print(f"Deleted task: {task.title}")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Select 1 to 5.")


if __name__ == "__main__":
    main()
