# Week 8 LabX BASIC: Automating with CSV and JSON Data

โปรเจกต์นี้ฝึกการอ่าน เขียน และประมวลผลไฟล์ข้อมูลแบบ plaintext 2 รูปแบบ คือ **CSV** และ **JSON**
โดยใช้โมดูล `csv` และ `json` ที่มากับ Python (ไม่ต้อง `pip install` อะไรเพิ่ม)

## 🎯 สิ่งที่โปรแกรมทำ

**CSV Workflow** (`src/csv_handler.py`)
1. อ่าน `data/input_sales.csv` ด้วย `csv.DictReader` (ได้ list ของ dict)
2. แปลง `Amount` และ `Price` จาก string เป็น `float` แล้วคำนวณยอดขายรวมและราคาเฉลี่ย
3. กรองรายการที่ `Amount >= 100`
4. เขียนรายการที่กรองแล้วพร้อมแถวสรุป (SUMMARY) ลง `data/output_filtered_sales.csv` ด้วย `csv.DictWriter`

**JSON Workflow** (`src/json_handler.py`)
1. อ่าน `data/input_inventory.json` ด้วย `json.load` (มีข้อมูลซ้อนใน `details`)
2. อัปเดต stock ของ `PROD001` เป็น 60 และ `PROD003` เป็น 75
3. เพิ่มสินค้าใหม่ `PROD004` (Gaming Headset)
4. เขียนผลลง `data/output_updated_inventory.json` ด้วย `json.dump(indent=2)`

## 📂 โครงสร้างโปรเจกต์

```text
data-processor/
├── src/
│   ├── __init__.py
│   ├── csv_handler.py      # คลาส CSVHandler: อ่าน/เขียน/ประมวลผล CSV
│   ├── json_handler.py     # คลาส JSONHandler: อ่าน/เขียน/แก้ไข JSON
│   └── utils.py            # logging และสร้างโฟลเดอร์
├── data/
│   ├── input_sales.csv                 # ข้อมูลขาเข้า (CSV)
│   ├── input_inventory.json            # ข้อมูลขาเข้า (JSON)
│   ├── output_filtered_sales.csv       # ผลลัพธ์ CSV
│   └── output_updated_inventory.json   # ผลลัพธ์ JSON
├── main.py                 # จุดเริ่มต้นโปรแกรม
├── .gitignore
└── README.md
```

## 🚀 วิธีรัน

```powershell
cd "week8\data-processor"
python main.py
```

> โปรเจกต์นี้ใช้แค่ built-in modules จึงไม่จำเป็นต้องสร้าง venv แต่ถ้าต้องการก็สร้างได้ด้วย `python -m venv venv` แล้ว `.\venv\Scripts\Activate.ps1`

## ✅ ผลลัพธ์

Log ใน terminal (ตัดเวลาออก):

```text
csv_handler - INFO - Successfully read 8 rows from '...\data\input_sales.csv'.
csv_handler - INFO - Sales data processed. Total Sales: 1902.00, Filtered Count: 3
__main__ - INFO - Summary of all sales: {'Total Sales': '1902.00', 'Average Item Price': '237.75', 'Filtered Sales Count': 3}
csv_handler - INFO - Successfully wrote 4 rows to '...\data\output_filtered_sales.csv'.
json_handler - INFO - Updated stock for product 'PROD001' to 60.
json_handler - INFO - Updated stock for product 'PROD003' to 75.
json_handler - INFO - Added new product: Gaming Headset.
json_handler - INFO - Successfully wrote JSON to '...\data\output_updated_inventory.json'.
__main__ - INFO - --- Data Processing Workflows Completed ---
```

`data/output_filtered_sales.csv`:

```csv
OrderID,Product,Amount,Price,Customer
101,Laptop,1200.50,1200.50,Alice
104,Monitor,300.00,300.00,Charlie
107,Headphones,150.00,150.00,Alice
SUMMARY,Total/Avg,1902.00,237.75,Count: 3
```

> หมายเหตุ: `Total Sales` และ `Average Item Price` คำนวณจาก **ทุกรายการ** (8 รายการ) ส่วน `Count` คือจำนวนรายการที่ผ่านการกรอง (3 รายการ)

## 🔧 Debugging

| ปัญหา | วิธีแก้ |
| --- | --- |
| `can't open file '...\main.py'` | ยังไม่ได้ `cd` เข้าโฟลเดอร์ `data-processor` |
| `CSV file not found` / `JSON file not found` | ตรวจว่า `input_sales.csv` และ `input_inventory.json` อยู่ในโฟลเดอร์ `data/` |
| `KeyError` | ชื่อหัวคอลัมน์ใน CSV ไม่ตรงกับที่โค้ดใช้ (`Amount`, `Price`) หรือมีช่องว่างเกิน |
| `json.JSONDecodeError` | JSON ผิด syntax เช่น ลืม `,` หรือใช้ `'` แทน `"` |
| `ValueError: could not convert string to float` | ค่าตัวเลขใน CSV มีสัญลักษณ์ เช่น `$` หรือ `,` (โค้ดจะข้ามแถวนั้นพร้อมแสดง warning) |
| ตัวอักษรเพี้ยน | ใช้ `encoding='utf-8'` ทั้งตอนอ่านและเขียน |

## Source

- Automate the Boring Stuff with Python, Chapter 16: Working with CSV Files and JSON Data: <https://automatetheboringstuff.com/2e/chapter16/>
