# LEARNINGLOG — ระบบยืมหนังสือ (Library Borrowing System)

## Prompt Log

---

### #001

| | |
|---|---|
| **TOPIC** | Data Design — ทำไมใช้ dict แทน list |
| **PROMPT** | "ในระบบยืมหนังสือ ควรเก็บข้อมูลหนังสือเป็น list หรือ dict? อธิบายเหตุผลพร้อมตัวอย่างโค้ด" |
| **AI_SAID** | Dict เหมาะกว่าเพราะค้นหาด้วย ISBN ได้ทันที O(1) ไม่ต้อง loop ทั้งรายการ ต่างจาก list ที่ต้อง iterate O(n) ทุกครั้ง |
| **I_LEARNED** | เข้าใจครั้งแรกว่า "dict คือ index ที่เราออกแบบเอง" — เหมือนสมุดโทรศัพท์ที่เปิดหาชื่อได้ทันทีโดยไม่ต้องพลิกทุกหน้า ส่วน list เหมือนอ่านทีละบรรทัดจนเจอ |
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
| **PROMPT** | "อธิบาย next(generator, None) ใน return_book() ให้ฉันเข้าใจ เทียบกับการเขียน for loop แบบธรรมดา" |
| **AI_SAID** | `next()` ดึงค่าแรกจาก iterator แล้วหยุดทันที ไม่ต้อง loop ต่อ ส่วน None คือ default ถ้าหาไม่เจอ ประหยัดกว่า for loop ที่ต้อง iterate จนจบ |
| **I_LEARNED** | ก่อนหน้านี้เขียน for loop + flag variable แต่ตอนนี้เข้าใจว่า `next()` ทำสิ่งเดียวกันใน 1 บรรทัด — ประหยัดทั้งโค้ดและ CPU เพราะหยุดทันทีที่เจอ |
| **STILL_CONFUSED** | ถ้า list ใหญ่มากๆ (เช่น 1 ล้าน entries) next() เร็วกว่า for loop มากแค่ไหน? |

---

### #004

| | |
|---|---|
| **TOPIC** | Testing — ทำไม test ที่ "คาดว่า error" สำคัญ |
| **PROMPT** | "ใน run_test() มี expect_pass=False หมายความว่าอะไร ทำไมต้อง test กรณีที่โปรแกรมควร error?" |
| **AI_SAID** | Test ที่คาดว่า error ตรวจสอบว่า guard clauses ทำงาน — ถ้า borrow_book ไม่ raise error เมื่อ ISBN ไม่มี แสดงว่า validation พัง ซึ่งอันตรายกว่า bug ที่ crash |
| **I_LEARNED** | เหมือนทดสอบกุญแจประตู — ต้องทดสอบว่า "ล็อคอยู่จริงไหม" ไม่ใช่แค่ "เปิดได้ไหม" bug ที่อันตรายที่สุดคือ validation ที่หายไปเงียบๆ ไม่มีใครรู้ |
| **STILL_CONFUSED** | มีวิธีอัตโนมัติตรวจว่า test ครอบคลุม code กี่เปอร์เซ็นต์? เคยได้ยิน "code coverage" |

---

### #005

| | |
|---|---|
| **TOPIC** | append-only log pattern |
| **PROMPT** | "ทำไม borrow_log ถึงเป็น append-only? ทำไมไม่ลบ row เมื่อคืนหนังสือ? มี real-world analogy ไหม?" |
| **AI_SAID** | Append-only logs เป็น pattern ที่ใช้ใน banking, version control, และ blockchain เพราะประวัติที่เปลี่ยนไม่ได้ (immutable history) สร้างความน่าเชื่อถือและตรวจสอบได้ (audit trail) |
| **I_LEARNED** | Git ก็เป็น append-only — commit ไม่เคยหายถ้าไม่ force push ธนาคารก็ไม่ลบ transaction เก่าออก แค่เพิ่ม "reversal transaction" ใหม่ — โค้ดของเราทำแบบเดียวกันโดยไม่รู้ตัว |
| **STILL_CONFUSED** | ถ้า borrow_log ใหญ่มาก (ล้าน entries) การ search ด้วย next() จะช้าไหม? ควรทำ index แยกไหม? |

---

## สรุปสิ่งที่กลุ่มเรียนรู้ตลอดโปรเจกต์

### Technical Insights (เรียนรู้จาก AI + ลงมือทำ)

| # | Insight | เรียนรู้จาก |
|---|---|---|
| 1 | `dict` O(1) vs `list` O(n) — ค้นหาต่างกันมาก | Prompt #001 |
| 2 | Validate before mutate — ป้องกัน partial state | Prompt #002 |
| 3 | `next(gen, None)` ดีกว่า for + flag | Prompt #003 |
| 4 | Test error cases สำคัญเท่า test happy path | Prompt #004 |
| 5 | Append-only log = audit trail pattern | Prompt #005 |

## Kanban Update (สุดท้าย)

```
✅ DONE
  • dict/list/set fundamentals
  • functions + docstring + type hints
  • try/except/raise
  • next() + generator expression  
  • dispatcher dict pattern (main_menu)
  • validate-before-mutate pattern
  • append-only log pattern
  • test suite (happy + edge + error cases)

🔄 IN PROGRESS (WIP = 2)
  • file I/O — save/load JSON
  • OOP refactor planning

📋 TODO
  • json module (Week 7)
  • class/object (Week 8+)
  • Flask web API (later)
  • pandas analytics (later)
```
