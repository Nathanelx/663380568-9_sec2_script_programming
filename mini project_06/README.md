# Mini Project: ระบบยืมหนังสือ

## Project Overview

ระบบยืม-คืนหนังสือ command-line application จำลองการทำงานของห้องสมุดขนาดเล็ก  

## Kanban Backlog Run

| Concept | ใช้ใน Library System | ไฟล์/ฟังก์ชัน |
|---|---|---|
| `dict` + nested dict | เก็บ books, members แบบ key-value | `books = {}`, `members = {}` |
| `list` | borrow_log แบบ append-only | `borrow_log = []` |
| `f-string` + format spec `:<N>` | จัดคอลัมน์ให้ตรงกัน | `list_books()` |
| `input()` + type conversion | รับค่าจากผู้ใช้ | `_ui_*()` ทุกตัว |
| `if-elif-else` + logical operators | validation 4 ขั้นใน borrow | `borrow_book()` |
| `for` loop + `while True` | เมนูหลัก + วน loop | `main_menu()` |
| `break` + `continue` | ออกจาก loop / ข้ามรายการ | `main_menu()`, `list_books()` |
| list methods `.append()` `.remove()` | เพิ่ม/ลบ ISBN ในรายการยืม | `borrowed_books` |
| `dict.get(key, default)` | safe access ไม่ crash | `view_report()`, `my_loans()` |
| `dict.items()` | วน loop key-value | `list_books()`, `view_report()` |
| `def` + `return` + type hints | ทุก function มี signature ชัดเจน | ทุก function |
| docstring | อธิบาย Args, Returns, Raises | ทุก function |
| `try` / `except` / `raise` | จับและโยน KeyError, ValueError | `main_menu()` + core functions |
| `next()` + generator expression | หา log entry แรกที่ตรงเงื่อนไข | `return_book()` |
| `lambda` + `sorted()` | เรียงหนังสือยอดนิยม | `view_report()` |
|Update| **`json.dump()` / `json.load()`** | **บันทึก/โหลด dict ↔ JSON file** | **`save_data()`, `load_data()`** |
|Update| **`os.path.exists()`** | **ตรวจไฟล์มีอยู่ก่อน load** | **`load_data()`** |
|Update| **`global` keyword** | **แก้ counter นอก function** | **`_book_id`, `_member_id`** |
|Update| **Auto-increment ID** | **ISBN001, M001 อัตโนมัติ** | **`_ui_add_book()`, `_ui_register()`** |



## Group Learning Outcomes

หลังจากทำโปรเจกต์นี้ครบทั้ง v1.0 และ v2.0 กลุ่มของเราเรียนรู้ว่า:


- ถ้า test ผ่านหมด = มั่นใจว่าไม่ได้ทำ feature ใหม่แล้วทำของเก่าพัง

---

---

## group grading rubric

### group assessments

|ผู้ประเมิน|ประเมิน ธนภัทร|ประเมิน ยศพล|ประเมิน ศุภชัย|ประเมิน ภาวัต |
|นายธนภัทร สมบูรณ์|10|10|10|10|
|นายยศพล ถิรพงศ์ชาติ|10|10|10|10|
|นายศุภชัย คนเพียร|10|10|10|10|
|นายภาวัต วงศ์มาลาสิทธิ์|10|10|10|10|
