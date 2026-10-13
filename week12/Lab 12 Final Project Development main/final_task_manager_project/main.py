# final-task-manager-project/main.py
import sys
import os

# Add the 'src' directory to Python's module search path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from task_manager import TaskManager
from cli_interface import CLIInterface


def main():
    """
    Main entry point for the Enhanced Task Manager application.
    Initializes TaskManager and CLIInterface, then starts the CLI loop.
    """
    manager = TaskManager()
    cli = CLIInterface(manager)
    cli.run()


if __name__ == "__main__":
    main()
