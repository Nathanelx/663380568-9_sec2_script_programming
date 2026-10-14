# agentic-data-processor/main.py
import os

# เรียกใช้โมดูลผ่านแพ็กเกจ src โดยตรง (ต้องรันจากโฟลเดอร์ agentic-data-processor)
from src.config_parser import ConfigParser
from src.data_agent import DataAgent
from src.utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


def check_required_input_files(config):
    """
    Checks if all input files specified in the config exist before starting the agent.
    """
    required_files_exist = True
    for task in config['tasks']:
        if task['type'] in ['load_csv', 'load_json']:
            file_path = task['file_path']
            if not os.path.exists(file_path):
                logger.critical(f"Required input file '{file_path}' not found for task '{task.get('name')}'.")
                required_files_exist = False
    return required_files_exist


def main():
    """
    Main entry point for the Agentic Data Processor.
    Loads config and runs the agent.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(base_dir, 'configs', 'data_pipeline_config.json')
    reports_dir = os.path.join(base_dir, 'reports')

    try:
        ensure_directory_exists(os.path.join(base_dir, 'data'))
        ensure_directory_exists(reports_dir)

        logger.info(f"Loading configuration from: {config_file_path}")
        config = ConfigParser(config_file_path).load_config()

        # path ใน config เขียนแบบ relative กับโฟลเดอร์โปรเจกต์ แปลงเป็น absolute ก่อนใช้
        for task in config['tasks']:
            if 'file_path' in task:
                task['file_path'] = os.path.normpath(os.path.join(base_dir, task['file_path']))

        if not check_required_input_files(config):
            logger.critical("One or more required input files are missing. Please create them as per README.md and config.")
            return

        logger.info("Initializing Data Agent...")
        agent = DataAgent(config, report_dir=reports_dir)

        logger.info("Running Data Agent workflow...")
        report_path = agent.run()

        logger.info(f"Data automation process completed. Audit report: {report_path}")

    except FileNotFoundError as e:
        logger.critical(f"File system error: {e}")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}")
        logger.info("Please check the format and required fields in your config file.")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred during execution: {e}", exc_info=True)


if __name__ == "__main__":
    main()
