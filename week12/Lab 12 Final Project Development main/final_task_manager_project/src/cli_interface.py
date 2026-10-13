# final-task-manager-project/src/cli_interface.py
import datetime


class CLIInterface:
    """
    Handles all command-line interface interactions: displaying menus,
    taking user input, and displaying output.
    Does NOT contain business logic directly; calls methods on TaskManager.
    """
    def __init__(self, task_manager):
        self.manager = task_manager

    def display_menu(self):
        print("\n==================================")
        print("--- Enhanced Task Manager Menu ---")
        print("==================================")
        print("1. Add Normal Task")
        print("2. Add Due Date Task")
        print("3. Add Priority Task")
        print("4. List All Tasks")
        print("5. Complete Task")
        print("6. Delete Task")
        print("7. Search Tasks")
        print("8. Filter Tasks")
        print("9. Sort Tasks")
        print("0. Exit")
        print("----------------------------------")

    def get_user_choice(self):
        return input("Enter your choice (0-9): ").strip()

    def get_task_description(self):
        while True:
            description = input("Enter task description: ").strip()
            if description:
                return description
            print("Task description cannot be empty. Please try again.")

    def get_due_date_input(self):
        while True:
            due_date_str = input("Enter due date (YYYY-MM-DD): ").strip()
            try:
                datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
                return due_date_str
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD (e.g., 2026-12-31).")

    def get_priority_input(self):
        while True:
            priority = input("Enter priority (High/Medium/Low): ").strip().capitalize()
            if priority in ["High", "Medium", "Low"]:
                return priority
            print("Invalid priority. Please enter 'High', 'Medium', or 'Low'.")

    def get_tags_input(self):
        tags_str = input("Enter tags (comma-separated, e.g., study,project,urgent - optional): ").strip()
        return [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()] if tags_str else []

    def _display_tasks(self, tasks, title="Tasks"):
        if not tasks:
            print(f"\n[Info] No {title.lower()} found.")
            return

        print(f"\n--- {title} (Total: {len(tasks)}) ---")
        for task in tasks:
            print(f"  * {task}")
        print("------------------------------------------")

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                description = self.get_task_description()
                tags = self.get_tags_input()
                new_task = self.manager.add_normal_task(description, tags=tags)
                print(f"[Success] Normal Task '{new_task.description}' added with ID {new_task.id}.")

            elif choice == '2':
                description = self.get_task_description()
                due_date_str = self.get_due_date_input()
                tags = self.get_tags_input()
                new_task = self.manager.add_due_date_task(description, due_date_str, tags=tags)
                if new_task:
                    print(f"[Success] Due Date Task '{new_task.description}' (Due: {new_task.due_date.strftime('%Y-%m-%d')}) added with ID {new_task.id}.")
                else:
                    print("[Error] Failed to add Due Date Task. Please check your input.")

            elif choice == '3':
                description = self.get_task_description()
                priority = self.get_priority_input()
                tags = self.get_tags_input()
                new_task = self.manager.add_priority_task(description, priority, tags=tags)
                if new_task:
                    print(f"[Success] Priority Task '{new_task.description}' (Priority: {new_task.priority}) added with ID {new_task.id}.")
                else:
                    print("[Error] Failed to add Priority Task. Please check your input.")

            elif choice == '4':
                tasks = self.manager.get_all_tasks()
                self._display_tasks(tasks, "Your Tasks")

            elif choice == '5':
                try:
                    task_id = int(input("Enter ID of task to complete: ").strip())
                    success, message = self.manager.complete_task(task_id)
                    prefix = "[Success]" if success else "[Notice]"
                    print(f"{prefix} {message}")
                except ValueError:
                    print("[Error] Invalid input. Please enter a valid number for Task ID.")

            elif choice == '6':
                try:
                    task_id = int(input("Enter ID of task to delete: ").strip())
                    success, message = self.manager.delete_task(task_id)
                    prefix = "[Success]" if success else "[Notice]"
                    print(f"{prefix} {message}")
                except ValueError:
                    print("[Error] Invalid input. Please enter a valid number for Task ID.")

            elif choice == '7':
                keyword = input("Enter search keyword (in description or tags): ").strip()
                found_tasks = self.manager.search_tasks(keyword)
                self._display_tasks(found_tasks, f"Search Results for '{keyword}'")

            elif choice == '8':
                print("\n--- Filter Tasks (Press Enter to skip any filter) ---")
                status_input = input("Filter by completed status (yes/no, leave blank for all): ").strip().lower()
                status = None
                if status_input == 'yes':
                    status = True
                elif status_input == 'no':
                    status = False

                due_before_str = input("Filter by due date before (YYYY-MM-DD, leave blank for all): ").strip()
                due_date_before = None
                if due_before_str:
                    try:
                        due_date_before = datetime.datetime.strptime(due_before_str, '%Y-%m-%d').date()
                    except ValueError:
                        print("[Warning] Invalid 'due date before' format. Ignoring.")
                        due_date_before = None

                due_after_str = input("Filter by due date after (YYYY-MM-DD, leave blank for all): ").strip()
                due_date_after = None
                if due_after_str:
                    try:
                        due_date_after = datetime.datetime.strptime(due_after_str, '%Y-%m-%d').date()
                    except ValueError:
                        print("[Warning] Invalid 'due date after' format. Ignoring.")
                        due_date_after = None

                priority_input = input("Filter by priority (High/Medium/Low, leave blank for all): ").strip().capitalize()
                priority_level = priority_input if priority_input in ["High", "Medium", "Low"] else None

                tags_input = input("Filter by tags (comma-separated, task must have ALL specified tags, leave blank for all): ").strip()
                contains_tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()] if tags_input else None

                filtered_tasks = self.manager.filter_tasks(
                    status=status,
                    due_date_before=due_date_before,
                    due_date_after=due_date_after,
                    priority_level=priority_level,
                    contains_tags=contains_tags
                )
                self._display_tasks(filtered_tasks, "Filtered Tasks")

            elif choice == '9':
                print("\n--- Sort Tasks ---")
                print("Available criteria: id, description, completed, due_date, priority")
                criterion = input("Sort by (default: id): ").strip().lower() or "id"
                reverse_str = input("Reverse order (yes/no, default: no): ").strip().lower()
                reverse = (reverse_str == 'yes')

                sorted_tasks = self.manager.sort_tasks(criterion, reverse)
                direction = "Descending" if reverse else "Ascending"
                self._display_tasks(sorted_tasks, f"Sorted Tasks by {criterion} ({direction})")

            elif choice == '0':
                print("\nExiting Task Manager. Goodbye and good luck with your final project presentation!")
                break
            else:
                print("[Error] Invalid choice. Please enter a number between 0 and 9.")
