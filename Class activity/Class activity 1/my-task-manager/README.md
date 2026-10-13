# Class Activity 1: Simple Task Manager CLI

แอปพลิเคชันจัดการงาน (Task Manager) แบบ Command-Line สำหรับ Week 7:
**Building a Simple CLI Application, Error Handling & Project Structure**

ฝึกการแบ่งโค้ดเป็นโมดูล, จัดการข้อผิดพลาดด้วย `try-except`, บันทึกข้อมูลถาวรด้วย JSON และดีบักใน VS Code

## ✨ Features

| เมนู | ความสามารถ |
| --- | --- |
| 1. Add New Task | เพิ่มงานพร้อม priority (Low / Medium / High, ค่าเริ่มต้น Medium) ได้ ID อัตโนมัติ |
| 2. List All Tasks | แสดงงานทั้งหมดเป็นตาราง พร้อมสรุปจำนวนที่ทำเสร็จ |
| 3. List Pending Tasks | แสดงเฉพาะงานที่ยังไม่เสร็จ |
| 4. List Completed Tasks | แสดงเฉพาะงานที่เสร็จแล้ว |
| 5. Search Tasks by Keyword | ค้นหางานจากคำในคำอธิบาย (ไม่สนตัวพิมพ์เล็ก/ใหญ่) |
| 6. Mark Task as Completed | ทำเครื่องหมายว่างานเสร็จ (พิมพ์ `2` หรือ `#2` ก็ได้) |
| 7. Delete Task | ลบงาน (ถามยืนยัน y/N ก่อนลบ) |
| 8. Save and Exit | บันทึกแล้วออกจากโปรแกรม |

ข้อมูลจะถูกบันทึกลง `data/tasks.json` อัตโนมัติทุกครั้งที่เพิ่ม/แก้/ลบ และโหลดกลับมาเมื่อเปิดโปรแกรม

## 📂 โครงสร้างโปรเจกต์

```text
my-task-manager/
├── src/
│   ├── __init__.py      # ทำให้ src เป็น Python package
│   ├── task_data.py     # Data layer: load_tasks() / save_tasks() กับไฟล์ JSON
│   └── task_logic.py    # Business logic: add, list, complete, delete, search
├── data/
│   └── tasks.json       # ไฟล์เก็บงาน (สร้างอัตโนมัติ)
├── main.py              # Presentation layer: เมนู CLI และรับ input แบบปลอดภัย
├── .gitignore
└── README.md
```

โครงสร้างข้อมูลของงานแต่ละรายการ:

```python
{"id": 1, "description": "Buy groceries", "completed": False, "priority": "High"}
```

## 🚀 วิธีรัน

ใช้แค่ built-in modules ไม่ต้องติดตั้งอะไรเพิ่ม

```powershell
cd "Class activity\Class activity 1\my-task-manager"
python main.py
```

หรือเปิด `main.py` ใน VS Code แล้วกดปุ่ม ▶ Run Python File

## ✅ ตัวอย่างการใช้งาน

```text
Enter choice (1-8): 1
Enter task description: Buy groceries
Enter priority (Low / Medium / High) [Default: Medium]: high
[OK] Task 'Buy groceries' [Priority: High] added successfully with ID #1.

Enter choice (1-8): 2

ID     | Status       | Priority   | Description
-----------------------------------------------------------------
#1     | [DONE]       | High       | Buy groceries
#2     | [PENDING]    | Medium     | Finish Python lab
=================================================================
Summary: 1/2 task(s) completed.
```

## 🛡️ Error Handling

| สถานการณ์ | Exception | โปรแกรมทำอะไร |
| --- | --- | --- |
| พิมพ์ ID เป็นตัวอักษร เช่น `abc` | `ValueError` | แจ้ง `[Error] Invalid input ...` แล้วกลับไปเมนู |
| พิมพ์ ID เป็น 0 หรือติดลบ | `ValueError` (raise เอง) | แจ้งว่า ID ต้องเป็นจำนวนเต็มบวก |
| ID ที่ไม่มีอยู่ | - | แจ้ง `Task with ID #99 was not found.` |
| คำอธิบายว่าง | - | แจ้ง `Description cannot be empty.` |
| priority ไม่ถูกต้อง | - | เตือนแล้วใช้ `Medium` |
| เลือกเมนูนอก 1-8 | - | แจ้ง `Invalid choice` |
| `tasks.json` เสีย/ไม่ใช่ JSON | `json.JSONDecodeError` | เตือนแล้วเริ่มด้วยรายการว่าง (ไม่ crash) |
| ไม่มีไฟล์ / ไม่มีสิทธิ์เขียนไฟล์ | `FileNotFoundError`, `PermissionError` | แจ้ง error แทนการ crash |
| กด Ctrl+C ระหว่างใช้งาน | `KeyboardInterrupt` | บันทึกงานฉุกเฉินแล้วออกอย่างปลอดภัย |

## 🐞 Debugging ใน VS Code

1. เปิดโฟลเดอร์ `my-task-manager` ใน VS Code
2. คลิกซ้ายของเลขบรรทัดใน `main.py` ที่บรรทัด `task_id = int(raw_input)` (ในฟังก์ชัน `prompt_task_id`) เพื่อวาง **Breakpoint** (จุดแดง)
3. ไปที่แถบ **Run and Debug** แล้วกด **Python File**
4. เลือกเมนู 6 แล้วพิมพ์ `abc` โปรแกรมจะหยุดที่ breakpoint
5. ใช้ **Step Over (F10)** จะเห็นว่าโปรแกรมกระโดดไปที่ `except ValueError` ใน `main()`
6. ดูค่าตัวแปร `raw_input`, `tasks` ในหน้าต่าง **Variables** และลำดับการเรียกฟังก์ชันใน **Call Stack**

| ปุ่ม | ความหมาย |
| --- | --- |
| Continue (F5) | รันต่อจนถึง breakpoint ถัดไป |
| Step Over (F10) | ทำบรรทัดถัดไป ไม่เข้าไปในฟังก์ชัน |
| Step Into (F11) | เข้าไปในฟังก์ชันที่เรียก |
| Step Out (Shift+F11) | ออกจากฟังก์ชันปัจจุบัน |
