# Mini Project: ระบบยืมหนังสือ

## Project Overview

ระบบยืม-คืนหนังสือ command-line application จำลองการทำงานของห้องสมุดขนาดเล็ก  

## Kanban Backlog Run

| state | Concept | ใช้ใน Library System | ไฟล์/ฟังก์ชัน |
|---|---|---|---|
|D1| `dict` + nested dict | เก็บ books, members แบบ key-value | `books = {}`, `members = {}` |
|D1| `list` | borrow_log แบบ append-only | `borrow_log = []` |
|D1| `f-string` + format spec `:<N>` | จัดคอลัมน์ให้ตรงกัน | `list_books()` |
|D1| `input()` + type conversion | รับค่าจากผู้ใช้ | `_ui_*()` ทุกตัว |
|D1| `if-elif-else` + logical operators | validation 4 ขั้นใน borrow | `borrow_book()` |
|D2| `for` loop + `while True` | เมนูหลัก + วน loop | `main_menu()` |
|D2| `break` + `continue` | ออกจาก loop / ข้ามรายการ | `main_menu()`, `list_books()` |
|D2| list methods `.append()` `.remove()` | เพิ่ม/ลบ ISBN ในรายการยืม | `borrowed_books` |
|D2| `dict.get(key, default)` | safe access ไม่ crash | `view_report()`, `my_loans()` |
|D2| `dict.items()` | วน loop key-value | `list_books()`, `view_report()` |
|D2| `def` + `return` + type hints | ทุก function มี signature ชัดเจน | ทุก function |
|D2| docstring | อธิบาย Args, Returns, Raises | ทุก function |
|D3| `try` / `except` / `raise` | จับและโยน KeyError, ValueError | `main_menu()` + core functions |
|D3| `next()` + generator expression | หา log entry แรกที่ตรงเงื่อนไข | `return_book()` |
|D3| `lambda` + `sorted()` | เรียงหนังสือยอดนิยม | `view_report()` |
|เพิ่มเติมหลังพรี| **`json.dump()` / `json.load()`** | **บันทึก/โหลด dict ↔ JSON file** | **`save_data()`, `load_data()`** |
|เพิ่มเติมหลังพรี| **`os.path.exists()`** | **ตรวจไฟล์มีอยู่ก่อน load** | **`load_data()`** |
|เพิ่มเติมหลังพรี| **`global` keyword** | **แก้ counter นอก function** | **`_book_id`, `_member_id`** |
|เพิ่มเติมหลังพรี| **Auto-increment ID** | **ISBN001, M001 อัตโนมัติ** | **`_ui_add_book()`, `_ui_register()`** |

## Group Learning Outcomes

## group grading rubric

### group assessments

|ผู้ประเมิน|ประเมิน ธนภัทร|ประเมิน ยศพล|ประเมิน ศุภชัย|ประเมิน ภาวัต |
|---|---|---|---|---|
|นายธนภัทร สมบูรณ์|10|10|10|10|
|นายยศพล ถิรพงศ์ชาติ|10|10|10|10|
|นายศุภชัย คนเพียร|10|10|10|10|
|นายภาวัต วงศ์มาลาสิทธิ์|10|10|10|10|
