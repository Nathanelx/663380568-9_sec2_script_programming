# Week 12: Final Project — Enhanced Task Manager CLI

**ผู้จัดทำ:** ชื่อ-นามสกุล นายศพล ถิรพงศ์ชาติ**รหัสนักศึกษา:** 663380568-9

โครงงานปลายภาค: Task Manager แบบ Command-Line ฉบับสมบูรณ์ ต่อยอดจากการวางแผนใน Week 11
รวมทุกเรื่องที่เรียนมา: **OOP (Inheritance / Polymorphism)**, **Modular Design**, **JSON Persistence**, **datetime**,
**Error Handling**, **Search / Filter / Sort** และ **Unit Testing**

| ไฟล์ | เนื้อหา |
| --- | --- |
| [`final_task_manager_project/`](final_task_manager_project/) | ซอร์สโค้ดโปรแกรม |
| [`PLAN.md`](PLAN.md) | Requirements, สถาปัตยกรรม, Class Diagram, ปัญหาทางเทคนิคและวิธีแก้, บทเรียน, แผนต่อยอด |
| [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) | รายการตรวจสอบก่อนส่งงานและนำเสนอ |

## ✨ Features

| เมนู | ความสามารถ |
| --- | --- |
| 1 / 2 / 3 | เพิ่มงาน 3 ประเภท: `Task`, `DueDateTask` (วันส่ง `YYYY-MM-DD`), `PriorityTask` (High / Medium / Low) พร้อม **tags** |
| 4 | แสดงงานทั้งหมด |
| 5 / 6 | เปลี่ยนเป็นเสร็จสิ้น / ลบงาน ตาม ID |
| 7 | **Search** คำบางส่วนใน description หรือ tags (ไม่สนตัวพิมพ์เล็ก-ใหญ่) |
| 8 | **Filter** หลายเงื่อนไขพร้อมกัน: สถานะ, ครบกำหนดก่อน / หลังวันที่, priority, tags (ต้องมีครบทุกตัว) |
| 9 | **Sort** ตาม id, description, completed, due_date, priority (Ascending / Descending) |
| 0 | ออกจากโปรแกรม |

ข้อมูลบันทึกลง `data/tasks.json` อัตโนมัติทุกครั้งที่เพิ่ม / แก้ / ลบ และมีงานตัวอย่าง 6 รายการ (ครบทุกประเภท) สำหรับสาธิต

## 🏗️ สถาปัตยกรรม (Separation of Concerns)

```text
final_task_manager_project/
├── main.py                  # Orchestrator: TaskManager + CLIInterface → cli.run()
├── src/
│   ├── cli_interface.py     # Presentation Layer: เมนู, รับ input, validation, แสดงผล
│   ├── task_manager.py      # Business Logic: CRUD, search, filter, sort
│   ├── data_persistence.py  # Data Layer: JSON ↔ objects (ดูจาก "_type")
│   └── task.py              # Models: Task ← DueDateTask, PriorityTask
├── tests/
│   └── test_task_manager.py # Unit tests (8 tests)
├── data/
│   └── tasks.json           # ข้อมูลงาน
└── .gitignore
```

## 🚀 วิธีรัน

ใช้แค่ built-in modules ไม่ต้องติดตั้งอะไรเพิ่ม

```powershell
cd "Lab\Lab12\Lab 12 Final Project Development main\final_task_manager_project"
python main.py
```

รัน unit tests:

```bash
python -m unittest discover tests
```

```text
Ran 8 tests in 0.016s

OK
```

## ✅ ตัวอย่างผลลัพธ์

```text
Enter your choice (0-9): 4

--- Your Tasks (Total: 6) ---
  * ID: 1 | Description: Complete Week 12 Final Project Documentation | Status: Pending | Tags: study, final-project, urgent
  * ID: 2 | Description: Submit OOP Project Source Code to GitHub | Status: Pending | Due: 2026-09-30 | Tags: study, github
  * ID: 3 | Description: Prepare Slides for Final Project Presentation | Status: Pending | Priority: High | Tags: presentation, urgent
  * ID: 4 | Description: Review PEP 8 and Python Docstrings | Status: Completed | Tags: refactor, code-quality
  * ID: 5 | Description: Practice CLI Demo Script with Pre-seeded Data | Status: Pending | Priority: Medium | Tags: demo, presentation
  * ID: 6 | Description: Midterm Examination Review | Status: Completed | Due: 2026-08-20 | Tags: exam, study
------------------------------------------
```

## 🎤 ลำดับการสาธิต (Demo Script แนะนำ)

1. **เมนู 4** แสดงงานตัวอย่าง 6 รายการ (มีครบ 3 ประเภท)
2. **เมนู 7** ค้นหา `study` → เจอ 3 รายการ (จากทั้ง description และ tags)
3. **เมนู 8** กรอง status = `no` และ tags = `presentation` → งาน ID 3 และ 5
4. **เมนู 9** เรียงตาม `priority` → High, Medium แล้วงานที่ไม่มี priority อยู่ท้าย
5. **เมนู 2** เพิ่มงานที่มีวันส่ง ลองใส่วันที่ผิด `31/12/2026` ให้เห็นการ validate
6. **เมนู 5** complete งาน แล้ว **เมนู 4** แสดงสถานะที่เปลี่ยน

## 🛡️ Error Handling

| สถานการณ์ | ผลลัพธ์ |
| --- | --- |
| คำอธิบายว่าง / วันที่ผิดรูปแบบ / priority ไม่ถูกต้อง | แจ้งเตือนแล้วถามใหม่ |
| ID ไม่ใช่ตัวเลข | `[Error] Invalid input. Please enter a valid number for Task ID.` |
| ID ที่ไม่มีในระบบ | `[Notice] Task not found.` |
| วันที่ในตัวกรองผิดรูปแบบ | `[Warning] ... Ignoring.` แล้วกรองด้วยเงื่อนไขที่เหลือ |
| `tasks.json` เสีย หรือมี `_type` ที่ไม่รู้จัก | เตือนแล้วเริ่มด้วยรายการว่าง / ข้ามรายการนั้น |

> หมายเหตุการเรียงลำดับ: เมื่อเรียง `due_date` / `priority` แบบ **Descending** งานที่ไม่มีค่านั้นจะขึ้นมาอยู่ต้นรายการ
> (เพราะใช้ `date.max` / `99` เป็นค่าแทน แล้วกลับลำดับทั้งรายการ) ตามที่อธิบายไว้ใน `PLAN.md` ข้อ 4.4

## 📝 ก่อนส่งงาน

- ใส่ชื่อ-นามสกุลด้านบนของไฟล์นี้
- ทำตาม [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) (ใส่ลิงก์ GitHub ของตัวเอง, เตรียมสไลด์ 7 ส่วน, ซ้อม demo 5-7 นาที)
