# TEST — ระบบยืมหนังสือ 

## T1 — Book Functions

### T1.1 add_book() ปกติ
```
Input    : isbn="ISBNTEST", title="Test Book", author="Author", qty=2
Expected : books["ISBNTEST"]["available"] == 2, books["ISBNTEST"]["total"] == 2
Result   : PASS ✅
```

### T1.2 add_book() qty=0 → ValueError
```
Input    : isbn="X", title="X", author="X", qty=0
Expected : raise ValueError
Result   : PASS ✅  ValueError: จำนวนต้องมากกว่า 0 (ได้รับ: 0)
```

### T1.3 search_book() พบผลลัพธ์
```
Input    : keyword="python"
Expected : ผลลัพธ์มีอย่างน้อย 1 รายการ
Result   : PASS ✅  พบ 2 รายการ
```

---

## T2 — Member Functions

### T2.1 register_member() ปกติ
```
Input    : member_id="M099", name="Test User", email="t@t.com"
Expected : members["M099"] มีอยู่ในระบบ
Result   : PASS ✅
```

### T2.2 register_member() ID ซ้ำ → ValueError
```
Input    : member_id="M001" (มีอยู่แล้ว)
Expected : raise ValueError
Result   : PASS ✅  ValueError: รหัสสมาชิก 'M001' มีอยู่แล้ว
```

---

## T3 — Borrow Functions

### T3.1 borrow_book() Happy Path
```
Input    : isbn="ISBN001", member_id="M001"
Expected : books["ISBN001"]["available"] ลดลง 1
           "ISBN001" อยู่ใน members["M001"]["borrowed_books"]
           borrow_log มี entry ใหม่ที่ returned_date=None
Before   : available=3
After    : available=2
Result   : PASS ✅
```

### T3.2 borrow_book() ISBN ไม่มีในระบบ → KeyError
```
Input    : isbn="XXXXX", member_id="M001"
Expected : raise KeyError
Result   : PASS ✅  KeyError: ไม่พบหนังสือ ISBN: XXXXX
```

### T3.3 borrow_book() สมาชิกไม่มีในระบบ → KeyError
```
Input    : isbn="ISBN002", member_id="M999"
Expected : raise KeyError
Result   : PASS ✅  KeyError: ไม่พบสมาชิก ID: M999
```

### T3.4 borrow_book() ยืมซ้ำ → ValueError
```
Precondition : M001 ยืม ISBN001 อยู่แล้ว (จาก T3.1)
Input        : isbn="ISBN001", member_id="M001"
Expected     : raise ValueError
Result       : PASS ✅  ValueError: 'Alice' ยืม 'Learning Python' อยู่แล้ว
```

---

## T4 — Return Functions

### T4.1 return_book() Happy Path
```
Precondition : M001 ยืม ISBN001 อยู่ (จาก T3.1)
Input        : isbn="ISBN001", member_id="M001"
Expected     : entry["returned_date"] ไม่เป็น None
               books["ISBN001"]["available"] เพิ่มขึ้น 1
               "ISBN001" ถูกลบจาก members["M001"]["borrowed_books"]
Before       : available=2, returned_date=None
After        : available=3, returned_date="2026-08-04"
Result       : PASS ✅
```

### T4.2 return_book() ไม่มีรายการยืมค้างอยู่ → KeyError
```
Precondition : M001 คืน ISBN001 แล้ว (จาก T4.1)
Input        : isbn="ISBN001", member_id="M001"
Expected     : raise KeyError
Result       : PASS ✅  KeyError: ไม่พบรายการยืม
```

### T4.3 return_book() ISBN ไม่มีในระบบ → KeyError
```
Input    : isbn="XXXXX", member_id="M001"
Expected : raise KeyError
Result   : PASS ✅  KeyError: ไม่พบหนังสือ ISBN: XXXXX
```

---

## T5 — Full Lifecycle (Integration Test)

**Scenario**: หนังสือมี 1 เล่ม, 2 คนต้องการยืม

```
Setup: ISBNX total=1, available=1 | สมาชิก Alice (MA) และ Bob (MB)

T5.1 Alice ยืม (available=1) → สำเร็จ
     Before: available=1
     After : available=0, Alice["borrowed_books"]=["ISBNX"]
     Result: PASS ✅

T5.2 Bob ยืม (available=0) → ValueError "ถูกยืมหมด"
     available ยังคง: 0 (ไม่เปลี่ยน)
     Result: PASS ✅

T5.3 Alice คืน → สำเร็จ
     Before: available=0, returned_date=None
     After : available=1, returned_date="2026-08-04"
     Result: PASS ✅

T5.4 Bob ยืม (available=1 อีกครั้ง) → สำเร็จ
     After : available=0, Bob["borrowed_books"]=["ISBNX"]
     Result: PASS ✅
```

---

## T6 — Overdue Fine

**Scenario**: ยืม 20 วัน, กำหนดคืน 14 วัน → เกิน 6 วัน

```
Setup:
  - borrow_date = วันนี้ - 20 วัน
  - due_date    = borrow_date + 14 วัน (6 วันที่แล้ว)

Expected:
  - overdue_days = max(0, 20 - 14) = 6 วัน
  - fine = 6 × 5 = 30 บาท
  - แสดงข้อความ "[!] เกินกำหนด 6 วัน -- ค่าปรับ 30 บาท"

Result: PASS ✅
```

---

## T7 — File I/O (v2.0)

### T7.1 save_data() สร้างไฟล์ได้
```
Input    : save_data("test_library_data.json")
Expected : os.path.exists("test_library_data.json") == True
Result   : PASS ✅
```

### T7.2 ไฟล์มี keys ครบ
```
Expected : JSON file มี keys: books, members, borrow_log, _log_id, _book_id, _member_id
Result   : PASS ✅  พบครบทั้ง 6 keys
```

### T7.3 load_data() โหลดข้อมูลกลับมาครบ
```
ขั้นตอน : clear data → load_data() → ตรวจสอบ
Expected : load_data() คืน True
           "ISBN001" อยู่ใน books
           "M001" อยู่ใน members
           borrow_log มี 1 entry
Result   : PASS ✅
```

---

## T8 — Auto-increment ID (v2.0)

### T8.1 ISBN format ถูกต้อง
```
Input    : _book_id = 0 → 1 → 2
Expected : f"ISBN{1:03d}" = "ISBN001"
           f"ISBN{2:03d}" = "ISBN002"
Result   : PASS ✅
```

### T8.2 Member ID format ถูกต้อง
```
Input    : _member_id = 0 → 1 → 2
Expected : f"M{1:03d}" = "M001"
           f"M{2:03d}" = "M002"
Result   : PASS ✅
```

---

## Edge Cases ที่ค้นพบระหว่างทดสอบ

### Issue #1 — remove() ใน borrowed_books
**พบเมื่อ**: return_book() ถูกเรียกซ้ำสองครั้ง  
**อาการ**: `ValueError: list.remove(x): x not in list`  
**แก้**: เพิ่ม `if isbn in member["borrowed_books"]:` ก่อน `.remove()`  
**สถานะ**: Fixed ✅

### Issue #2 — load_data() รันครั้งแรก
**พบเมื่อ**: ยังไม่มีไฟล์ `library_data.json`  
**อาการ**: FileNotFoundError ถ้าไม่มี `os.path.exists()` guard  
**แก้**: `if not os.path.exists(filename): return False`  
**สถานะ**: Fixed ✅

### Issue #3 — _book_id ไม่ถูก reset หลัง load
**พบเมื่อ**: โหลดข้อมูลแล้ว _book_id กลับเป็น 0  
**แก้**: `load_data()` โหลด `_book_id` และ `_member_id` จาก JSON ด้วย  
**สถานะ**: Fixed ✅


