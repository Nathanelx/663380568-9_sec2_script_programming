# CHANGELOG — ระบบยืมหนังสือ (Library Borrowing System)

> รูปแบบ: `[วันที่] เวอร์ชัน — หัวข้อ`  
> ทุก entry เขียนด้วยคำของตัวเอง — ไม่ copy จาก AI โดยตรง

---

## [2026-08-03] v1.0.0 — Initial Release

### เพิ่มใหม่ (Added)
- `seed_data()` — โหลดข้อมูล 5 หนังสือ + 3 สมาชิกสำหรับ demo
- `add_book()` — upsert pattern: เพิ่มใหม่หรืออัปเดตจำนวน
- `list_books()` — แสดงรายการพร้อม status ว่าง/ไม่ว่าง
- `search_book()` — list comprehension กรองด้วย keyword
- `register_member()` — ลงทะเบียนพร้อมตรวจ duplicate
- `borrow_book()` — 4-layer validation ก่อน mutate data
- `return_book()` — `next()` + generator หา active log + overdue fine
- `my_loans()` — ดูรายการที่ยืมอยู่ตอนนี้
- `view_report()` — สรุปสถิติ + top popular books
- `main_menu()` — dispatcher dict pattern → functions

### สิ่งที่เรียนรู้จากเวอร์ชันนี้

**Data Design**
- เลือก `dict` แทน `list` สำหรับ books และ members เพราะค้นหาด้วย ISBN/member_id ได้เร็ว O(1)
- `borrow_log` เป็น append-only `list` เพราะประวัติไม่ควรลบ — เหมือน bank statement
- `returned_date: None` แทนการลบ row ออก — "คืนหนังสือ" คือ update ไม่ใช่ delete

**Functions**
- Validate ก่อน mutate เสมอ — ถ้า validate ทีหลังและ error กลางทาง data จะเสียหายบางส่วน
- UI functions (`_ui_*`) แยกจาก core logic ทำให้ test core ได้โดยไม่ต้องกด input
- `next(generator, None)` ดีกว่า for loop + break เพราะอ่านง่ายและ Pythonic กว่า

**Error Handling**
- `KeyError` เหมาะกับ "ไม่พบ key" (isbn/member_id ไม่มีในระบบ)
- `ValueError` เหมาะกับ "ข้อมูลผิดกฎ" (หนังสือไม่ว่าง, ยืมซ้ำ, qty < 1)
- ทุก error message ควรบอก: เกิดอะไร + ทำไม — ไม่ใช่แค่ "Error"

### ยังสับสน / ต้องเรียนเพิ่ม → Backlog

- `global _log_id` ใน borrow_book() ยังรู้สึกไม่สะอาด — ควรใช้ closure หรือ class แทน
- ถ้าโปรแกรม crash กลาง borrow_book() หลัง `available -= 1` แต่ก่อน `log.append()` — ข้อมูล inconsistent ได้อย่างไร และแก้ยังไง? (→ ต้องเรียน transaction / atomic operation)
- `timedelta` ทำงานยังไงกับ timezone? — ถ้าระบบใช้ใน timezone อื่นจะมีปัญหาไหม?

---

## [2026-08-03] v1.0.1 — Bug Fix & Testing

### แก้ไข (Fixed)
- `return_book()` — เพิ่มตรวจสอบ `isbn in members[member_id]["borrowed_books"]` ก่อน remove เพื่อป้องกัน ValueError
- `my_loans()` — แก้ overdue check ให้ใช้ `date.fromisoformat()` แทนการ compare string โดยตรง

### ทดสอบ (Tested)
- Happy Path: borrow → return ทำงานถูกต้อง
- Edge Cases: ISBN ไม่มี, สมาชิกไม่มี, ยืมซ้ำ, หนังสือหมด
- Full Lifecycle: ยืมจนหมด → ยืมไม่ได้ → คืน → ยืมได้อีก
- Overdue: simulate วันที่ผ่านมา 20 วัน → ค่าปรับ 30 บาท ถูกต้อง

### สิ่งที่เรียนรู้จากการ test

- Test ทำให้พบ bug ที่ไม่คิดว่าจะเกิด เช่น return_book() ที่เรียกซ้ำสองครั้งไม่ควรสำเร็จ
- `expect_pass=False` ใน run_test() เป็น pattern ที่ดีสำหรับทดสอบ error cases
- การ simulate วันที่ด้วยการแก้ไข dict ใน borrow_log โดยตรง ทำได้เพราะ Python dict เป็น mutable

---

## [รอ] v1.1.0 — Persistence (File I/O)

### วางแผนจะทำ
- [ ] `save_db(filename)` — บันทึก books/members/borrow_log เป็น JSON
- [ ] `load_db(filename)` — โหลดข้อมูลจากไฟล์เมื่อเริ่มโปรแกรม
- [ ] เพิ่มเมนู `[S] Save` และ `[L] Load` ใน main_menu()
- [ ] เพิ่ม `try/except FileNotFoundError` ใน load_db()

### สาเหตุที่เลื่อนไปก่อน
- ต้องเรียน file I/O และ `json` module ก่อน (Week 7)
- ต้องคิดว่าจะ serialize `date` object อย่างไร (JSON ไม่รู้จัก datetime)

---

## [รอ] v2.0.0 — OOP Refactor

### วางแผนจะทำ
- [ ] `class Library` — encapsulate books, members, borrow_log เป็น instance variables
- [ ] `class Book` — data class พร้อม `__repr__` และ `is_available` property
- [ ] `class Member` — data class พร้อม `can_borrow` property (ตรวจ quota)

### เหตุผลที่จะ refactor
- Global variables หลายตัว (`books`, `members`, `borrow_log`) จัดการยากเมื่อโปรแกรมใหญ่ขึ้น
- OOP จะทำให้ `library.borrow("ISBN001", "M001")` อ่านง่ายกว่า `borrow_book("ISBN001", "M001")`
