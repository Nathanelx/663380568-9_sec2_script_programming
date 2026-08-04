# CHANGELOG — ระบบยืมหนังสือ (Library Borrowing System)


## v1.0.0 — Initial Release

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

## v1.0.1 — Bug Fix & Testing

### แก้ไข (Fixed)
- `return_book()` — เพิ่มตรวจสอบ `isbn in members[member_id]["borrowed_books"]` ก่อน remove เพื่อป้องกัน ValueError
- `my_loans()` — แก้ overdue check ให้ใช้ `date.fromisoformat()` แทนการ compare string โดยตรง
