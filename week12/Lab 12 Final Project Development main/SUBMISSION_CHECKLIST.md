# ✅ Submission Checklist: Week 12 Final Project & Presentation

เอกสารตรวจสอบความพร้อมก่อนส่งงานและนำเสนอผลงาน สำหรับนักศึกษาชั้นปีที่ 2  
ให้นักศึกษาตรวจสอบทุกข้อให้ครบถ้วนก่อนส่งลิงก์และขึ้นนำเสนอในชั้นเรียน

🔗 **GitHub Repository**: (ใส่ลิงก์ repository ของตัวเองก่อนส่งงาน)

---

## 🗂️ 1. รายการตรวจสอบโครงสร้าง Repository & Git

- [ ] **Git Initialization**: โฟลเดอร์โปรเจกต์มีการติดตั้ง Git และเชื่อมโยงกับ GitHub เรียบร้อย
- [ ] **Commit History**: มีประวัติการ Commit อย่างสม่ำเสมอ (ไม่ส่งงานด้วย 1 Commit รวดเดียว) แสดงให้เห็นกระบวนการพัฒนาทีละ Phase
- [ ] **Repository Visibility**: ตั้งค่า Repository เป็น Public หรือได้ทำการเพิ่มอีเมลของอาจารย์/TA เป็น Collaborator แล้ว
- [ ] **`.gitignore`**: มีไฟล์ `.gitignore` ที่กรองไฟล์แคช `__pycache__/`, `.env`, `.vscode/` ไม่ให้หลุดขึ้น GitHub
- [ ] **ไม่มี Dead Files**: ลบไฟล์ทดลองที่ไม่ได้ใช้งานออกเรียบร้อยแล้ว

---

## 💻 2. รายการตรวจสอบซอร์สโค้ด (Source Code & Functionality)

### `src/task.py`
- [ ] คลาส `Task` มีแอตทริบิวต์ `tags` (list of strings)
- [ ] เมธอด `add_tag(tag)` ตัดช่องว่างส่วนเกินและแปลงเป็นตัวพิมพ์เล็ก (Normalized) ป้องกันแท็กซ้ำ
- [ ] เมธอด `remove_tag(tag)` สามารถลบแท็กได้อย่างถูกต้อง
- [ ] คลาส `DueDateTask` สืบทอดจาก `Task`, ตรวจสอบรูปแบบวันที่ `YYYY-MM-DD`, และมีเมธอด `to_dict()` / `__str__()` ที่ถูกต้อง
- [ ] คลาส `PriorityTask` สืบทอดจาก `Task`, ตรวจสอบระดับความสำคัญ (`High`, `Medium`, `Low`), และมีเมธอด `to_dict()` / `__str__()` ที่ถูกต้อง

### `src/data_persistence.py`
- [ ] สามารถบันทึกงานลงไฟล์ `data/tasks.json` ด้วย `json.dump(..., indent=4)`
- [ ] สามารถโหลดข้อมูลจากไฟล์ JSON และแปลงกลับเป็น Object ตาม Class จริง (`Task`, `DueDateTask`, `PriorityTask`) โดยดูจากฟิลด์ `_type`
- [ ] มี `setdefault('tags', [])` เพื่อรองรับไฟล์ข้อมูลเก่าโดยไม่เกิด Error
- [ ] มี Error Handling ดักจับไฟล์เสียหาย (`json.JSONDecodeError`) หรือไฟล์ไม่พบ

### `src/task_manager.py`
- [ ] การสร้างงานใหม่ทุกประเภททำงานได้ถูกต้อง และกำหนด ID อัตโนมัติไม่ซ้ำกัน
- [ ] ฟังก์ชัน `search_tasks(keyword)` ค้นหาคำค้นหาบางส่วน (Partial match) ทั้งใน Description และ Tags แบบไม่สนตัวพิมพ์เล็ก-ใหญ่
- [ ] ฟังก์ชัน `filter_tasks(...)` กรองข้อมูลได้ถูกต้อง ทั้งแบบเงื่อนไขเดียวและรวมหลายเงื่อนไข (Status, Due Date Before/After, Priority, Tags)
- [ ] ฟังก์ชัน `sort_tasks(...)` รองรับการจัดเรียงตาม ID, Description, Completed, Due Date (ผลักงานที่ไม่มีวันส่งไปท้ายสุด) และ Priority (High -> Medium -> Low)
- [ ] รองรับทั้ง Ascending และ Descending (`reverse=True`)

### `src/cli_interface.py` & `main.py`
- [ ] เมนูแสดงตัวเลือกครบถ้วน 0-9 
- [ ] มีการตรวจสอบ Input ของผู้ใช้ (เช่น วันที่ต้องเป็น YYYY-MM-DD, Priority ต้องเป็น High/Medium/Low, ID ต้องเป็นตัวเลข)
- [ ] โปรแกรมไม่ Crash เมื่อผู้ใช้กรอกข้อมูลผิดรูปแบบ
- [ ] `main.py` สามารถรันได้ด้วยคำสั่ง `python main.py` โดยไม่มี Error

---

## 🧪 3. รายการตรวจสอบการทดสอบระบบ (Testing & Quality)

- [ ] รันชุดทดสอบอัตโนมัติผ่านครบทุกเคส (OK) ด้วยคำสั่ง:
  ```bash
  python -m unittest discover tests
  ```
- [ ] โค้ดทั้งหมดเขียนถูกต้องตามมาตรฐาน PEP 8 (เว้นวรรค, การตั้งชื่อตัวแปรและฟังก์ชัน)
- [ ] มี Docstrings อธิบายคลาสและเมธอดสำคัญครบถ้วน

---

## 📄 4. รายการตรวจสอบเอกสารประกอบ (Documentation)

- [ ] **`README.md`**:
  - [ ] ใส่ชื่อ-นามสกุล และรหัสนักศึกษาครบถ้วน
  - [ ] ตรวจสอบคำอธิบายสถาปัตยกรรมและขั้นตอนการรันโปรแกรม
- [ ] **`PLAN.md`**:
  - [ ] มีการบันทึกปัญหาทางเทคนิคที่พบ (Technical Challenges) และวิธีแก้ไข
  - [ ] มีการบันทึกสิ่งที่ได้เรียนรู้ (Lessons Learned) และแนวทางพัฒนาต่อยอด (Future Work)
- [ ] **`data/tasks.json`**:
  - [ ] มีข้อมูลงานตัวอย่างอย่างน้อย 5-6 รายการ ครบทุกประเภทและมี Tags พร้อมสำหรับการสาธิต (Demo)

---

## 🎤 5. รายการตรวจสอบการนำเสนอผลงาน (Presentation Readiness)

- [ ] **สไลด์การนำเสนอ**: เตรียมสไลด์ครบทั้ง 7 ส่วน:
  1. Introduction (แนะนำตัว & วัตถุประสงค์)
  2. Problem Solved (ปัญหาที่โปรแกรมแก้ไข)
  3. Live Demo (การสาธิตการทำงานจริง)
  4. Software Architecture (อธิบายโครงสร้าง OOP & Separation of Concerns)
  5. Technical Challenges & Solutions (ปัญหาที่พบ เช่น Polymorphic Sort และวิธีแก้)
  6. Lessons Learned (บทเรียนที่ได้จากการทำโปรเจกต์)
  7. Future Work & Q&A (แผนการพัฒนาต่อยอด)
- [ ] **Live Demo Script**: ซ้อมลำดับขั้นตอนการกดเมนูใน Terminal ให้คล่องแคล่ว
- [ ] **Time Management**: ควบคุมเวลาการนำเสนอให้อยู่ภายใน 5 - 7 นาที
- [ ] **Backup Plan**: มีแผนสำรองกรณีโปรแกรมติดขัดระหว่าง Demo (เช่น เตรียมภาพจับหน้าจอ หรือไฟล์บันทึกสำรอง)
