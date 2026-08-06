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

---

## Group Learning Outcomes

**1. Data Structure Selection**  
เลือก `dict` สำหรับ books และ members เพราะค้นหาด้วย ISBN / member_id ได้เร็ว O(1) ไม่ต้องวนหาทั้งรายการแบบ list ที่ช้า O(n)

**2. Append-only Log Pattern**  
`borrow_log` เป็น list ที่เพิ่มอย่างเดียว ไม่ลบ — "คืนหนังสือ" คือการอัปเดต `returned_date` ไม่ใช่การลบ entry เหมือน bank statement และ git commit ที่ประวัติไม่หายไป

**3. Validate Before Mutate**  
`borrow_book()` ตรวจสอบเงื่อนไขทั้ง 4 ขั้นให้ผ่านก่อน แล้วค่อยแก้ไข data ในขั้นตอนเดียว — ถ้าแก้ data กลางทางแล้วเกิด error จะทำให้ข้อมูลเสียหายบางส่วน

**4. next() + Generator Expression**  
`next((e for e in borrow_log if condition), None)` หา log entry แรกที่ตรงเงื่อนไขแล้วหยุดทันที ดีกว่า for loop + flag variable เพราะอ่านง่ายและประหยัดกว่า

**5. UI / Core Separation**  
`_ui_*()` functions ทำหน้าที่รับ input แล้วส่งต่อให้ core functions เท่านั้น core functions ไม่รู้จัก `input()` เลย ทำให้ทดสอบ core ได้โดยไม่ต้องกด keyboard

**6. Data Persistence — json module**  
`json.dump()` แปลง dict/list เป็น text เก็บในไฟล์ และ `json.load()` อ่านกลับมาเป็น dict/list ได้ทันที Pattern: load ตอนเปิดโปรแกรม → ใช้งาน → save ตอนออก เหมือนทุก application จริง

**7. Defensive Programming — os.path.exists()**  
ตรวจว่าไฟล์มีอยู่ก่อน load เสมอ เพราะรันครั้งแรกยังไม่มีไฟล์ ถ้าไม่ตรวจจะเกิด FileNotFoundError crash ทันที

**8. Auto-increment ID**  
`f"ISBN{_book_id:03d}"` สร้าง ISBN001, ISBN002 อัตโนมัติ — format spec `:03d` จอง 3 หลักเติม 0 นำหน้า ทำให้ sort ได้ถูกต้องและดูเป็นระเบียบ

### ด้าน Process

**9. Incremental Development**  
พัฒนาจาก v1.0 → v2.0 โดยเพิ่มฟีเจอร์ทีละอย่าง ไม่เขียนใหม่ทั้งหมด ทำให้รู้ว่า bug ใหม่เกิดจากส่วนที่เพิ่งเพิ่ม

**10. AI-assisted Learning**  
ใช้ AI ถาม-ตอบแต่ละ concept แล้วบันทึกใน LEARNINGLOG ทุกครั้ง — prompt ที่ดีต้องมี context + problem + constraint และต้องอ่านทำความเข้าใจคำตอบก่อนใช้งาน ไม่ copy-paste ตาบอด

---

## Group Grading Rubric

| หมวด | คะแนน | ดีเยี่ยม (A 90%+) | ผ่านเกณฑ์ (B 75–89%) | กำลังพัฒนา (C 60–74%) | เริ่มต้น (F <60%) |
|---|---|---|---|---|---|
| **A. Core Functions** | 25 | ทุก function ทำงานถูกต้อง + validation ครบ 4 ขั้น + error message ชัดเจน | ส่วนใหญ่ถูกต้อง มี validation หลัก | ทำงานได้บางส่วน | ยังทำไม่ได้ |
| **B. File I/O** | 20 | save/load ทำงานได้ + ข้อมูลไม่หายหลัง restart + ตรวจ os.path.exists() | save/load ได้แต่มีกรณีที่พัง | มีโค้ดแต่ยังไม่ทำงาน | ไม่มี |
| **C. Auto-increment ID** | 15 | ISBN และ M_ID สร้างอัตโนมัติถูกต้อง + format :03d + บันทึกลงไฟล์ได้ | ทำงานได้แต่ format ผิด | มีแนวคิดแต่ไม่ครบ | ไม่มี |
| **D. Error Handling** | 15 | try/except ทุกจุด + raise ถูกประเภท (KeyError/ValueError) + message บอก context | ครอบคลุม happy path + error หลัก | มีบางส่วน | ไม่มี |
| **E. Code Quality** | 15 | docstring + type hints + ชื่อตัวแปรสื่อความหมาย + comment อธิบาย logic | ส่วนใหญ่มี docstring | minimal comment | ไม่มี |
| **F. AI Learning Process** | 10 | LEARNINGLOG ≥ 3 prompts + I_LEARNED เขียนด้วยคำตัวเอง + Changelog อัปเดต | ≥ 1 prompt + changelog | มีแต่ copy-paste จาก AI | ไม่มีเลย |
| **รวม** | **100** | **90–100** | **75–89** | **60–74** | **< 60** |

---

## Group assessments

|ผู้ประเมิน|ประเมิน ธนภัทร|ประเมิน ยศพล|ประเมิน ศุภชัย|ประเมิน ภาวัต |
|---|---|---|---|---|
|นายธนภัทร สมบูรณ์|10|10|10|10|
|นายยศพล ถิรพงศ์ชาติ|10|10|10|10|
|นายศุภชัย คนเพียร|10|10|10|10|
|นายภาวัต วงศ์มาลาสิทธิ์|10|10|10|10|
