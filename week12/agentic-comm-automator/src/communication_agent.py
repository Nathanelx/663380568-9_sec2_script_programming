# agentic-comm-automator/src/communication_agent.py
import datetime
import json
import os
import time

from .utils import setup_logging, log_audit_entry, ensure_directory_exists, get_env_variable
from .email_tasks import EmailTasks
from .sms_tasks import SMSTasks
from .template_renderer import TemplateRenderer

logger = setup_logging(__name__)


class CommunicationAgent:
    """
    An agent that orchestrates communication tasks (email, SMS, inbox processing) based on a
    configuration file, managing an internal context for dynamic values.
    """
    def __init__(self, config, base_dir):
        self.config = config
        self.base_dir = base_dir
        self.audit_log = []
        self.context = {}  # Stores dynamic values for templating and task chaining
        self.start_time = datetime.datetime.now()

        try:
            sender_email = get_env_variable("SENDER_EMAIL")
            sender_app_password = get_env_variable("SENDER_APP_PASSWORD")
            smtp_server = get_env_variable("SMTP_SERVER")
            smtp_port = int(get_env_variable("SMTP_PORT"))
            imap_server = get_env_variable("IMAP_SERVER")
        except ValueError as e:
            logger.critical(f"Agent initialization failed: Missing environment variables. {e}")
            raise

        self.email_tasks = EmailTasks(smtp_server, smtp_port, imap_server, sender_email, sender_app_password)
        self.sms_tasks = SMSTasks(self.email_tasks)  # SMS uses EmailTasks for the underlying send
        self.template_renderer = TemplateRenderer()

        self.handlers = {
            "send_email": self._handle_send_email,
            "send_sms": self._handle_send_sms,
            "process_inbox": self._handle_process_inbox,
        }
        logger.info("CommunicationAgent initialized with task handlers.")

    # ---------- Context & templates ----------
    def _update_context(self, key, value):
        """Updates a value in the agent's context."""
        self.context[key] = value
        logger.debug(f"Context updated: '{key}' = {value}")

    def _render(self, template_string, extra=None):
        """Renders a template using the agent context (+ extra values such as the current email)."""
        return self.template_renderer.render(template_string, {**self.context, **(extra or {})})

    def _abs_path(self, path):
        return os.path.normpath(os.path.join(self.base_dir, path))

    # ---------- Task handlers: return (success, output_data) ----------
    def _handle_send_email(self, params):
        recipients = {k: [self._render(r) for r in v] for k, v in params.get('recipients', {}).items()}
        subject = self._render(params["subject_template"])
        body = self._render(params["body_template"])
        attachments = [self._abs_path(self._render(p)) for p in params.get("attachments", [])]

        success = self.email_tasks.send_email(recipients, subject, body, attachments, params.get("is_html", False))
        return success, {"recipients": recipients, "subject": subject, "attachments": attachments}

    def _handle_send_sms(self, params):
        phone_numbers = [self._render(p) for p in params["phone_numbers"]]
        message = self._render(params["message_template"])
        success = self.sms_tasks.send_sms(phone_numbers, message, params.get("carrier_name"))
        return success, {"phone_numbers": phone_numbers, "message": message}

    def _rule_matches(self, conditions, email_info):
        """ตรวจเงื่อนไข if ของ rule กับอีเมลหนึ่งฉบับ (ทุกเงื่อนไขต้องเป็นจริง)"""
        if "subject_contains" in conditions and self._render(conditions["subject_contains"]) not in email_info['subject']:
            return False
        if "body_contains" in conditions and self._render(conditions["body_contains"]) not in email_info['text_body']:
            return False
        if "from_sender_contains" in conditions and self._render(conditions["from_sender_contains"]) not in email_info['sender']:
            return False
        if "has_attachments" in conditions and conditions["has_attachments"] != email_info['has_attachments']:
            return False
        return True

    def _apply_rule_actions(self, actions, email_info):
        """ทำ action ใน then ของ rule และคืนรายการ action ที่ทำ"""
        done = []
        if actions.get("send_sms_alert"):
            message = self._render(actions.get("alert_message_template", "Urgent email received: {subject} from {sender}"), email_info)
            phone_numbers = [self._render(p) for p in actions.get("alert_phone_numbers", [])]
            ok = self.sms_tasks.send_sms(phone_numbers, message, actions.get("alert_carrier"))
            done.append({"action": "send_sms_alert", "success": ok, "message": message})
        if "reply_with_template" in actions:
            reply_subject = self._render(actions.get("reply_subject_template", "Re: {subject}"), email_info)
            reply_body = self._render(actions["reply_with_template"], email_info)
            ok = self.email_tasks.send_email(recipients={'to': [email_info['sender']]}, subject=reply_subject, body=reply_body)
            done.append({"action": "reply", "success": ok, "subject": reply_subject})
        return done

    def _handle_process_inbox(self, params):
        criteria = params["search_criteria"]
        download_dir = self._abs_path(params.get("download_attachments_base_dir", "data/incoming_attachments"))

        wait_seconds = params.get("wait_seconds", 0)
        if wait_seconds:
            logger.info(f"Waiting {wait_seconds} seconds for emails to arrive...")
            time.sleep(wait_seconds)

        uids = self.email_tasks.search_emails(
            mailbox=params.get("mailbox", "INBOX"),
            criteria=criteria.get("status", "UNSEEN"),
            from_sender=self._render(criteria["from_sender"]) if criteria.get("from_sender") else None,
            subject_contains=self._render(criteria["subject_contains"]) if criteria.get("subject_contains") else None,
        )
        if not uids:
            logger.info("No emails found matching search criteria for inbox processing.")
            return True, {"processed_emails": []}  # No emails found is not a failure

        processed = []
        for uid in uids:
            email_info = self.email_tasks.fetch_email_content(uid, mark_as_read=True, download_attachments_dir=download_dir)
            if not email_info:
                logger.error(f"Failed to fetch content for email UID {uid.decode('utf-8')}.")
                continue

            actions_done = []
            for i, rule in enumerate(params.get("rules", [])):
                if self._rule_matches(rule.get("if", {}), email_info):
                    logger.info(f"Rule {i + 1} matched for email UID {email_info['uid']}. Applying actions...")
                    actions_done.extend(self._apply_rule_actions(rule.get("then", {}), email_info))
                else:
                    logger.info(f"Rule {i + 1} did not match email UID {email_info['uid']}.")

            processed.append({
                "uid": email_info["uid"], "sender": email_info["sender"], "subject": email_info["subject"],
                "attachments": [a["filepath"] or a["filename"] for a in email_info["attachments_meta"]],
                "actions": actions_done,
            })
            log_audit_entry(self.audit_log, "INFO", f"Processed email UID {email_info['uid']}: '{email_info['subject']}'",
                            "process_inbox", processed[-1])
        return True, {"processed_emails": processed}

    # ---------- Agent loop ----------
    def _process_task(self, task):
        """Dispatches a task to the appropriate handler and manages context."""
        task_type = task.get("type")
        task_name = task.get("name", task_type)
        output_context_key = task.get("output_context_key")

        logger.info(f"Executing task: '{task_name}' (Type: {task_type})")
        log_audit_entry(self.audit_log, "INFO", f"Starting task '{task_name}'", task_type, task)

        handler = self.handlers.get(task_type)
        if handler is None:
            log_audit_entry(self.audit_log, "WARNING", f"Unsupported task type: {task_type}", task_type, task)
            return

        try:
            success, output_data = handler(task.get("parameters", {}))
            if success and output_data is not None and output_context_key:
                self._update_context(output_context_key, output_data)
            status = "SUCCESS" if success else "ERROR"
            log_audit_entry(self.audit_log, status,
                            f"Task '{task_name}' {'completed successfully' if success else 'failed'}.", task_type, output_data)
        except Exception as e:
            log_audit_entry(self.audit_log, "ERROR", f"An error occurred during task '{task_name}': {e}", task_type,
                            {"error": str(e)})
            logger.error(f"Error during task '{task_name}': {e}", exc_info=True)

    def _generate_audit_report(self, output_dir):
        """Generates a JSON audit report."""
        ensure_directory_exists(output_dir)
        report_path = os.path.join(output_dir, f"audit_report_comm_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.audit_log, f, indent=4, ensure_ascii=False, default=str)
            logger.info(f"Audit report saved to: {report_path}")
        except Exception as e:
            logger.error(f"Failed to save audit report: {e}")
        return report_path

    def run(self):
        """Executes all tasks defined in the configuration."""
        logger.info("Starting Communication Agent run...")
        log_audit_entry(self.audit_log, "INFO", "Communication Agent started.", "agent_run")

        # Simulated data that might come from a previous agent (e.g. the Week 8 data agent)
        self._update_context("report_name", "DailySalesSummary")
        self._update_context("report_date", datetime.date.today().strftime("%Y-%m-%d"))
        self._update_context("sales_figure", 12345.67)
        self._update_context("total_customers", 500)
        self._update_context("attachment_path_1", "data/reports/sales_report.pdf")
        self._update_context("attachment_path_2", "data/reports/summary_data.xlsx")
        self._update_context("student_info", get_env_variable("STUDENT_INFO", "ชื่อ-นามสกุล และรหัสนักศึกษา"))

        for task in self.config.get("tasks", []):
            self._process_task(task)

        duration = (datetime.datetime.now() - self.start_time).total_seconds()
        errors = sum(1 for entry in self.audit_log if entry["status"] == "ERROR")
        log_audit_entry(self.audit_log, "INFO", f"Communication Agent finished in {duration:.2f} seconds with {errors} error(s).",
                        "agent_run_summary")
        logger.info(f"Communication Agent finished. Total time: {duration:.2f} seconds. Errors: {errors}")

        return self._generate_audit_report(os.path.join(self.base_dir, 'reports'))
