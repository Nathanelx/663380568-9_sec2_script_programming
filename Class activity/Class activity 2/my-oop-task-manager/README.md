# Class Activity 2: OOP Task Manager CLI

Week 8: **Object-Oriented Programming (OOP) Fundamentals & Refactoring the CLI Task Manager**

นำ Task Manager จาก Class Activity 1 (แบบ procedural: ใช้ dict + ฟังก์ชัน) มา **refactor เป็น OOP**
โดยแยกเป็นคลาส `Task` (ข้อมูลงาน 1 รายการ) และ `TaskManager` (จัดการรายการงานและการบันทึกไฟล์)

## 🧱 OOP Design

```text
main.py (CLI เมนู)
   │  manager = TaskManager()
   ▼
TaskManager                         Task
├─ tasks: list[Task]   ───────────► ├─ id, description, completed
├─ next_id: int                     ├─ mark_complete()
├─ add_task(description)            ├─ to_dict()      → dict สำหรับบันทึก JSON
├─ list_tasks()                     ├─ __str__()      → "ID: 1 | Description: ... | Status: Pending"
├─ complete_task(task_id)           └─ __repr__()     → "Task(id=1, description='...', completed=False)"
├─ delete_task(task_id)
├─ _load_tasks()   JSON → Task objects
└─ _save_tasks()   Task objects → JSON (data/tasks.json)
```

| แนวคิด OOP | ในโปรเจกต์นี้ |
| --- | --- |
| **Class** (แม่แบบ) | `Task`, `TaskManager` |
| **Object / Instance** | `Task(1, "งาน 1")`, `manager = TaskManager()` |
| **Attribute** | `task.id`, `task.description`, `task.completed`, `manager.tasks`, `manager.next_id` |
| **Method** | `task.mark_complete()`, `manager.add_task(...)` |
| **`__init__` / `self`** | constructor กำหนดค่า attribute ของ object ตัวนั้น ๆ |
| **Encapsulation** | การโหลด/บันทึกไฟล์ซ่อนอยู่ใน `_load_tasks()` / `_save_tasks()` (ขึ้นต้นด้วย `_` = ใช้ภายในคลาส) |
| **`__str__` / `__repr__`** | `print(task)` แสดงข้อความอ่านง่าย / `repr(task)` สำหรับดีบัก |

### เทียบกับ Class Activity 1

| Procedural (Activity 1) | OOP (Activity 2) |
| --- | --- |
| `{"id": 1, "description": "...", "completed": False}` | `Task(1, "...")` |
| `task_logic.add_task(tasks, desc)` | `manager.add_task(desc)` |
| `task["completed"] = True` | `task.mark_complete()` |
| ต้องส่ง `tasks` เข้าออกทุกฟังก์ชัน | ข้อมูลอยู่ใน `manager.tasks` |
| บันทึกไฟล์ตอนกดออก | บันทึกอัตโนมัติทุกครั้งที่ add / complete / delete |

## 📂 โครงสร้างโปรเจกต์

```text
my-oop-task-manager/
├── src/
│   ├── __init__.py         # ทำให้ src เป็น Python package
│   ├── task.py             # คลาส Task
│   └── task_manager.py     # คลาส TaskManager (logic + บันทึกไฟล์)
├── tests/
│   ├── test_task.py        # unit test คลาส Task (6 tests)
│   └── test_task_manager.py# unit test คลาส TaskManager (5 tests)
├── data/
│   └── tasks.json          # ไฟล์เก็บงาน (สร้างอัตโนมัติ)
├── main.py                 # จุดเริ่มต้นโปรแกรม (เมนู CLI)
├── .gitignore
└── README.md
```

## 🚀 วิธีรัน

ใช้แค่ built-in modules ไม่ต้องติดตั้งอะไรเพิ่ม

```powershell
cd "Class activity\Class activity 2\my-oop-task-manager"
python main.py
```

รัน unit tests:

```bash
python -m unittest discover tests
```

## ✅ ผลลัพธ์

```text
--- OOP Task Manager Menu ---
1. Add Task
2. List Tasks
3. Complete Task
4. Delete Task
5. Exit
-------------------------
Enter your choice (1-5): 3
Enter ID of task to complete: 2
Task ID 2 marked as completed.

Enter your choice (1-5): 2

--- Your Tasks ---
ID: 1 | Description: งาน 1 | Status: Pending
ID: 2 | Description: งาน 2 | Status: Completed
------------------
```

Unit tests:

```text
Ran 11 tests in 0.011s

OK
```

## 🐞 Debugging ใน VS Code (เน้น OOP)

1. วาง breakpoint ที่บรรทัด `manager = TaskManager()` ใน `main.py`
   และใน `__init__` / `_load_tasks` ของ `task_manager.py`, `__init__` / `mark_complete` ของ `task.py`
2. ไปที่ **Run and Debug** แล้วกด **Python File**
3. เมื่อหยุดที่ `manager = TaskManager()` กด **Step Into (F11)** เพื่อเข้า `TaskManager.__init__` แล้วเข้า `_load_tasks`
4. ตอนวนสร้าง `Task(...)` จาก JSON กด F11 เข้า `Task.__init__` ดูการกำหนด `self.id`, `self.description`
5. ในหน้าต่าง **Variables** กางดู `self` จะเห็นว่าแต่ละ method ทำงานกับ object ตัวไหน
6. ตอน complete งาน ให้ step เข้า `manager.complete_task()` → `task.mark_complete()` ดู `self.completed` เปลี่ยนเป็น `True`

## 🔧 Troubleshooting

| ปัญหา | วิธีแก้ |
| --- | --- |
| `ModuleNotFoundError: No module named 'task_manager'` | รันจากโฟลเดอร์ `my-oop-task-manager` ด้วย `python main.py` |
| `Warning: tasks.json is empty or corrupted` | ไฟล์ JSON เสีย โปรแกรมเริ่มด้วยรายการว่าง (ลบ `data/tasks.json` ได้) |
| `Invalid input. Please enter a number for Task ID.` | ต้องพิมพ์ ID เป็นตัวเลข |
