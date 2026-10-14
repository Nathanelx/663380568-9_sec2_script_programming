# agentic-data-processor/src/csv_tasks.py
import csv
import operator as op
import os
from collections import defaultdict
from .utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

# map สัญลักษณ์ใน config ไปเป็นฟังก์ชันเปรียบเทียบ
OPERATORS = {
    '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '==': op.eq, '!=': op.ne,
}


class CSVTasks:
    """
    Handles advanced reading, writing, and processing of CSV files.
    All data is handled as a list of dictionaries.
    """
    def __init__(self):
        logger.info("CSVTasks initialized.")

    def load_csv(self, file_path):
        """
        Loads a CSV file and returns its content as a list of dictionaries.
        Assumes the first row is the header.
        """
        if not os.path.exists(file_path):
            logger.error(f"CSV file not found: {file_path}")
            return None

        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                data = list(csv.DictReader(file))
            logger.info(f"Successfully loaded {len(data)} rows from '{file_path}'.")
            return data
        except Exception as e:
            logger.error(f"Error loading CSV file '{file_path}': {e}")
            return None

    def save_csv(self, data, file_path, fieldnames=None):
        """
        Saves a list of dictionaries to a CSV file.
        `fieldnames` can be explicitly provided or inferred from the first dictionary.
        """
        if not data:
            logger.warning("No data provided to save to CSV. File will not be created.")
            return False

        ensure_directory_exists(os.path.dirname(file_path))

        if fieldnames is None:
            if isinstance(data[0], dict):
                fieldnames = list(data[0].keys())
                logger.info(f"Inferred fieldnames for CSV: {fieldnames}")
            else:
                logger.error("Cannot infer fieldnames: data is not a list of dictionaries.")
                return False

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Successfully saved {len(data)} rows to '{file_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error saving CSV file '{file_path}': {e}")
            return False

    def transform_csv_aggregate(self, data, group_by_field, aggregate_field, aggregate_type="sum"):
        """
        Aggregates CSV data (list of dicts) by a specified field.
        Supports 'sum', 'count', 'average'.
        """
        if not data:
            logger.warning("No data to aggregate.")
            return []
        if aggregate_type not in ("sum", "count", "average"):
            logger.error(f"Unsupported aggregation type: {aggregate_type}")
            return None

        aggregated = defaultdict(lambda: {'count': 0, 'sum': 0.0})

        for row in data:
            group_value = row.get(group_by_field)
            if group_value is None:
                logger.warning(f"Skipping row due to missing group_by_field '{group_by_field}': {row}")
                continue
            try:
                aggregated[group_value]['sum'] += float(row.get(aggregate_field, 0))
                aggregated[group_value]['count'] += 1
            except (ValueError, TypeError) as e:
                logger.warning(f"Skipping row due to invalid '{aggregate_field}': {row}. Error: {e}")

        results = []
        for group_value, metrics in aggregated.items():
            result_row = {group_by_field: group_value}
            if aggregate_type == "sum":
                result_row[f'Total_{aggregate_field}'] = round(metrics['sum'], 2)
            elif aggregate_type == "count":
                result_row[f'Count_{aggregate_field}'] = metrics['count']
            else:
                result_row[f'Average_{aggregate_field}'] = round(metrics['sum'] / metrics['count'], 2)
            results.append(result_row)

        logger.info(f"Aggregated data by '{group_by_field}' using '{aggregate_type}'. Produced {len(results)} rows.")
        return results

    def filter_csv(self, data, filter_field, operator, value):
        """
        Filters CSV data (list of dicts) based on a condition.
        `operator` can be '>', '<', '>=', '<=', '==', '!='.
        If `value` is a number, the field is compared as a number; otherwise as a string.
        """
        if not data:
            logger.warning("No data to filter.")
            return []
        compare = OPERATORS.get(operator)
        if compare is None:
            logger.error(f"Unsupported filter operator: '{operator}'.")
            return None

        filtered_data = []
        for row in data:
            field_value = row.get(filter_field)
            if field_value is None:
                logger.debug(f"Skipping row in filter due to missing field '{filter_field}': {row}")
                continue
            try:
                if isinstance(value, (int, float)):
                    field_value = float(field_value)
                if compare(field_value, value):
                    filtered_data.append(row)
            except ValueError as e:
                logger.warning(f"Type conversion error during filter for row: {row}. Error: {e}")

        logger.info(f"Filtered data by '{filter_field} {operator} {value}'. Resulted in {len(filtered_data)} rows.")
        return filtered_data
