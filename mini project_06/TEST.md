# TEST — ระบบยืมหนังสือ (Library Borrowing System)

**วันที่ทดสอบ**: 2026-08-03  
**สภาพแวดล้อม**: Python 3.11 | Google Colab / Jupyter Notebook  
**ผู้ทดสอบ**: [ชื่อกลุ่ม]

---

## สรุปผลการทดสอบ

| หมวด | จำนวน Test | ผ่าน | ไม่ผ่าน | อัตรา |
|---|---|---|---|---|
| Book Functions | 3 | 3 | 0 | 100% |
| Member Functions | 2 | 2 | 0 | 100% |
| Borrow Functions | 4 | 4 | 0 | 100% |
| Return Functions | 3 | 3 | 0 | 100% |
| Integration Tests | 2 | 2 | 0 | 100% |
| **รวมทั้งหมด** | **14** | **14** | **0** | **100%** |

---

## Test Cases รายละเอียด

### A. Book Functions

#### Test A1 — add_book() ปกติ
```
Input    : isbn="ISBNTEST", title="Test Book", author="Author A", qty=2
Expected : books["ISBNTEST"]["available"] == 2
Result   : PASS ✅
```

#### Test A2 — add_book() qty=0 → ValueError
```
Input    : isbn="X", title="X", author="X", qty=0
Expected : raise ValueError
Result   : PASS ✅  ValueError: จำนวนต้องมากกว่า 0 (ได้รับ: 0)
```

#### Test A3 — search_book() พบผลลัพธ์
```
Input    : keyword="python"
Expected : ผลลัพธ์มีอย่างน้อย 1 รายการ
Result   : PASS ✅  พบ 2 รายการ (Learning Python, Python Crash Course)
```

---

### B. Member Functions

#### Test B1 — register_member() ปกติ
```
Input    : member_id="M099", name="Test User", email="test@test.com"
Expected : members["M099"] มีอยู่
Result   : PASS ✅
```

#### Test B2 — register_member() ID ซ้ำ → ValueError
```
Input    : member_id="M001" (มีอยู่แล้ว), name="Dup", email="dup@test.com"
Expected : raise ValueError
Result   : PASS ✅  ValueError: รหัสสมาชิก 'M001' มีอยู่แล้ว
```

---

### C. Borrow Functions

#### Test C1 — borrow_book() Happy Path
```
Input    : isbn="ISBN001", member_id="M001"
Expected : books["ISBN001"]["available"] ลดลง 1, log entry สร้างขึ้น
Result   : PASS ✅
Before   : available=3
After    : available=2, borrow_log มี 1 entry ใหม่
```

#### Test C2 — borrow_book() ISBN ไม่มีในระบบ → KeyError
```
Input    : isbn="XXXXX", member_id="M001"
Expected : raise KeyError
Result   : PASS ✅  KeyError: ไม่พบหนังสือ ISBN: XXXXX
```

#### Test C3 — borrow_book() สมาชิกไม่มีในระบบ → KeyError
```
Input    : isbn="ISBN002", member_id="M999"
Expected : raise KeyError
Result   : PASS ✅  KeyError: ไม่พบสมาชิก ID: M999
```

#### Test C4 — borrow_book() ยืมซ้ำ → ValueError
```
Precondition : M001 ยืม ISBN001 อยู่แล้ว (จาก Test C1)
Input        : isbn="ISBN001", member_id="M001"
Expected     : raise ValueError
Result       : PASS ✅  ValueError: 'Alice Wonderland' ยืม 'Learning Python' อยู่แล้ว
```

---

### D. Return Functions

#### Test D1 — return_book() Happy Path
```
Precondition : M001 ยืม ISBN001 อยู่ (จาก Test C1)
Input        : isbn="ISBN001", member_id="M001"
Expected     : entry["returned_date"] ไม่เป็น None, available เพิ่มขึ้น 1
Result       : PASS ✅
Before       : available=2, returned_date=None
After        : available=3, returned_date="2026-08-03"
```

#### Test D2 — return_book() ไม่มีรายการยืมค้างอยู่ → KeyError
```
Precondition : M001 คืน ISBN001 แล้ว (จาก Test D1)
Input        : isbn="ISBN001", member_id="M001"
Expected     : raise KeyError
Result       : PASS ✅  KeyError: ไม่พบรายการยืม
```

#### Test D3 — return_book() ISBN ไม่มีในระบบ → KeyError
```
Input    : isbn="XXXXX", member_id="M001"
Expected : raise KeyError
Result   : PASS ✅  KeyError: ไม่พบหนังสือ ISBN: XXXXX
```

---

### E. Integration Tests

#### Test E1 — Full Lifecycle (ยืมจนหมด → ยืมไม่ได้ → คืน → ยืมได้อีก)
```
Setup    : หนังสือ ISBNX มี 1 เล่ม, สมาชิก MA และ MB

Step 1: MA ยืม ISBNX
        Expected: สำเร็จ, available=0
        Result  : PASS ✅

Step 2: MB ยืม ISBNX (available=0)
        Expected: raise ValueError "ถูกยืมหมดแล้ว"
        Result  : PASS ✅

Step 3: MA คืน ISBNX
        Expected: สำเร็จ, available=1
        Result  : PASS ✅

Step 4: MB ยืม ISBNX (available=1 อีกครั้ง)
        Expected: สำเร็จ, available=0
        Result  : PASS ✅

Overall : PASS ✅
```

#### Test E2 — Overdue Fine Calculation
```
Setup   : M002 ยืม ISBN003, แก้ borrow_date เป็น 20 วันที่แล้ว
          due_date = borrow_date + 14 วัน = 6 วันที่แล้ว

Input   : return_book("ISBN003", "M002")
Expected: overdue_days = 6, fine = 6 × 5 = 30 บาท
Result  : PASS ✅
Output  : "[!] เกินกำหนด 6 วัน -- ค่าปรับ 30 บาท"
```

---

## Edge Cases ที่ค้นพบระหว่างการทดสอบ

### Issue #1 — remove() ใน borrowed_books
**พบเมื่อ**: ทดสอบ return_book() ซ้ำสองครั้ง  
**อาการ**: ValueError: list.remove(x): x not in list  
**แก้ไข**: เพิ่ม `if isbn in member["borrowed_books"]:` ก่อน `.remove()`  
**สถานะ**: Fixed ✅

### Issue #2 — Date comparison แบบ string
**พบเมื่อ**: ทดสอบ overdue check ข้ามเดือน  
**อาการ**: "2026-09-01" < "2026-10-01" ถูก แต่ "2026-9-1" < "2026-10-1" ผิด  
**แก้ไข**: ใช้ `date.fromisoformat()` แทนการ compare string โดยตรง  
**สถานะ**: Fixed ✅

---

## สิ่งที่ยังไม่ได้ทดสอบ (Known Gaps)

| Test Case | เหตุผลที่ยังไม่ทำ | Priority |
|---|---|---|
| borrow_log ขนาดใหญ่ (> 10,000 entries) | ต้องใช้ time measurement | Low |
| input validation ใน _ui_*() functions | ต้องใช้ mock input | Low |
| concurrent access (2 user พร้อมกัน) | Python single-thread ไม่มีปัญหา แต่เมื่อย้ายไป web | Future |
| unicode ในชื่อหนังสือ/สมาชิก | ทดสอบด้วยชื่อภาษาไทยแล้ว ยังไม่ครอบคลุมภาษาอื่น | Low |

---

## สรุป

ระบบผ่านการทดสอบ **14/14 test cases (100%)** ครอบคลุม:
- Happy path ทุก function
- Error cases ที่สำคัญ (KeyError, ValueError)
- Integration test Full Lifecycle
- Edge case ค่าปรับเมื่อเลยกำหนด

**โค้ดพร้อมใช้งาน** สำหรับ demo และส่งงาน  
**Next step**: เพิ่ม file I/O และทดสอบ persistence
