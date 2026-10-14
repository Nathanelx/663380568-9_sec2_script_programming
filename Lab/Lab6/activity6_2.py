# --- Activity 6.2: Standard Library Exploration ---
# ตัวอย่างการใช้โมดูลใน Python Standard Library (https://docs.python.org/3/library/)
# ดูสรุปการอภิปรายเรื่องข้อดีของ Modular Programming ใน activity6_2.md

import datetime
import os
import sys
from collections import Counter


# 1) datetime - จัดการวันที่และเวลา เช่น คำนวณจำนวนวันก่อนถึงวันสอบ
today = datetime.date.today()
exam_day = datetime.date(today.year, 12, 15)
if exam_day < today:
    exam_day = exam_day.replace(year=today.year + 1)
print(f"Today: {today:%d/%m/%Y}")
print(f"Days until exam ({exam_day}): {(exam_day - today).days} days")

# 2) os - ทำงานกับไฟล์/โฟลเดอร์ เช่น แสดงไฟล์ .py ในโฟลเดอร์นี้
folder = os.path.dirname(os.path.abspath(__file__))
py_files = [f for f in os.listdir(folder) if f.endswith(".py")]
print(f"Python files in {os.path.basename(folder)}: {sorted(py_files)}")

# 3) sys - ข้อมูลเกี่ยวกับ Python interpreter
print(f"Python version: {sys.version.split()[0]}")
print(f"Platform: {sys.platform}")

# 4) collections.Counter - นับความถี่ของข้อมูล เช่น นับตัวอักษรในคำ
word = "programming"
counts = Counter(word)
print(f"Letter counts in '{word}': {dict(counts)}")
print(f"Most common 2 letters: {counts.most_common(2)}")
