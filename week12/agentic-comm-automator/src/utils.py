# agentic-comm-automator/src/utils.py
import datetime
import logging
import os
import re

from dotenv import load_dotenv

# Load environment variables from .env file (โฟลเดอร์โปรเจกต์)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ${VAR_NAME} (ตัวพิมพ์ใหญ่) ใน config = ค่าจาก .env  ส่วน ${sales_figure:.2f} เป็นเครื่องหมาย $ ตามด้วย {template}
ENV_PATTERN = re.compile(r"\$\{([A-Z][A-Z0-9_]*)\}")


def setup_logging(name, level=logging.INFO):
    """Sets up a logger for specific modules."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:  # Prevent adding multiple handlers if called multiple times
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False  # ไม่ส่งต่อไป root logger เพื่อไม่ให้ข้อความแสดงซ้ำ
    return logger


def get_env_variable(var_name, default=None):
    """Retrieves an environment variable, raising an error if not found (and no default)."""
    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not set. Please check your .env file or environment settings.")
    return value


def expand_env_vars(value):
    """แทนที่ ${VAR} ทุกจุดใน config (string / list / dict) ด้วยค่าจาก environment variables"""
    if isinstance(value, str):
        return ENV_PATTERN.sub(lambda m: get_env_variable(m.group(1)), value)
    if isinstance(value, list):
        return [expand_env_vars(v) for v in value]
    if isinstance(value, dict):
        return {k: expand_env_vars(v) for k, v in value.items()}
    return value


def ensure_directory_exists(path):
    """Ensures that a directory exists, creating it if necessary."""
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory ensured: {path}")
    except OSError as e:
        logging.error(f"Error creating directory {path}: {e}")
        raise


def log_audit_entry(audit_log_list, status, message, task_type="N/A", details=None):
    """Adds an entry to the audit log list."""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "status": status,
        "task_type": task_type,
        "message": message,
        "details": details if details else {}
    }
    audit_log_list.append(log_entry)
    if status in ("ERROR", "CRITICAL"):
        logging.error(f"AUDIT LOG - {status}: {message} | Task: {task_type} | Details: {details}")
    else:
        logging.info(f"AUDIT LOG - {status}: {message} | Task: {task_type}")
