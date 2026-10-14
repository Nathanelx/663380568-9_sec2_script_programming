import os
import sys
import unittest
import tempfile
import datetime

# Add 'src' to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from task import Task, DueDateTask, PriorityTask
from task_manager import TaskManager
from data_persistence import DataPersistence


class TestTaskModels(unittest.TestCase):
    """Test suite for domain model classes: Task, DueDateTask, PriorityTask."""

    def test_task_creation_and_tags(self):
        task = Task(1, "Test Base Task", tags=["study", "urgent"])
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Test Base Task")
        self.assertFalse(task.completed)
        self.assertEqual(task.tags, ["study", "urgent"])

        # Test add_tag with case normalization & duplicate prevention
        task.add_tag(" STUDY ")
        self.assertEqual(len(task.tags), 2)  # Should not duplicate 'study'
        task.add_tag("NewTag")
        self.assertIn("newtag", task.tags)

        # Test remove_tag
        task.remove_tag("study")
        self.assertNotIn("study", task.tags)

        # Test mark_complete
        task.mark_complete()
        self.assertTrue(task.completed)

        # Test to_dict
        d = task.to_dict()
        self.assertEqual(d["_type"], "Task")
        self.assertEqual(d["id"], 1)
        self.assertTrue(d["completed"])
        self.assertIn("newtag", d["tags"])

    def test_duedate_task(self):
        due_task = DueDateTask(2, "Submit Project", "2026-10-31", tags=["school"])
        self.assertEqual(due_task.due_date, datetime.date(2026, 10, 31))
        self.assertIn("Due: 2026-10-31", str(due_task))

        d = due_task.to_dict()
        self.assertEqual(d["_type"], "DueDateTask")
        self.assertEqual(d["due_date"], "2026-10-31")

        # Invalid date format
        with self.assertRaises((ValueError, TypeError)):
            DueDateTask(3, "Invalid Date", "31-10-2026")

    def test_priority_task(self):
        pri_task = PriorityTask(3, "Fix Critical Bug", "High", tags=["bug"])
        self.assertEqual(pri_task.priority, "High")
        self.assertIn("Priority: High", str(pri_task))

        d = pri_task.to_dict()
        self.assertEqual(d["_type"], "PriorityTask")
        self.assertEqual(d["priority"], "High")

        # Invalid priority value
        with self.assertRaises(ValueError):
            PriorityTask(4, "Invalid Priority", "SuperUrgent")


class TestTaskManagerLogic(unittest.TestCase):
    """Test suite for business logic in TaskManager."""

    def setUp(self):
        # Create a temporary file for isolated persistence testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, "test_tasks.json")
        self.manager = TaskManager(self.temp_file)

        # Populate with initial test tasks
        self.t1 = self.manager.add_normal_task("Study for exam", tags=["study", "exam"])
        self.t2 = self.manager.add_due_date_task("Submit report", "2026-09-20", tags=["assignment", "study"])
        self.t3 = self.manager.add_priority_task("Emergency meeting", "High", tags=["urgent"])
        self.t4 = self.manager.add_priority_task("Casual reading", "Low", tags=["personal"])
        self.t5 = self.manager.add_due_date_task("Pay electricity bill", "2026-09-10", tags=["finance"])

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_crud_operations(self):
        self.assertEqual(len(self.manager.get_all_tasks()), 5)

        # Complete task
        success, msg = self.manager.complete_task(self.t1.id)
        self.assertTrue(success)
        self.assertTrue(self.manager.get_task_by_id(self.t1.id).completed)

        # Complete already completed task
        success, msg = self.manager.complete_task(self.t1.id)
        self.assertFalse(success)

        # Delete task
        success, msg = self.manager.delete_task(self.t4.id)
        self.assertTrue(success)
        self.assertIsNone(self.manager.get_task_by_id(self.t4.id))
        self.assertEqual(len(self.manager.get_all_tasks()), 4)

    def test_search_tasks(self):
        # Search in description
        results = self.manager.search_tasks("report")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, self.t2.id)

        # Search in tags (case-insensitive)
        results = self.manager.search_tasks("STUDY")
        self.assertEqual(len(results), 2)  # t1 and t2 have 'study' tag

        # Search empty keyword
        self.assertEqual(self.manager.search_tasks(""), [])

    def test_filter_tasks(self):
        # Filter by completed status
        self.manager.complete_task(self.t1.id)
        completed_tasks = self.manager.filter_tasks(status=True)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].id, self.t1.id)

        # Filter by priority
        high_pri = self.manager.filter_tasks(priority_level="High")
        self.assertEqual(len(high_pri), 1)
        self.assertEqual(high_pri[0].id, self.t3.id)

        # Filter by due date
        target_date = datetime.date(2026, 9, 15)
        due_before = self.manager.filter_tasks(due_date_before=target_date)
        self.assertEqual(len(due_before), 1)
        self.assertEqual(due_before[0].id, self.t5.id)

        # Filter by tags (task must have ALL specified tags)
        tag_filter = self.manager.filter_tasks(contains_tags=["study", "exam"])
        self.assertEqual(len(tag_filter), 1)
        self.assertEqual(tag_filter[0].id, self.t1.id)

    def test_sort_tasks(self):
        # Sort by ID descending
        sorted_id_desc = self.manager.sort_tasks(criterion="id", reverse=True)
        self.assertEqual(sorted_id_desc[0].id, 5)

        # Sort by Priority: High (1) -> Low (3) -> Non-priority (99)
        sorted_pri = self.manager.sort_tasks(criterion="priority")
        self.assertEqual(sorted_pri[0].id, self.t3.id)  # High
        self.assertEqual(sorted_pri[1].id, self.t4.id)  # Low

        # Sort by Due Date: 2026-09-10 (t5) -> 2026-09-20 (t2) -> others at end
        sorted_date = self.manager.sort_tasks(criterion="due_date")
        self.assertEqual(sorted_date[0].id, self.t5.id)
        self.assertEqual(sorted_date[1].id, self.t2.id)

    def test_persistence_reload(self):
        # Test that data is persisted and can be reloaded accurately
        new_manager = TaskManager(self.temp_file)
        tasks = new_manager.get_all_tasks()
        self.assertEqual(len(tasks), 5)

        due_task = next(t for t in tasks if t.id == self.t2.id)
        self.assertIsInstance(due_task, DueDateTask)
        self.assertEqual(due_task.due_date, datetime.date(2026, 9, 20))
        self.assertEqual(due_task.tags, ["assignment", "study"])


if __name__ == "__main__":
    unittest.main()
