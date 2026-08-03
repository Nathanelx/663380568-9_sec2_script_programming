# 📚 Mini Project: ระบบยืมหนังสือ (Library Borrowing System)

**วิชา**: CP352301 Python Fundamentals  
**กลุ่ม**: [ใส่ชื่อกลุ่ม]  
**สมาชิก**:
- [ชื่อ-สกุล] รหัส [xxxxxxxxx]
- [ชื่อ-สกุล] รหัส [xxxxxxxxx]
- [ชื่อ-สกุล] รหัส [xxxxxxxxx]

---

## Project Overview

ระบบยืม-คืนหนังสือ command-line application จำลองการทำงานของห้องสมุดขนาดเล็ก ครอบคลุม Python fundamentals ตั้งแต่ Week 1–6

**Real-world use case**: ห้องสมุดมหาวิทยาลัย, ระบบยืม e-book, IT Asset Tracking

---

## Project Files

| ไฟล์ | คำอธิบาย |
|---|---|
| `Week5_Library_System.ipynb` | Source code หลัก + demo + tests |
| `README.md` | ภาพรวมโปรเจกต์ (ไฟล์นี้) |
| `CHANGELOG.md` | บันทึกการเปลี่ยนแปลงและสิ่งที่เรียนรู้ |
| `LEARNINGLOG.md` | บันทึก AI prompts และ insights รายวัน |
| `TEST.md` | รายงานผลการทดสอบ |

---

## Kanban Backlog Run

### ✅ Done — Python Concepts ที่ใช้ในโปรเจกต์

| Week | Topic | นำมาใช้ใน Library System |
|---|---|---|
| W1 | variables, dict, list, f-string | DATA LAYER: books, members, borrow_log |
| W1 | input(), type conversion | _ui_*() helper functions รับ input |
| W2 | if-elif-else, logical operators | validation 4 ขั้นใน borrow_book() |
| W3 | for loop, while True | main_menu() loop, list comprehension search |
| W4 | list methods, tuple unpacking | seed_data(), sorted(), list comprehension |
| W5 | dict .get(), nested dict | books/members nested structure, .get() safe access |
| W5 | set | ISBN uniqueness check |
| W6 | functions, docstring, type hints | ทุก function มี docstring + type hints |
| W6 | try/except/raise | KeyError, ValueError validation ครบทุก function |
| W6 | next() + generator | return_book() หา log entry |

### 🔄 In Progress (WIP ≤ 2)

- บันทึกข้อมูลลงไฟล์ .json (file I/O)
- เพิ่มระบบจองหนังสือ (reservation system)

### 📋 Backlog — Feature ที่วางแผนจะเพิ่ม

- [ ] บันทึก borrow_log เป็น `.json` เพื่อ persistence
- [ ] ระบบจองหนังสือเมื่อหนังสือไม่ว่าง
- [ ] ระบบรีวิวและให้คะแนน (1-5 ดาว)
- [ ] รายงาน overdue list และ member stats
- [ ] OOP refactor: `class Library`, `class Book`, `class Member`
- [ ] Web API ด้วย Flask

---

## Group Learning Outcomes

หลังจากทำโปรเจกต์นี้ กลุ่มของเราเรียนรู้ว่า:

### ด้าน Technical

1. **Data Design**: `dict` ซ้อน `dict` คือ pattern เดียวกับ JSON API และ database record จริง
2. **Append-only log**: `borrow_log` ไม่ลบ — เหมือน bank transaction log และ git commit history (audit trail)
3. **`next()` + generator**: วิธี Pythonic ในการหา item แรกที่ตรงเงื่อนไขใน list
4. **Validate before mutate**: ตรวจสอบทุก input ก่อนแก้ไข data — ถ้า validate หลัง data อาจเสียหายบางส่วน
5. **UI vs Core separation**: `_ui_*()` functions แยกจาก core logic ทำให้ core เป็น pure function ที่ test ง่าย

### ด้าน Process

6. **AI Co-Learning**: การถาม AI ด้วย prompt ที่ชัดเจนได้คำตอบที่ดีกว่า — ต้องระบุ context, constraint, และ expected output
7. **Incremental development**: เริ่มจาก seed_data() → core functions → UI → testing — ทำทีละส่วนง่ายกว่า

---

## Group Grading Rubric

| หมวด | คะแนน | เกณฑ์ A | เกณฑ์ B | เกณฑ์ C |
|---|---|---|---|---|
| **A. Core Functions** | 30 | ทำงานถูกต้องทุก function + validation ครบ | ทำงานได้ส่วนใหญ่ มี validation | บางส่วนทำงาน |
| **B. Data Design** | 20 | dict/list design เหมาะสม + อธิบายเหตุผลได้ | design ถูกต้อง อธิบายได้บางส่วน | design มีข้อผิดพลาด |
| **C. Error Handling** | 15 | try/except + raise ครบทุก edge case + message ชัด | ครอบคลุม happy path + บาง error | มีแค่ happy path |
| **D. Testing** | 15 | test ครบ happy/edge/error cases + overdue | test หลักๆ ครบ | test บางส่วน |
| **E. Code Quality** | 10 | docstring + type hints + ชื่อตัวแปรชัด + comment | ส่วนใหญ่มี docstring | minimal comment |
| **F. AI Learning Process** | 10 | LEARNINGLOG ≥ 3 prompts + my_understanding + changelog | ≥ 1 prompt + changelog | มีแต่ไม่สมบูรณ์ |
| **รวม** | **100** | **90–100** | **75–89** | **60–74** |

---

## Group Assessment (Self & Peer)

### การประเมินตนเอง

| สมาชิก | หน้าที่หลัก | ความรับผิดชอบ | คะแนนตนเอง /10 |
|---|---|---|---|
| [ชื่อ 1] | Core functions (borrow/return) | [ระบุ] | [x] |
| [ชื่อ 2] | UI, seed_data, testing | [ระบุ] | [x] |
| [ชื่อ 3] | Documentation, CHANGELOG, LEARNINGLOG | [ระบุ] | [x] |

## How to Run

```bash
# วิธีที่ 1: Jupyter Notebook / Google Colab
# เปิด Week5_Library_System.ipynb แล้วรัน cells ตามลำดับ

# วิธีที่ 2: Python terminal
python library_system.py
```

**Dependencies**: Python 3.8+ (ไม่มี external library — ใช้แค่ `datetime` ที่มากับ standard library)

---

## Resources

- [Google Classroom](https://classroom.google.com/c/ODU1MTkyMjcwMTQ2?cjc=aze7m237) — รหัส `aze7m237`
- [Drive](https://drive.google.com/drive/folders/12wiiYWYl8GG8-YYeCSlYHQh8rZLqEU29)
- [NotebookLM](https://notebooklm.google.com/notebook/936b004b-36ff-41cf-ab75-49adc6949af0)
