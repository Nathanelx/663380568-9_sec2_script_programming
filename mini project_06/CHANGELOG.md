# CHANGELOG — ระบบยืมหนังสือ (Library Borrowing System)

> เขียนด้วยคำของตัวเอง — ไม่ copy จาก AI โดยตรง

---

## v2.0.0 — File I/O + Auto-increment ID

### เพิ่มใหม่ (Added)

#### 1. ระบบบันทึกและโหลดข้อมูล (Data Persistence)
```python
DATA_FILE = "library_data.json"

save_data()   # บันทึก books, members, borrow_log, IDs → JSON
load_data()   # โหลดกลับมาเมื่อเปิดโปรแกรมใหม่
```
**ทำไมถึงเพิ่ม**: v1.0 ข้อมูลหายทุกครั้งที่ปิดโปรแกรม — ไม่ใช้งานได้จริง

**สิ่งที่เรียนรู้**:
- `json.dump(data, f, ensure_ascii=False, indent=4)` — บันทึก dict/list เป็น JSON อ่านได้
- `json.load(f)` — โหลด JSON กลับเป็น dict/list ได้เลย ไม่ต้องแปลงเอง
- `os.path.exists(filename)` — ตรวจก่อนเปิดไฟล์ ป้องกัน FileNotFoundError
- `data.get("books", {})` — ถ้า key ไม่มีใน JSON คืน default แทน crash

#### 2. Auto-increment ID
```python
_book_id   = 0   # นับลำดับหนังสือ
_member_id = 0   # นับลำดับสมาชิก
```
- ISBN สร้างอัตโนมัติ: `f"ISBN{_book_id:03d}"` → ISBN001, ISBN002, ...
- Member ID อัตโนมัติ: `f"M{_member_id:03d}"` → M001, M002, ...

**สิ่งที่เรียนรู้**:
- `:03d` ใน f-string = จำนวนเต็ม จอง 3 หลัก เติม 0 นำหน้า
- `global _book_id` ใน _ui_add_book() — ต้องประกาศ global เพื่อแก้ค่านอก function

#### 3. ปรับ main_menu()
```python
def main_menu():
    load_data()   # โหลดข้อมูลทันทีที่เปิดโปรแกรม
    ...
    if choice == "0":
        save_data()   # บันทึกก่อนออก
        break
```

#### 4. ลบ seed_data()
เพราะตอนนี้โหลดจาก `library_data.json` แทน — ไม่ต้องใส่ข้อมูลจำลองอีกต่อไป

---

### เปลี่ยนแปลง (Changed)

| ฟังก์ชัน | v1.0 | v2.0 |
|---|---|---|
| `_ui_add_book()` | รับ ISBN จากผู้ใช้ | สร้าง ISBN อัตโนมัติ |
| `_ui_register()` | รับ member_id จากผู้ใช้ | สร้าง M_ID อัตโนมัติ |
| `main_menu()` | แค่วน loop | เรียก load_data() ต้น + save_data() ก่อนออก |

### ลบออก (Removed)

- `seed_data()` — ไม่ต้องการแล้ว เพราะมี load_data() แทน

---

### สิ่งที่เรียนรู้จาก v2.0

**File I/O Pattern**
```
เปิดโปรแกรม → load_data() → ใช้งาน → save_data() → ปิดโปรแกรม
```
Pattern นี้เหมือนทุก app จริง — SQLite, mobile app, game save file ทำแบบเดียวกัน

**ทำไม save ตอนออกเท่านั้น ไม่ save ทุก action?**
ถ้า save ทุก action = เขียนไฟล์บ่อยมาก ช้า และเสี่ยงไฟล์เสียถ้า crash กลางทาง
→ ในระบบจริงจะใช้ database transaction แทน แต่สำหรับโปรเจกต์นี้ save ตอนออกพอ

**global variable กับ counter**
`global _book_id` ไม่ ideal แต่เหมาะกับ procedural style ของโปรเจกต์นี้
→ ถ้า refactor เป็น OOP จะกลายเป็น `self._book_id` แทน ไม่ต้องใช้ global

---

## v1.0.1 — Bug Fix

- แก้ `return_book()`: เพิ่มตรวจ `isbn in borrowed_books` ก่อน `.remove()`
- แก้ overdue check ใช้ `date.fromisoformat()` แทน string compare

## v1.0.0 — Initial Release

### เพิ่มใหม่
- `add_book()`, `list_books()`, `search_book()`
- `register_member()`, `list_members()`
- `borrow_book()` — 4-layer validation
- `return_book()` — next() + generator + overdue fine
- `my_loans()`, `view_report()`
- `main_menu()` — dispatcher dict pattern
- `seed_data()` — ข้อมูลจำลอง 5 หนังสือ 3 สมาชิก

### สิ่งที่เรียนรู้
- dict ซ้อน dict = pattern เดียวกับ JSON API
- borrow_log append-only = audit trail
- validate ก่อน mutate เสมอ
- next(generator, None) หา item แรก — Pythonic กว่า for+break
- UI แยกจาก core → core test ง่าย
