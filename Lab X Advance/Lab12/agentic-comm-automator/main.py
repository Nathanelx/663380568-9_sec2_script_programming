# agentic-comm-automator/main.py
import os
import sys

# เรียกใช้โมดูลผ่านแพ็กเกจ src (ต้องรันจากโฟลเดอร์ agentic-comm-automator)
from src.config_parser import ConfigParser
from src.communication_agent import CommunicationAgent
from src.utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

# ค่าเดียวกับใน CommunicationAgent.run() ใช้ตรวจ path ไฟล์แนบที่เขียนเป็น template
KNOWN_ATTACHMENTS = {
    "{attachment_path_1}": "data/reports/sales_report.pdf",
    "{attachment_path_2}": "data/reports/summary_data.xlsx",
}


def check_required_files(config, base_dir):
    """Checks that every attachment listed in send_email tasks exists."""
    missing_files = []
    for task in config['tasks']:
        if task['type'] != 'send_email':
            continue
        for att_path in task.get('parameters', {}).get('attachments', []):
            file_path = os.path.join(base_dir, KNOWN_ATTACHMENTS.get(att_path, att_path))
            if '{' not in file_path and not os.path.exists(file_path):
                missing_files.append(file_path)
    return missing_files


def main():
    """
    Main entry point for the Agentic Communication Automator.
    Loads config and runs the agent.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(base_dir, 'configs', 'comm_pipeline_config.json')

    try:
        ensure_directory_exists(os.path.join(base_dir, 'data', 'reports'))
        ensure_directory_exists(os.path.join(base_dir, 'data', 'incoming_attachments'))
        ensure_directory_exists(os.path.join(base_dir, 'reports'))  # For audit reports

        logger.info(f"Loading configuration from: {config_file_path}")
        config = ConfigParser(config_file_path).load_config()

        missing = check_required_files(config, base_dir)
        if missing:
            logger.critical(f"Required attachment files are missing: {', '.join(missing)}")
            sys.exit(1)

        logger.info("Initializing Communication Agent...")
        agent = CommunicationAgent(config, base_dir)

        logger.info("Running Communication Agent workflow...")
        report_path = agent.run()
        logger.info(f"Communication automation process completed. Audit report: {report_path}")

    except FileNotFoundError as e:
        logger.critical(f"File system error: {e}")
    except ValueError as e:
        logger.critical(f"Configuration or environment variable error: {e}")
        logger.info("Please check your config file and .env (copy .env.example to .env and fill it in).")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred during execution: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
