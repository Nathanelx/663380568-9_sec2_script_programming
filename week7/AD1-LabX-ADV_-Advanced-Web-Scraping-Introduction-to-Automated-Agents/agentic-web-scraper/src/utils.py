# agentic-web-scraper/src/utils.py
import csv
import json
import os
import time
from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def save_data_to_json(data: List[Dict[str, Any]], filepath: str):
    """บันทึกข้อมูลเป็นไฟล์ JSON"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_data_to_csv(data: List[Dict[str, Any]], filepath: str):
    """บันทึกข้อมูลเป็นไฟล์ CSV (utf-8-sig เพื่อให้เปิดใน Excel ได้ถูกต้อง)"""
    if not data:
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def wait_for_element(driver, selector: str, timeout: int = 10, by: By = By.CSS_SELECTOR):
    """Explicit wait: รอจนกว่า element จะปรากฏในหน้า"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )


def safe_click(driver, element):
    """เลื่อนหน้าให้เห็น element ก่อน แล้วค่อยคลิก"""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.5)
    element.click()


def retry(func, max_retries: int = 3, delay: float = 2):
    """เรียก func ซ้ำได้สูงสุด max_retries ครั้งหากเกิดข้อผิดพลาดชั่วคราว"""
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                raise
            print(f"  Attempt {attempt} failed ({type(e).__name__}), retrying in {delay}s...")
            time.sleep(delay)
