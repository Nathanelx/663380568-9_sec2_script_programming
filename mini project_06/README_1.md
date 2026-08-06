# 📚 Mini Project: ระบบยืมหนังสือ (Library Borrowing System)

**วิชา**: CP352301 Python Fundamentals  
**กลุ่ม**: [ใส่ชื่อกลุ่ม]  
**สมาชิก**:
- [ชื่อ-สกุล] รหัส [xxxxxxxxx]
- [ชื่อ-สกุล] รหัส [xxxxxxxxx]
- [ชื่อ-สกุล] รหัส [xxxxxxxxx]

---

## Project Overview

ระบบยืม-คืนหนังสือ command-line application จำลองการทำงานของห้องสมุดขนาดเล็ก  
**v2.0** เพิ่มระบบบันทึกข้อมูลลงไฟล์ JSON และ Auto-increment ID

**Real-world use case**: ห้องสมุดมหาวิทยาลัย (OPAC), ระบบยืม e-book (Kindle/Libby), IT Asset Tracking

---

## Project Files

| ไฟล์ | คำอธิบาย |
|---|---|
| `sourcecode (3).ipynb` | Source code v2.0 + demo (ไฟล์ล่าสุด) |
| `library_data.json` | ไฟล์เก็บข้อมูลที่สร้างขึ้นเมื่อรันโปรแกรม |
| `README.md` | ภาพรวมโปรเจกต์ (ไฟล์นี้) |
| `CHANGELOG.md` | บันทึกการเปลี่ยนแปลง v1.0 → v2.0 |
| `LEARNINGLOG.md` | บันทึก AI prompts และ insights |

---

## 1. Kanban Backlog Run

### ✅ Done — Python Concepts ที่ใช้ในโปรเจกต์

| Week | Concept | ใช้ใน Library System | ไฟล์/ฟังก์ชัน |
|---|---|---|---|
| W1 | `dict` + nested dict | เก็บ books, members แบบ key-value | `books = {}`, `members = {}` |
| W1 | `list` | borrow_log แบบ append-only | `borrow_log = []` |
| W1 | `f-string` + format spec `:<N>` | จัดคอลัมน์ให้ตรงกัน | `list_books()` |
| W1 | `input()` + type conversion | รับค่าจากผู้ใช้ | `_ui_*()` ทุกตัว |
| W2 | `if-elif-else` + logical operators | validation 4 ขั้นใน borrow | `borrow_book()` |
| W3 | `for` loop + `while True` | เมนูหลัก + วน loop | `main_menu()` |
| W3 | `break` + `continue` | ออกจาก loop / ข้ามรายการ | `main_menu()`, `list_books()` |
| W4 | list methods `.append()` `.remove()` | เพิ่ม/ลบ ISBN ในรายการยืม | `borrowed_books` |
| W5 | `dict.get(key, default)` | safe access ไม่ crash | `view_report()`, `my_loans()` |
| W5 | `dict.items()` | วน loop key-value | `list_books()`, `view_report()` |
| W6 | `def` + `return` + type hints | ทุก function มี signature ชัดเจน | ทุก function |
| W6 | docstring | อธิบาย Args, Returns, Raises | ทุก function |
| W6 | `try` / `except` / `raise` | จับและโยน KeyError, ValueError | `main_menu()` + core functions |
| W6 | `next()` + generator expression | หา log entry แรกที่ตรงเงื่อนไข | `return_book()` |
| W6 | `lambda` + `sorted()` | เรียงหนังสือยอดนิยม | `view_report()` |
| **W7** | **`json.dump()` / `json.load()`** | **บันทึก/โหลด dict ↔ JSON file** | **`save_data()`, `load_data()`** |
| **W7** | **`os.path.exists()`** | **ตรวจไฟล์มีอยู่ก่อน load** | **`load_data()`** |
| **W7** | **`global` keyword** | **แก้ counter นอก function** | **`_book_id`, `_member_id`** |
| **W7** | **Auto-increment ID** | **ISBN001, M001 อัตโนมัติ** | **`_ui_add_book()`, `_ui_register()`** |

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

