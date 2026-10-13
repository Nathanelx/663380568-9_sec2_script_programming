# agentic-data-processor/src/data_agent.py
import datetime
import json
import os
from .utils import setup_logging, log_audit_entry, ensure_directory_exists
from .csv_tasks import CSVTasks
from .json_tasks import JSONTasks
from .conversion_tasks import ConversionTasks

logger = setup_logging(__name__)


class DataAgent:
    """
    An agent that processes various data formats (CSV, JSON) based on a
    structured configuration file, managing internal data state.

    แต่ละ task อ่านข้อมูลจาก data_store ด้วย input_data_key
    แล้วเก็บผลลัพธ์กลับด้วย output_data_key ทำให้ต่อ task เป็น pipeline ได้
    """
    def __init__(self, config, report_dir="reports"):
        self.config = config
        self.report_dir = report_dir
        self.audit_log = []
        self.data_store = {}  # Stores intermediate data results {key: data_object}
        self.start_time = datetime.datetime.now()

        self.csv_tasks = CSVTasks()
        self.json_tasks = JSONTasks()
        self.conversion_tasks = ConversionTasks()

        # task type -> method ที่ใช้ทำงานนั้น
        self.handlers = {
            "load_csv": self._load_csv,
            "save_csv": self._save_csv,
            "transform_csv_aggregate": self._transform_csv_aggregate,
            "filter_csv": self._filter_csv,
            "load_json": self._load_json,
            "save_json": self._save_json,
            "update_json_data": self._update_json_data,
            "query_json_data": self._query_json_data,
            "csv_to_json_conversion": self._csv_to_json,
            "json_to_csv_conversion": self._json_to_csv,
        }

        logger.info("Data Agent initialized with configuration.")

    # ---------- Task handlers: return (success, output_data) ----------
    def _load_csv(self, task, data):
        result = self.csv_tasks.load_csv(task["file_path"])
        return result is not None, result

    def _save_csv(self, task, data):
        return self.csv_tasks.save_csv(data, task["file_path"], task.get("fieldnames")), None

    def _transform_csv_aggregate(self, task, data):
        result = self.csv_tasks.transform_csv_aggregate(
            data, task["group_by_field"], task["aggregate_field"], task.get("aggregate_type", "sum"))
        return result is not None, result

    def _filter_csv(self, task, data):
        result = self.csv_tasks.filter_csv(data, task["filter_field"], task["operator"], task["value"])
        return result is not None, result

    def _load_json(self, task, data):
        result = self.json_tasks.load_json(task["file_path"])
        return result is not None, result

    def _save_json(self, task, data):
        return self.json_tasks.save_json(data, task["file_path"], task.get("indent", 2)), None

    def _update_json_data(self, task, data):
        result = self.json_tasks.update_json_data(data, task["updates"])
        return result is not None, result

    def _query_json_data(self, task, data):
        result = self.json_tasks.query_json_data(data, task["path"])
        log_audit_entry(self.audit_log, "INFO", f"Query result for path '{task['path']}': {result}",
                        task["type"], {"query_path": task["path"], "result": result})
        return True, result

    def _csv_to_json(self, task, data):
        return True, self.conversion_tasks.csv_to_json(data)

    def _json_to_csv(self, task, data):
        rows, _ = self.conversion_tasks.json_to_csv(data, task.get("fieldnames"))
        return True, rows

    # ---------- Agent loop ----------
    def _process_task(self, task):
        """Dispatches a task to the appropriate handler and manages data state."""
        task_type = task.get("type")
        task_name = task.get("name", task_type)
        input_data_key = task.get("input_data_key")
        output_data_key = task.get("output_data_key")

        logger.info(f"Executing task: '{task_name}' (Type: {task_type})")
        log_audit_entry(self.audit_log, "INFO", f"Starting task '{task_name}'", task_type, task)

        handler = self.handlers.get(task_type)
        if handler is None:
            log_audit_entry(self.audit_log, "WARNING", f"Unsupported task type: {task_type}", task_type, task)
            logger.warning(f"Unsupported task type: {task_type}")
            return

        current_data = None
        if input_data_key:
            if input_data_key not in self.data_store:
                log_audit_entry(self.audit_log, "ERROR",
                                f"Task '{task_name}' failed: Required input data '{input_data_key}' not found in store.",
                                task_type, task)
                return
            current_data = self.data_store[input_data_key]

        try:
            success, output_data = handler(task, current_data)

            if success and output_data is not None and output_data_key:
                self.data_store[output_data_key] = output_data

            status = "SUCCESS" if success else "ERROR"
            log_audit_entry(self.audit_log, status,
                            f"Task '{task_name}' {'completed successfully' if success else 'failed'}.",
                            task_type, task)
        except Exception as e:
            log_audit_entry(self.audit_log, "ERROR", f"An error occurred during task '{task_name}': {e}",
                            task_type, {"error": str(e), "task_details": task})
            logger.error(f"Error during task '{task_name}': {e}", exc_info=True)

    def _generate_audit_report(self):
        """Generates a JSON audit report."""
        ensure_directory_exists(self.report_dir)
        report_filename = f"audit_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(self.report_dir, report_filename)

        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.audit_log, f, indent=4, ensure_ascii=False)
            logger.info(f"Audit report saved to: {report_path}")
        except Exception as e:
            logger.error(f"Failed to save audit report: {e}")
        return report_path

    def run(self):
        """Executes all tasks defined in the configuration."""
        logger.info("Starting Data Agent run...")
        log_audit_entry(self.audit_log, "INFO", "Data Agent started.", "agent_run")

        for task in self.config.get("tasks", []):
            self._process_task(task)

        duration = (datetime.datetime.now() - self.start_time).total_seconds()
        errors = sum(1 for entry in self.audit_log if entry["status"] == "ERROR")
        log_audit_entry(self.audit_log, "INFO",
                        f"Data Agent finished in {duration:.2f} seconds with {errors} error(s).",
                        "agent_run_summary")
        logger.info(f"Data Agent finished. Total time: {duration:.2f} seconds. Errors: {errors}")

        return self._generate_audit_report()
