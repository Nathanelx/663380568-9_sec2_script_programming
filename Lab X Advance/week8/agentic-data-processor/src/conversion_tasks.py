# agentic-data-processor/src/conversion_tasks.py
import json
from .utils import setup_logging

logger = setup_logging(__name__)


def _convert_value(value):
    """แปลง string จาก CSV ให้เป็นชนิดข้อมูลที่เหมาะสม (int, float, bool, None)"""
    if value is None:
        return None
    text = value.strip()
    if text == '' or text.lower() == 'null':
        return None
    if text.lower() in ('true', 'false'):
        return text.lower() == 'true'
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text


class ConversionTasks:
    """
    Handles conversions between CSV (list of dicts) and JSON formats.
    """
    def __init__(self):
        logger.info("ConversionTasks initialized.")

    def csv_to_json(self, csv_data):
        """
        Converts CSV data (list of dictionaries of strings) to JSON-friendly data.
        Numeric strings become numbers, "true"/"false" become booleans, empty becomes null.
        """
        if not csv_data:
            logger.warning("No CSV data to convert to JSON.")
            return []

        json_data = [{key: _convert_value(value) for key, value in row.items()} for row in csv_data]
        logger.info(f"Converted {len(csv_data)} CSV rows to JSON format.")
        return json_data

    def json_to_csv(self, json_data, fieldnames=None):
        """
        Converts JSON data (list of dictionaries) to flat CSV rows.
        Nested dicts are flattened one level as "parent.child" (e.g. details.brand).
        Lists are stored as JSON strings.
        Returns (rows, fieldnames).
        """
        if not json_data:
            logger.warning("No JSON data to convert to CSV.")
            return [], []

        if fieldnames is None:
            fieldnames = []
            for item in json_data:
                for key, value in item.items():
                    names = [f"{key}.{sub}" for sub in value] if isinstance(value, dict) else [key]
                    for name in names:
                        if name not in fieldnames:  # เก็บลำดับคอลัมน์ตามที่เจอครั้งแรก
                            fieldnames.append(name)
            logger.info(f"Inferred fieldnames for JSON to CSV: {fieldnames}")

        csv_rows = []
        for item in json_data:
            row = {}
            for field in fieldnames:
                if '.' in field:
                    parent, child = field.split('.', 1)
                    nested = item.get(parent)
                    value = nested.get(child, '') if isinstance(nested, dict) else ''
                else:
                    value = item.get(field, '')
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                row[field] = value
            csv_rows.append(row)

        logger.info(f"Converted {len(json_data)} JSON objects to CSV format.")
        return csv_rows, fieldnames
