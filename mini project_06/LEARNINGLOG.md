# LEARNINGLOG — ระบบยืมหนังสือ v2.0

> บันทึก AI Prompts + ความเข้าใจของตัวเอง  
> System Prompt: *"As a Python novice, please respond with AI ethics, explainable AI, and responsible AI in mind."*

---

## Prompt Log

---

### [2026-08-04] #006 — v2.0 อัปเกรด

| | |
|---|---|
| **TOPIC** | File I/O — บันทึกข้อมูลลงไฟล์ JSON |
| **PROMPT** | "ระบบยืมหนังสือที่ทำไว้ข้อมูลหายทุกครั้งที่ปิดโปรแกรม จะแก้ยังไงให้ข้อมูลอยู่ถาวร?" |
| **AI_SAID** | ใช้ `json` module: `json.dump()` บันทึก dict/list เป็น JSON file, `json.load()` โหลดกลับมา เรียก load ตอนเปิดโปรแกรม save ตอนปิด |
| **I_LEARNED** | JSON คือ dict/list ที่แปลงเป็น text เก็บในไฟล์ได้ — เหมือนถ่ายรูป dict แล้วเก็บไว้ เปิดโปรแกรมครั้งหน้าก็โหลดรูปนั้นกลับมา เป็น pattern เดียวกับที่ทุก app ใช้ |
| **STILL_CONFUSED** | ถ้าโปรแกรม crash ระหว่างใช้งาน (ยังไม่ได้ save) ข้อมูลหายไหม? ระบบจริงแก้ยังไง? |

---

### [2026-08-04] #007

| | |
|---|---|
| **TOPIC** | `os.path.exists()` — ทำไมต้องตรวจก่อน load |
| **PROMPT** | "ทำไม load_data() ต้องตรวจ os.path.exists() ก่อน? ถ้าไม่ตรวจจะเกิดอะไร?" |
| **AI_SAID** | ถ้าไม่ตรวจและไฟล์ยังไม่มี (เช่น รันครั้งแรก) จะเกิด FileNotFoundError crash ทันที os.path.exists() คืน True/False ให้ตัดสินใจก่อนเปิดไฟล์ |
| **I_LEARNED** | เหมือนเช็คว่ามีจดหมายในกล่องก่อนเปิด ถ้าเปิดกล่องเปล่าโดยไม่เช็ค = error การ defensive programming คือคิดถึงกรณีที่สิ่งที่คาดหวังอาจไม่มีอยู่ |
| **STILL_CONFUSED** | `with open(file) as f` ต่างจาก `f = open(file)` ยังไง? ทำไม with ดีกว่า? |

---

### [2026-08-04] #008

| | |
|---|---|
| **TOPIC** | Auto-increment ID — f-string format `:03d` |
| **PROMPT** | "f'ISBN{_book_id:03d}' หมายความว่าอะไร ทำไมต้องมี :03d?" |
| **AI_SAID** | `:03d` คือ format spec: `0` = เติม 0 นำหน้า, `3` = จอง 3 หลัก, `d` = integer เลข 1 จะได้ "001" ไม่ใช่ "1" |
| **I_LEARNED** | เหมือนการนับเลขในร้านอาหาร — ป้าย "001" ดูเป็นระเบียบกว่า "1" และ sort ตามลำดับได้ถูกต้อง ถ้าใช้ "1" "2" ... "10" จะ sort ผิดเป็น "1","10","2" |
| **STILL_CONFUSED** | format spec อื่นมีอะไรอีก? เช่น `:>10` `:.2f` ใช้เมื่อไหร่? |

---

### [2026-08-04] #009

| | |
|---|---|
| **TOPIC** | global keyword — ทำไม _ui_add_book() ต้องประกาศ global |
| **PROMPT** | "ทำไม _ui_add_book() ต้องเขียน global _book_id ถ้าไม่เขียนจะเกิดอะไร?" |
| **AI_SAID** | ถ้าไม่ประกาศ global Python จะมองว่า `_book_id += 1` เป็นการสร้างตัวแปร local ใหม่ ทำให้เกิด UnboundLocalError เพราะ local ยังไม่มีค่า |
| **I_LEARNED** | Python rule: ถ้าเห็น `=` ใน function → ถือเป็น local เสมอ ต้องบอก Python ชัดๆ ว่า "ตัวนี้ global นะ" ถ้าไม่บอก มันคิดเองว่าสร้างใหม่ |
| **STILL_CONFUSED** | ถ้า refactor เป็น OOP `self._book_id` จะไม่ต้องใช้ global แล้วใช่ไหม? ทำไม self ถึงต่างจาก global? |

---

### [2026-08-04] #010

| | |
|---|---|
| **TOPIC** | สรุป architecture เปลี่ยนจาก v1.0 → v2.0 |
| **PROMPT** | "สรุปให้หน่อยว่า v1.0 กับ v2.0 ต่างกันยังไง และ pattern ที่เพิ่มเข้ามาเรียกว่าอะไร?" |
| **AI_SAID** | v1.0 = in-memory only (ข้อมูลหาย), v2.0 = persistent storage ด้วย JSON pattern เรียกว่า "data persistence" — load on start, save on exit เป็น pattern พื้นฐานของทุก application |
| **I_LEARNED** | ทุก app ที่ใช้งานจริงมี persistence — Line เก็บ chat, Google Keep เก็บ notes, game เก็บ save file ทั้งหมดใช้ pattern เดียวกันนี้ แค่ v1.0 ของเราลืมทำส่วนนี้ |
| **STILL_CONFUSED** | Database (SQLite, MySQL) ต่างจาก JSON file ยังไง? ควรใช้อันไหนเมื่อไหร่? |

---

## สรุปรวม — สิ่งที่เรียนรู้ทั้งหมด

### v1.0 Concepts (Prompt #001–005)

| # | Insight |
|---|---|
| 1 | `dict` O(1) vs `list` O(n) — ค้นหาต่างกันมาก |
| 2 | Validate before mutate — ป้องกัน partial corruption |
| 3 | `next(gen, None)` ดีกว่า for+flag |
| 4 | Test error cases สำคัญเท่า test happy path |
| 5 | Append-only log = audit trail |

### v2.0 Concepts ใหม่ (Prompt #006–010)

| # | Insight |
|---|---|
| 6 | `json.dump/load` แปลง dict/list ↔ text file ได้โดยตรง |
| 7 | `os.path.exists()` ตรวจก่อนเปิดไฟล์ — defensive programming |
| 8 | f-string `:03d` จัด format ตัวเลขให้เป็นระเบียบ |
| 9 | `global` ต้องประกาศถ้าจะแก้ตัวแปรนอก function |
| 10 | Data persistence pattern: load on start → use → save on exit |

### คำถามที่ยังไม่มีคำตอบ → Backlog

- JSON vs SQLite vs Database — ใช้เมื่อไหร่?
- `with open()` vs `f = open()` — ทำไม with ดีกว่า?
- OOP: `self._book_id` แก้ปัญหา global ได้จริงไหม?
- Transaction: ป้องกัน data loss ตอน crash ยังไง?
- format spec อื่น: `:<10`, `:>10`, `:.2f` ใช้เมื่อไหร่?

---

## Kanban Update (v2.0)

```
✅ DONE (เพิ่มจาก v2.0)
  + json module — dump/load
  + os.path.exists()
  + Data persistence pattern
  + Auto-increment ID ด้วย global counter
  + f-string format spec :03d

🔄 IN PROGRESS (WIP ≤ 2)
  - GitHub artifacts ครบชุด
  - เตรียมนำเสนอ

📋 BACKLOG
  - OOP refactor (class Library)
  - Pandas analytics
  - Flask web API
  - SQLite database (แทน JSON)
```
