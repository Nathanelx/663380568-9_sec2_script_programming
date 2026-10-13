# Class Activity 4: Enhanced Task Manager (Project Planning & Design)

Week 11: **Project Planning & Design: Building an Enhanced Task Manager**

ต่อยอด Task Manager จาก Class Activity 1-2 โดยเริ่มจาก **วางแผนและออกแบบ** ก่อนเขียนโค้ด (ดู [`PLAN.md`](PLAN.md))
แล้วจัดโครงสร้างใหม่ตามหลัก **Separation of Concerns** แยกเป็น 4 ชั้น และเพิ่มความสามารถ
**Tags, Search, Filter, Sort**

## 🏗️ สถาปัตยกรรม

```text
main.py  (Orchestrator: สร้าง TaskManager + CLIInterface แล้วเริ่ม cli.run())
   │
   ▼
cli_interface.py   ── Presentation Layer: เมนู, รับ input, ตรวจรูปแบบ, แสดงผล (ไม่มี business logic)
   │
   ▼
task_manager.py    ── Business Logic Layer: add / complete / delete / search / filter / sort
   │         ╲
   ▼          ╲──► task.py  ── Domain Models: Task, DueDateTask(Task), PriorityTask(Task)
data_persistence.py ── Data Layer: โหลด/บันทึก data/tasks.json (แปลง JSON ↔ object ตาม "_type")
```

| ไฟล์ | หน้าที่ |
| --- | --- |
| `src/task.py` | คลาส `Task` (มี `tags`), `DueDateTask` (มี `due_date`), `PriorityTask` (มี `priority`) — inheritance + polymorphism ของ `to_dict()` / `__str__()` |
| `src/data_persistence.py` | `DataPersistence.load_tasks()` / `save_tasks()` จัดการไฟล์ JSON ทั้งหมด |
| `src/task_manager.py` | `TaskManager` จัดการรายการงาน ไม่ยุ่งกับไฟล์หรือ input/output โดยตรง |
| `src/cli_interface.py` | `CLIInterface` เมนู 0-9 และ validation ของ input |
| `main.py` | จุดเริ่มต้นโปรแกรม |
| `PLAN.md` | เอกสารวางแผน: requirements, architecture, class diagram, ความท้าทาย |

## ✨ เมนู

| เมนู | ความสามารถ |
| --- | --- |
| 1 | เพิ่มงานทั่วไป + tags |
| 2 | เพิ่มงานที่มีวันครบกำหนด (ตรวจรูปแบบ `YYYY-MM-DD`) + tags |
| 3 | เพิ่มงานที่มีระดับความสำคัญ (High / Medium / Low) + tags |
| 4 | แสดงงานทั้งหมด |
| 5 | เปลี่ยนสถานะงานเป็นเสร็จสิ้น |
| 6 | ลบงาน |
| 7 | **ค้นหา** คำใน description หรือ tags (ไม่สนตัวพิมพ์เล็ก/ใหญ่) |
| 8 | **กรอง** ตามสถานะ, ครบกำหนดก่อนวันที่, ความสำคัญ, tag (ใช้หลายเงื่อนไขพร้อมกันได้) |
| 9 | **เรียงลำดับ** ตาม id / due_date / priority (น้อยไปมาก หรือ มากไปน้อย) |
| 0 | ออกจากโปรแกรม |

### Assignment: Search / Filter / Sort

ในโค้ดตัวอย่าง (scaffold) ทั้ง 3 ฟังก์ชันใน `task_manager.py` เป็น placeholder ที่พิมพ์ `[DEBUG] ... ยังไม่ได้ถูก Implement`
โปรเจกต์นี้ implement แล้วตามแนวทางใน `PLAN.md`:

- `search_tasks(keyword)` — คืนงานที่ keyword อยู่ใน description หรือ tag
- `filter_tasks(status, due_date_before, priority, tags)` — กรองทีละเงื่อนไข (เงื่อนไขที่เว้นว่างจะข้าม) ถ้าวันที่ผิดรูปแบบจะแจ้งเตือน
- `sort_tasks(criterion, reverse)` — งานที่ไม่มี `due_date` / `priority` จะอยู่ท้ายรายการเสมอ
  (แก้ปัญหา "Sorting Heterogeneous Objects" ใน `PLAN.md` ข้อ 5)

## 🚀 วิธีรัน

ใช้แค่ built-in modules ไม่ต้องติดตั้งอะไรเพิ่ม

```powershell
cd "Class activity\Class activity 4\enhanced-task-manager-design"
python main.py
```

## ✅ ตัวอย่างผลลัพธ์

```text
เลือกเมนู (0-9): 4

--- รายการงานทั้งหมด (4 รายการ) ---
- ID: 1 | Description: อ่านเอกสาร PLAN.md และทำความเข้าใจสถาปัตยกรรม | Status: Completed | Tags: study, architecture, week11
- ID: 2 | Description: ส่งงานโปรเจกต์ Task Manager ฉบับสมบูรณ์ | Status: Pending | Due: 2026-09-30 | Tags: assignment, university
- ID: 3 | Description: Implement ฟังก์ชัน search_tasks, filter_tasks และ sort_tasks | Status: Pending | Priority: High | Tags: coding, python, priority
- ID: 4 | Description: ทบทวนการทำงานของ Data Persistence และ JSON Serialization | Status: Pending | Priority: Medium | Tags: review, python

เลือกเมนู (0-9): 7
กรอกคำค้นหา (Keyword): python

--- ผลการค้นหาสำหรับ 'python' (2 รายการ) ---
- ID: 3 | ... | Priority: High | Tags: coding, python, priority
- ID: 4 | ... | Priority: Medium | Tags: review, python

เลือกเมนู (0-9): 9
เรียงตาม (id / due_date / priority) [ค่าเริ่มต้น: id]: priority
เรียงจากมากไปน้อย (Descending? y/n) [ค่าเริ่มต้น: n]: n

--- รายการงานที่จัดเรียงแล้ว (เกณฑ์: priority) ---
- ID: 3 | ... | Priority: High | ...
- ID: 4 | ... | Priority: Medium | ...
- ID: 1 | ... (ไม่มี priority อยู่ท้าย)
- ID: 2 | ...
```

## 🛡️ Error Handling

| สถานการณ์ | ผลลัพธ์ |
| --- | --- |
| รายละเอียดงานว่าง | ถามใหม่จนกว่าจะกรอก |
| วันที่ผิดรูปแบบ เช่น `2021-13-40` | แจ้ง "รูปแบบวันที่ไม่ถูกต้อง" แล้วถามใหม่ |
| priority ไม่ใช่ High/Medium/Low | แจ้งแล้วถามใหม่ |
| ID ไม่ใช่ตัวเลข / ไม่มีในระบบ | แจ้งข้อผิดพลาด กลับไปเมนู |
| `tasks.json` เสีย หรือมี `_type` ที่ไม่รู้จัก | เตือนแล้วเริ่มด้วยรายการว่าง / ข้ามรายการนั้น |
