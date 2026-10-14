# Week 10 LabX BASIC: Automating Spreadsheets (Excel & Google Sheets)

โปรเจกต์นี้ใช้ไลบรารี `openpyxl` อ่านข้อมูลยอดขายจากไฟล์ Excel (`.xlsx`) คำนวณราคารวมของแต่ละสินค้าและยอดรวมทั้งหมด
แล้วเขียนผลลงไฟล์ Excel ใหม่พร้อมจัดรูปแบบ (หัวตารางสีเขียวตัวหนา แถวยอดรวมสีเหลือง เส้นขอบ และรูปแบบตัวเลข)

## 🎯 สิ่งที่ได้ฝึก

- **Workbook & Worksheet**: `openpyxl.load_workbook()`, `openpyxl.Workbook()`, `wb.active`, `wb.create_sheet()`, `wb.save()`
- **อ่าน/เขียนเซลล์**: `sheet.iter_rows(min_row=2, values_only=True)`, `sheet.cell(row=, column=, value=)`
- **คำนวณข้อมูล**: Total Price = Quantity × Unit Price และ Grand Total
- **จัดรูปแบบ**: `Font`, `PatternFill`, `Border`, `Alignment`, `number_format = '#,##0.00'`
- **จัดการโครงสร้างชีต**: `merge_cells()` และปรับความกว้างคอลัมน์อัตโนมัติ
- **Error handling**: ข้ามแถวว่าง และข้ามแถวที่ตัวเลขไม่ถูกต้อง

## 📂 โครงสร้างโปรเจกต์

```text
spreadsheet-automator/
├── src/
│   ├── __init__.py
│   └── excel_processor.py         # คลาส ExcelProcessor (โหลด/สร้าง/บันทึก/ประมวลผล Excel)
├── data/
│   ├── input_sales.xlsx           # ไฟล์ข้อมูลขาเข้า
│   └── output_sales_report.xlsx   # ไฟล์รายงานที่สร้างขึ้น
├── main.py                        # จุดเริ่มต้นโปรแกรม
├── requirements.txt
├── .gitignore
└── README.md
```

## 📥 ข้อมูลขาเข้า (`data/input_sales.xlsx`, ชีต `Sheet1`)

| Product Name | Quantity | Unit Price |
| :----------- | :------- | :--------- |
| Laptop       | 2        | 1200.50    |
| Mouse        | 5        | 25.00      |
| Keyboard     | 3        | 75.99      |
| Monitor      | 1        | 300.00     |
| *(แถวว่าง)*   |          |            |
| Printer      | 1        | 150.00     |

> มีแถวว่างไว้ 1 แถวเพื่อทดสอบว่าสคริปต์ข้ามแถวว่างได้

## 🚀 วิธีรัน

1. เข้าไปที่โฟลเดอร์โปรเจกต์ (ต้องรันจากในโฟลเดอร์นี้ เพราะ `main.py` อ้างถึง `data/` แบบ relative)

   ```powershell
   cd "Lab X Basic\Lab10\spreadsheet-automator"
   ```

2. สร้างและเปิดใช้งาน virtual environment แล้วติดตั้ง `openpyxl`

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. รันโปรแกรม

   ```bash
   python main.py
   ```

## ✅ ผลลัพธ์

```text
Starting sales data processing from 'data\input_sales.xlsx'...
Workbook 'data\input_sales.xlsx' loaded successfully.
New workbook 'new_workbook.xlsx' created.
Workbook saved to 'data\output_sales_report.xlsx'.
Sales report successfully generated and saved to 'data\output_sales_report.xlsx'.
```

`data/output_sales_report.xlsx` (ชีต `Sales Report`)

| Product Name | Quantity | Unit Price | Total Price |
| :----------- | :------- | :--------- | ----------: |
| Laptop       | 2        | 1200.5     | 2,401.00    |
| Mouse        | 5        | 25         | 125.00      |
| Keyboard     | 3        | 75.99      | 227.97      |
| Monitor      | 1        | 300        | 300.00      |
| Printer      | 1        | 150        | 150.00      |
| **Grand Total:** (รวมเซลล์ A–C) | | | **3,203.97** |

## ☁️ Google Sheets (แนวคิด)

- ใช้ Google Sheets API ผ่านไลบรารี เช่น `gspread`
- ต้องยืนยันตัวตนด้วย OAuth 2.0 หรือ Service Account และเก็บไฟล์ key ไว้เป็นความลับ (ห้าม commit ขึ้น git)
- แนวคิดคล้าย `openpyxl` (spreadsheet → worksheet → cell) แต่ทำงานผ่านอินเทอร์เน็ตกับไฟล์บน cloud และมีข้อจำกัดจำนวน request

## 🔧 Debugging

| ปัญหา | วิธีแก้ |
| --- | --- |
| `Error: Input file 'data\input_sales.xlsx' not found.` | ยังไม่ได้ `cd` เข้าโฟลเดอร์ `spreadsheet-automator` หรือไม่มีไฟล์ใน `data/` |
| `ModuleNotFoundError: No module named 'openpyxl'` | activate venv แล้วรัน `pip install -r requirements.txt` |
| `InvalidFileException` | ไฟล์ไม่ใช่ `.xlsx` (เช่น `.xls` แบบเก่า) หรือไฟล์เสีย |
| `PermissionError` ตอนบันทึก | ปิดไฟล์ `output_sales_report.xlsx` ใน Excel ก่อนรันใหม่ |
| ตัวเลขผิด | ลำดับคอลัมน์ต้องเป็น Product Name, Quantity, Unit Price |

## Source

- Automate the Boring Stuff with Python, Chapter 13: Working with Excel Spreadsheets: <https://automatetheboringstuff.com/2e/chapter13/>
