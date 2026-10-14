# final-task-manager-project/src/task.py
import datetime


class Task:
    """
    Base class for all tasks in the task manager.
    Includes a 'tags' attribute for categorization.
    """
    def __init__(self, id, description, completed=False, tags=None):
        self.id = id
        self.description = description
        self.completed = completed
        # Ensure tags is always a list, even if None is passed
        self.tags = list(tags) if tags is not None else []

    def mark_complete(self):
        """Marks the task as completed."""
        self.completed = True

    def add_tag(self, tag):
        """Adds a tag to the task, preventing duplicates."""
        tag = tag.strip().lower()  # Normalize tag input
        if tag and tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        """Removes a tag from the task."""
        tag = tag.strip().lower()
        if tag in self.tags:
            self.tags.remove(tag)

    def to_dict(self):
        """
        Converts the Task object to a dictionary for JSON serialization.
        Includes a '_type' field and tags.
        """
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "tags": self.tags,
            "_type": "Task"
        }

    def __str__(self):
        """
        Returns a human-readable string representation of the task.
        """
        status = "Completed" if self.completed else "Pending"
        tags_str = f" | Tags: {', '.join(self.tags)}" if self.tags else ""
        return f"ID: {self.id} | Description: {self.description} | Status: {status}{tags_str}"

    def __repr__(self):
        return f"Task(id={self.id}, description='{self.description}', completed={self.completed}, tags={self.tags})"


class DueDateTask(Task):
    """
    A task with an additional due date, stored as a datetime.date object.
    Inherits from the base Task class.
    """
    def __init__(self, id, description, due_date, completed=False, tags=None):
        super().__init__(id, description, completed, tags)
        # due_date can be a string (from JSON/CLI) or a datetime.date object
        if isinstance(due_date, str):
            self.due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()
        elif isinstance(due_date, datetime.date):
            self.due_date = due_date
        else:
            raise TypeError("due_date must be a string in YYYY-MM-DD format or a datetime.date object")

    def to_dict(self):
        """
        Overrides to_dict to include due_date (formatted as string) and its own type identifier.
        """
        base_dict = super().to_dict()
        base_dict["due_date"] = self.due_date.strftime('%Y-%m-%d')
        base_dict["_type"] = "DueDateTask"
        return base_dict

    def __str__(self):
        """
        Overrides __str__ to include the due date.
        """
        base_str = super().__str__()
        # Insert due date before tags part if tags exist, otherwise append
        if ' | Tags:' in base_str:
            base_str_without_tags, tags_part = base_str.split(' | Tags:', 1)
            return f"{base_str_without_tags} | Due: {self.due_date.strftime('%Y-%m-%d')} | Tags: {tags_part.strip()}"
        return f"{base_str} | Due: {self.due_date.strftime('%Y-%m-%d')}"

    def __repr__(self):
        return (f"DueDateTask(id={self.id}, description='{self.description}', "
                f"due_date='{self.due_date.strftime('%Y-%m-%d')}', completed={self.completed}, tags={self.tags})")


class PriorityTask(Task):
    """
    A task with an additional priority level.
    Inherits from the base Task class.
    """
    def __init__(self, id, description, priority, completed=False, tags=None):
        super().__init__(id, description, completed, tags)
        # Ensure priority is one of the allowed values
        allowed_priorities = ["High", "Medium", "Low"]
        if priority not in allowed_priorities:
            raise ValueError(f"Priority must be one of {allowed_priorities}")
        self.priority = priority

    def to_dict(self):
        """
        Overrides to_dict to include priority and its own type identifier.
        """
        base_dict = super().to_dict()
        base_dict["priority"] = self.priority
        base_dict["_type"] = "PriorityTask"
        return base_dict

    def __str__(self):
        """
        Overrides __str__ to include the priority.
        """
        base_str = super().__str__()
        # Insert priority before tags part if tags exist, otherwise append
        if ' | Tags:' in base_str:
            base_str_without_tags, tags_part = base_str.split(' | Tags:', 1)
            return f"{base_str_without_tags} | Priority: {self.priority} | Tags: {tags_part.strip()}"
        return f"{base_str} | Priority: {self.priority}"

    def __repr__(self):
        return (f"PriorityTask(id={self.id}, description='{self.description}', "
                f"priority='{self.priority}', completed={self.completed}, tags={self.tags})")
