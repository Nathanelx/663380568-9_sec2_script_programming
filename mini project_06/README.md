# Mini Project: ระบบยืมหนังสือ

## Project Overview

ระบบยืม-คืนหนังสือ command-line application จำลองการทำงานของห้องสมุดขนาดเล็ก  

## 1. Kanban Backlog Run

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

### 🔄 In Progress (WIP ≤ 2)
- เตรียมนำเสนอ 10-15 นาที
- ทำ GitHub artifacts ครบชุด

### 📋 Backlog — Feature ที่วางแผนจะทำต่อ

| Priority | Feature | เหตุผล |
|---|---|---|
| สูง | OOP refactor: `class Library`, `class Book`, `class Member` | แก้ปัญหา global variable, code อ่านง่ายขึ้น |
| สูง | `with open()` ใน save/load | ปลอดภัยกว่า ปิดไฟล์อัตโนมัติ |
| กลาง | ระบบจองหนังสือเมื่อหนังสือไม่ว่าง | user experience ดีขึ้น |
| กลาง | Pandas: วิเคราะห์ borrow_log เป็น DataFrame | สถิติการยืมรายเดือน |
| ต่ำ | Flask: web API | เปลี่ยนจาก CLI เป็น web |
| ต่ำ | SQLite: แทน JSON file | รองรับข้อมูลขนาดใหญ่ |

---

## 2. Group Learning Outcomes

หลังจากทำโปรเจกต์นี้ครบทั้ง v1.0 และ v2.0 กลุ่มของเราเรียนรู้ว่า:


- ถ้า test ผ่านหมด = มั่นใจว่าไม่ได้ทำ feature ใหม่แล้วทำของเก่าพัง

---

---


### Peer Assessment — สมาชิกในกลุ่มประเมินกัน

| ประเมินโดย ↓ / ประเมิน → | [ชื่อ 1] | [ชื่อ 2] | [ชื่อ 3] |
|---|---|---|---|
| [ชื่อ 1] | — | [x/10] | [x/10] |
| [ชื่อ 2] | [x/10] | — | [x/10] |
| [ชื่อ 3] | [x/10] | [x/10] | — |

