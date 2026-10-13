# agentic-document-automator/src/document_agent.py
import os
import json
import datetime

from utils import setup_logging, log_audit_entry, ensure_directory_exists
from pdf_tasks import PDFTasks
from word_tasks import WordTasks

logger = setup_logging(__name__)


class DocumentAgent:
    """Runs document tasks (Word report, PDF watermark/merge, text extraction) defined in the config."""

    def __init__(self, config):
        self.config = config
        self.audit_log = []
        self.start_time = datetime.datetime.now()
        self.pdf_processor = PDFTasks()
        self.word_processor = WordTasks()

    def _save_text(self, text, output_text_file):
        ensure_directory_exists(os.path.dirname(output_text_file))
        with open(output_text_file, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f"Text saved to '{output_text_file}'.")

    def _process_task(self, task):
        task_type = task.get("type")
        task_name = task.get("name", task_type)
        logger.info(f"Executing task: '{task_name}' (Type: {task_type})")
        log_audit_entry(self.audit_log, "INFO", f"Starting task '{task_name}'", task_type, task)
        try:
            success = False
            if task_type == "generate_word_report":
                # global_data + data ของ task (ค่าใน task ทับ global ได้)
                placeholders = {**self.config.get("global_data", {}), **task.get("data", {})}
                success = self.word_processor.generate_report_from_template(
                    task["template_path"], task["output_path"], placeholders, task.get("table_data"))
            elif task_type == "apply_pdf_watermark":
                success = self.pdf_processor.apply_watermark(
                    task["input_pdf"], task["output_pdf"], task["watermark_text"],
                    task.get("font_size", 50), tuple(task.get("color", [0.5, 0.5, 0.5, 0.2])), task.get("angle", 45))
            elif task_type == "merge_pdfs":
                success = self.pdf_processor.merge_pdfs(task["input_pdfs"], task["output_pdf"])
            elif task_type == "extract_pdf_text":
                text = self.pdf_processor.extract_text_from_pdf(task["input_pdf"])
                if text:
                    self._save_text(text, task["output_text_file"])
                    success = True
            elif task_type == "extract_word_text":
                text = self.word_processor.extract_text_from_word(task["input_docx"])
                if text:
                    self._save_text(text, task["output_text_file"])
                    success = True
            else:
                log_audit_entry(self.audit_log, "WARNING", f"Unsupported task type: {task_type}", task_type)
                return

            if success:
                log_audit_entry(self.audit_log, "SUCCESS", f"Task '{task_name}' completed.", task_type)
            else:
                log_audit_entry(self.audit_log, "ERROR", f"Task '{task_name}' failed.", task_type)
        except Exception as e:
            log_audit_entry(self.audit_log, "ERROR", f"Error in '{task_name}': {e}", task_type)

    def _generate_audit_report(self, output_dir):
        ensure_directory_exists(output_dir)
        report_path = os.path.join(output_dir, f"audit_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.audit_log, f, indent=4, ensure_ascii=False)
        logger.info(f"Audit report saved to: {report_path}")
        return report_path

    def run(self):
        log_audit_entry(self.audit_log, "INFO", "Document Agent started.", "agent_run")
        for task in self.config.get("tasks", []):
            self._process_task(task)
        duration = (datetime.datetime.now() - self.start_time).total_seconds()
        errors = sum(1 for entry in self.audit_log if entry["status"] == "ERROR")
        log_audit_entry(self.audit_log, "INFO", f"Finished in {duration:.2f}s with {errors} error(s).", "agent_run_summary")
        # บันทึก audit report ไว้ที่ documents/reports/
        reports_dir = os.path.join(os.path.dirname(self.config['output_files']['generated_report']), 'reports')
        return self._generate_audit_report(reports_dir)
