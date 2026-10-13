# agentic-document-automator/main.py
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config_parser import ConfigParser
from document_agent import DocumentAgent
from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

PATH_KEYS = ['template_path', 'output_path', 'input_pdf', 'output_pdf', 'input_docx', 'output_text_file']


def check_required_files(config):
    """ตรวจว่าไฟล์ input (template, PDF ต้นฉบับ, PDF ที่จะรวม) มีครบก่อนเริ่มทำงาน"""
    all_exist = True
    for task in config['tasks']:
        required = []
        if task['type'] == 'generate_word_report':
            required.append(task['template_path'])
        elif task['type'] == 'apply_pdf_watermark':
            required.append(task['input_pdf'])
        elif task['type'] == 'merge_pdfs':
            required.extend(task['input_pdfs'])
        for path in required:
            if not os.path.exists(path):
                logger.critical(f"Required input file not found for task '{task.get('name')}': {path}")
                all_exist = False
    return all_exist


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(base_dir, 'configs', 'document_automation_config.json')

    ensure_directory_exists(os.path.join(base_dir, 'documents'))
    ensure_directory_exists(os.path.join(base_dir, 'templates'))

    try:
        config = ConfigParser(config_file_path).load_config()
    except (FileNotFoundError, ValueError) as e:
        logger.critical(f"Configuration error: {e}")
        return

    # แปลง path ใน config (relative กับโฟลเดอร์โปรเจกต์) ให้เป็น absolute path
    for key, value in config['output_files'].items():
        config['output_files'][key] = os.path.normpath(os.path.join(base_dir, value))
    for task in config['tasks']:
        for k in PATH_KEYS:
            if k in task:
                task[k] = os.path.normpath(os.path.join(base_dir, task[k]))
        if 'input_pdfs' in task:
            task['input_pdfs'] = [os.path.normpath(os.path.join(base_dir, p)) for p in task['input_pdfs']]

    if not check_required_files(config):
        logger.critical("Missing required input files! Please check the 'templates' and 'documents' folders.")
        return

    agent = DocumentAgent(config)
    report_path = agent.run()
    logger.info(f"Document automation process completed. Audit report: {report_path}")


if __name__ == "__main__":
    main()
