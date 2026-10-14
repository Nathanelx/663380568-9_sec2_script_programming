# agentic-data-processor/src/json_tasks.py
import copy
import json
import os
from .utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


def _step(node, key):
    """
    เดินเข้าไป 1 ระดับใน JSON: dict ใช้ key, list ใช้ index (ตัวเลข)
    คืนค่า (found, child)
    """
    if isinstance(node, dict):
        return (key in node), node.get(key)
    if isinstance(node, list) and key.isdigit():
        index = int(key)
        if 0 <= index < len(node):
            return True, node[index]
    return False, None


class JSONTasks:
    """
    Handles advanced reading, writing, and manipulation of JSON data.
    Paths use dot-notation, e.g. "0.details.brand" (list index 0 -> key details -> key brand).
    An empty path "" means the root object.
    """
    def __init__(self):
        logger.info("JSONTasks initialized.")

    def load_json(self, file_path):
        """Loads a JSON file and returns the Python object."""
        if not os.path.exists(file_path):
            logger.error(f"JSON file not found: {file_path}")
            return None

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info(f"Successfully loaded JSON from '{file_path}'.")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in '{file_path}': {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading JSON file '{file_path}': {e}")
            return None

    def save_json(self, data, file_path, indent=2):
        """Saves a Python object to a JSON file, with pretty-printing."""
        ensure_directory_exists(os.path.dirname(file_path))

        try:
            with open(file_path, mode='w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
            logger.info(f"Successfully saved JSON to '{file_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error saving JSON file '{file_path}': {e}")
            return False

    def _resolve(self, data, keys):
        """Follows a list of keys from data. Returns (found, node)."""
        node = data
        for key in keys:
            found, node = _step(node, key)
            if not found:
                return False, None
        return True, node

    def update_json_data(self, data, updates):
        """
        Applies updates to a JSON-like Python object (returns a modified deep copy).
        `updates` is a list of dicts: {"path": "0.stock", "value": 75, "operation": "set"}
        Operations: 'set', 'add_to_list', 'remove_from_list'.
        """
        if not data:
            logger.warning("No JSON data provided for update.")
            return data

        modified_data = copy.deepcopy(data)  # ไม่แก้ข้อมูลต้นฉบับใน data store

        for update in updates:
            path = update.get("path")
            value = update.get("value")
            operation = update.get("operation", "set")

            if path is None:
                logger.warning(f"Update skipped: missing 'path' in update: {update}")
                continue

            keys = path.split('.') if path else []

            if operation == "set":
                if not keys:
                    logger.warning(f"Cannot 'set' the root object. Skipping update: {update}")
                    continue
                found, parent = self._resolve(modified_data, keys[:-1])
                target_key = keys[-1]
                if found and isinstance(parent, dict):
                    parent[target_key] = value
                    logger.info(f"Set '{path}' to '{value}'.")
                elif found and isinstance(parent, list) and target_key.isdigit() and int(target_key) < len(parent):
                    parent[int(target_key)] = value
                    logger.info(f"Set '{path}' (list index) to '{value}'.")
                else:
                    logger.warning(f"Path '{path}' not found. Skipping update: {update}")

            elif operation in ("add_to_list", "remove_from_list"):
                found, target = self._resolve(modified_data, keys)
                if not found or not isinstance(target, list):
                    logger.warning(f"Cannot '{operation}' for path '{path}': target is not a list. Skipping: {update}")
                    continue
                where = f"'{path}'" if path else "root list"
                if operation == "add_to_list":
                    target.append(value)
                    logger.info(f"Added item to {where}.")
                elif value in target:
                    target.remove(value)
                    logger.info(f"Removed '{value}' from {where}.")
                else:
                    logger.warning(f"Value '{value}' not found in {where}. Skipping remove.")

            else:
                logger.warning(f"Unsupported operation '{operation}' for path '{path}'. Skipping update: {update}")

        return modified_data

    def query_json_data(self, data, path):
        """
        Queries a specific element from nested JSON data using a dot-notation path.
        Returns the value or None if not found.
        """
        if not data:
            logger.warning("No JSON data to query.")
            return None

        found, result = self._resolve(data, path.split('.') if path else [])
        if not found:
            logger.warning(f"Query path '{path}' not found.")
            return None

        logger.info(f"Successfully queried '{path}'. Result: {result}")
        return result
