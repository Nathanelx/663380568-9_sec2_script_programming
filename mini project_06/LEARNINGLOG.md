# LEARNINGLOG — ระบบยืมหนังสือ

## Prompt Log — v1.0

---

### #001

| | |
|---|---|
| **TOPIC** | Data Design — ทำไมใช้ dict แทน list |
| **PROMPT** | "ในระบบยืมหนังสือ ควรเก็บข้อมูลหนังสือเป็น list หรือ dict? อธิบายเหตุผลพร้อมตัวอย่างโค้ด" |
| **AI_SAID** | Dict เหมาะกว่าเพราะค้นหาด้วย ISBN ได้ทันที O(1) ไม่ต้อง loop ทั้งรายการ ต่างจาก list ที่ต้อง iterate O(n) ทุกครั้ง |
| **I_LEARNED** | เข้าใจว่า dict คือ "index ที่เราออกแบบเอง" — เหมือนสมุดโทรศัพท์ที่เปิดหาชื่อได้ทันทีโดยไม่ต้องพลิกทุกหน้า ส่วน list เหมือนอ่านทีละบรรทัดจนเจอ |
| **STILL_CONFUSED** | dict กับ list ต่างกันเรื่อง memory ใช้แค่ไหน? ถ้าข้อมูลน้อยๆ (< 100 items) ความเร็วต่างกันมากไหม? |

---

### #002

| | |
|---|---|
| **TOPIC** | Validation — ลำดับการตรวจสอบใน borrow_book() |
| **PROMPT** | "ทำไมต้อง validate ก่อน mutate data? ถ้า validate หลังจะเกิดอะไรขึ้น? ยกตัวอย่างกรณีที่ data เสียหาย" |
| **AI_SAID** | ถ้า validate หลัง และ error เกิดตรงกลาง data บางส่วนถูกแก้แล้ว บางส่วนยังไม่ถูกแก้ ทำให้ระบบอยู่ในสถานะกึ่งกลางที่ไม่สอดคล้องกัน เช่น available ลดแล้วแต่ log ยังไม่ถูกสร้าง |
| **I_LEARNED** | นึกภาพได้ว่าถ้า ATM หักเงินออกจากบัญชีแล้วแต่เครื่องดับก่อนจ่ายเงิน — นั่นคือ partial mutation ที่เลวร้าย validate ก่อน = ตรวจหมดก่อน ถ้าผ่านทั้งหมดค่อยแตะ data |
| **STILL_CONFUSED** | Database ใช้วิธีอะไรแก้ปัญหานี้? เคยได้ยินคำว่า "transaction" แต่ใน Python ทำได้ไหม? |

---

### #003

| | |
|---|---|
| **TOPIC** | `next()` + generator expression |
| **PROMPT** | "อธิบาย next(generator, None) ใน return_book() ให้เข้าใจ เทียบกับการเขียน for loop แบบธรรมดา" |
| **AI_SAID** | `next()` ดึงค่าแรกจาก iterator แล้วหยุดทันที ไม่ต้อง loop ต่อ ส่วน None คือ default ถ้าหาไม่เจอ ประหยัดกว่า for loop ที่ต้อง iterate จนจบ |
| **I_LEARNED** | ก่อนหน้านี้เขียน for loop + flag variable แต่ตอนนี้เข้าใจว่า `next()` ทำสิ่งเดียวกันใน 1 บรรทัด ประหยัดทั้งโค้ดและ CPU เพราะหยุดทันทีที่เจอ |
| **STILL_CONFUSED** | ถ้า borrow_log ใหญ่มากๆ (เช่น 1 ล้าน entries) next() เร็วกว่า for loop มากแค่ไหน? |

---

### #004

| | |
|---|---|
| **TOPIC** | Testing — ทำไม test ที่ "คาดว่า error" สำคัญ |
| **PROMPT** | "ใน run_test() มี expect_pass=False หมายความว่าอะไร ทำไมต้อง test กรณีที่โปรแกรมควร error?" |
| **AI_SAID** | Test ที่คาดว่า error ตรวจสอบว่า guard clauses ทำงาน ถ้า borrow_book ไม่ raise error เมื่อ ISBN ไม่มี แสดงว่า validation พัง ซึ่งอันตรายกว่า bug ที่ crash |
| **I_LEARNED** | เหมือนทดสอบกุญแจประตู ต้องทดสอบว่า "ล็อคอยู่จริงไหม" ไม่ใช่แค่ "เปิดได้ไหม" bug ที่อันตรายที่สุดคือ validation ที่หายไปเงียบๆ ไม่มีใครรู้ |
| **STILL_CONFUSED** | มีวิธีอัตโนมัติตรวจว่า test ครอบคลุม code กี่เปอร์เซ็นต์? เคยได้ยิน "code coverage" |

---

### #005

| | |
|---|---|
| **TOPIC** | Append-only log pattern |
| **PROMPT** | "ทำไม borrow_log ถึงเป็น append-only? ทำไมไม่ลบ row เมื่อคืนหนังสือ? มี real-world analogy ไหม?" |
| **AI_SAID** | Append-only logs เป็น pattern ที่ใช้ใน banking, version control, และ blockchain เพราะประวัติที่เปลี่ยนไม่ได้ (immutable history) สร้างความน่าเชื่อถือและตรวจสอบได้ (audit trail) |
| **I_LEARNED** | Git ก็เป็น append-only — commit ไม่เคยหายถ้าไม่ force push ธนาคารก็ไม่ลบ transaction เก่าออก แค่เพิ่ม "reversal transaction" ใหม่ โค้ดของเราทำแบบเดียวกันโดยไม่รู้ตัว |
| **STILL_CONFUSED** | ถ้า borrow_log ใหญ่มาก (ล้าน entries) การ search ด้วย next() จะช้าไหม? ควรทำ index แยกไหม? |

---

## Prompt Log — v2.0

---

### #006

| | |
|---|---|
| **TOPIC** | File I/O — บันทึกข้อมูลลงไฟล์ JSON |
| **PROMPT** | "ระบบยืมหนังสือที่ทำไว้ข้อมูลหายทุกครั้งที่ปิดโปรแกรม จะแก้ยังไงให้ข้อมูลอยู่ถาวร?" |
| **AI_SAID** | ใช้ `json` module: `json.dump()` บันทึก dict/list เป็น JSON file, `json.load()` โหลดกลับมา เรียก load ตอนเปิดโปรแกรม save ตอนปิด |
| **I_LEARNED** | JSON คือ dict/list ที่แปลงเป็น text เก็บในไฟล์ได้ เหมือนถ่ายรูป dict แล้วเก็บไว้ เปิดโปรแกรมครั้งหน้าก็โหลดรูปนั้นกลับมา เป็น pattern เดียวกับที่ทุก app ใช้ |
| **STILL_CONFUSED** | ถ้าโปรแกรม crash ระหว่างใช้งาน (ยังไม่ได้ save) ข้อมูลหายไหม? ระบบจริงแก้ยังไง? |

---

### #007

| | |
|---|---|
| **TOPIC** | `os.path.exists()` — ทำไมต้องตรวจก่อน load |
| **PROMPT** | "ทำไม load_data() ต้องตรวจ os.path.exists() ก่อน? ถ้าไม่ตรวจจะเกิดอะไร?" |
| **AI_SAID** | ถ้าไม่ตรวจและไฟล์ยังไม่มี (เช่น รันครั้งแรก) จะเกิด FileNotFoundError crash ทันที os.path.exists() คืน True/False ให้ตัดสินใจก่อนเปิดไฟล์ |
| **I_LEARNED** | เหมือนเช็คว่ามีจดหมายในกล่องก่อนเปิด ถ้าเปิดกล่องเปล่าโดยไม่เช็ค = error การ defensive programming คือคิดถึงกรณีที่สิ่งที่คาดหวังอาจไม่มีอยู่ |
| **STILL_CONFUSED** | `with open(file) as f` ต่างจาก `f = open(file)` ยังไง? ทำไม with ดีกว่า? |

---

### #008

| | |
|---|---|
| **TOPIC** | Auto-increment ID — f-string format `:03d` |
| **PROMPT** | "f'ISBN{_book_id:03d}' หมายความว่าอะไร ทำไมต้องมี :03d?" |
| **AI_SAID** | `:03d` คือ format spec: `0` = เติม 0 นำหน้า, `3` = จอง 3 หลัก, `d` = integer เลข 1 จะได้ "001" ไม่ใช่ "1" |
| **I_LEARNED** | เหมือนการนับเลขในร้านอาหาร ป้าย "001" ดูเป็นระเบียบกว่า "1" และ sort ตามลำดับได้ถูกต้อง ถ้าใช้ "1" "2" ... "10" จะ sort ผิดเป็น "1","10","2" |
| **STILL_CONFUSED** | format spec อื่นมีอะไรอีก? เช่น `:>10` `:.2f` ใช้เมื่อไหร่? |

---

### #009

| | |
|---|---|
| **TOPIC** | global keyword — ทำไม _ui_add_book() ต้องประกาศ global |
| **PROMPT** | "ทำไม _ui_add_book() ต้องเขียน global _book_id ถ้าไม่เขียนจะเกิดอะไร?" |
| **AI_SAID** | ถ้าไม่ประกาศ global Python จะมองว่า `_book_id += 1` เป็นการสร้างตัวแปร local ใหม่ ทำให้เกิด UnboundLocalError เพราะ local ยังไม่มีค่า |
| **I_LEARNED** | Python rule: ถ้าเห็น `=` ใน function ถือเป็น local เสมอ ต้องบอก Python ชัดๆ ว่า "ตัวนี้ global นะ" ถ้าไม่บอก มันคิดเองว่าสร้างใหม่ |
| **STILL_CONFUSED** | ถ้า refactor เป็น OOP `self._book_id` จะไม่ต้องใช้ global แล้วใช่ไหม? ทำไม self ถึงต่างจาก global? |

---

### #010

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

| # | Insight | Prompt |
|---|---|---|
| 1 | `dict` O(1) vs `list` O(n) — ค้นหาต่างกันมาก | #001 |
| 2 | Validate before mutate — ป้องกัน partial corruption | #002 |
| 3 | `next(gen, None)` ดีกว่า for+flag | #003 |
| 4 | Test error cases สำคัญเท่า test happy path | #004 |
| 5 | Append-only log = audit trail เหมือน bank statement | #005 |

### v2.0 Concepts (Prompt #006–010)

| # | Insight | Prompt |
|---|---|---|
| 6 | `json.dump/load` แปลง dict/list ↔ text file ได้โดยตรง | #006 |
| 7 | `os.path.exists()` ตรวจก่อนเปิดไฟล์ — defensive programming | #007 |
| 8 | f-string `:03d` จัด format ตัวเลขให้เป็นระเบียบและ sort ถูก | #008 |
| 9 | `global` ต้องประกาศถ้าจะแก้ตัวแปรนอก function | #009 |
| 10 | Data persistence pattern: load on start → use → save on exit | #010 |

---

## Kanban Update (รวม v1.0 + v2.0)

```
✅ DONE
  v1.0:
  + dict/list data design
  + validate before mutate pattern
  + next() + generator expression
  + append-only log pattern
  + test suite — happy path + error cases
  + UI/core separation

  v2.0:
  + json module — dump/load
  + os.path.exists()
  + data persistence pattern
  + auto-increment ID + global counter
  + f-string format spec :03d

🔄 IN PROGRESS (WIP ≤ 2)
  - GitHub artifacts ครบชุด
  - เตรียมนำเสนอ 10-15 นาที

📋 BACKLOG
  - OOP refactor (class Library)
  - Pandas analytics
  - Flask web API
  - SQLite database (แทน JSON)
  - with open() pattern
  - code coverage (pytest)
```
