# Week 10 LabX ADV: Advanced Spreadsheet Automation & Agentic Workflows

**Agentic Spreadsheet Processor** คือ agent ที่จัดการไฟล์ Excel (`.xlsx`) ตาม "แผน" ในไฟล์ config
(`configs/example_spreadsheet_config.json`) โดยใช้ฟีเจอร์ขั้นสูงของ `openpyxl` ได้แก่ สูตร Excel, conditional formatting และกราฟ
แล้วบันทึกทุกขั้นตอนลงชีต **Audit Log** ในไฟล์ผลลัพธ์

## 🧠 แนวคิด Agent

```text
config (แผน) ──► SpreadsheetAgent.run()
                   ├─ โหลด input_file
                   ├─ วนทำ tasks ตามลำดับ (copy_data / calculate_column / conditional_format / chart)
                   ├─ บันทึก audit log ทุกขั้นตอน (SUCCESS / WARNING / ERROR)
                   ├─ สร้างชีต "Audit Log"
                   └─ บันทึก output_file
```

## 📋 Task ที่รองรับ

| type | ทำอะไร | key ที่ใช้ |
| --- | --- | --- |
| `copy_data` | คัดลอกข้อมูลจากชีตหนึ่งไปอีกชีต | `source_sheet`, `dest_sheet` |
| `calculate_column` | ใส่สูตร Excel ทั้งคอลัมน์ (`{row}` = เลขแถว) | `sheet`, `target_column`, `header`, `start_row`, `formula`, `number_format` |
| `conditional_format` | `color_scale`, `data_bar`, `icon_set`, `expression` | `sheet`, `range`, `rule_type` + สีหรือสูตร |
| `chart` | สร้างกราฟ `bar` / `line` / `pie` | `sheet`, `chart_type`, `data_range`, `category_range`, `title`, `top_left_cell` |

## 📂 โครงสร้างโปรเจกต์

```text
agentic-spreadsheet-processor/
├── src/
│   ├── __init__.py
│   ├── spreadsheet_agent.py        # SpreadsheetAgent: วน task, จัดการ Excel, audit log
│   ├── config_parser.py            # โหลดและตรวจสอบ config
│   ├── utils.py                    # logging และ helper
│   └── google_sheets_utils.py      # โครงสำหรับต่อ Google Sheets API ในอนาคต (แนวคิด)
├── configs/
│   └── example_spreadsheet_config.json   # แผนงานของ agent (6 tasks)
├── data/
│   ├── input_data.xlsx             # ข้อมูลขาเข้า (ชีต SalesData)
│   └── output_report.xlsx          # ไฟล์ผลลัพธ์
├── create_dummy_data.py            # สคริปต์สร้าง input_data.xlsx
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 📥 ข้อมูลขาเข้า (`data/input_data.xlsx`, ชีต `SalesData`)

| Product Name | Quantity | Unit Price |
| :--- | :--- | :--- |
| Laptop | 2 | 1200.50 |
| Mouse | 5 | 25.00 |
| Keyboard | 3 | 75.99 |
| Monitor | 1 | 300.00 |
| Projector | 1 | 850.00 |
| Webcam | 10 | 45.00 |
| Headset | 4 | 99.99 |
| SSD | 2 | 180.00 |
| Router | 1 | 70.00 |

## 🚀 วิธีรัน

```powershell
cd "Lab X Advance\Lab10\agentic-spreadsheet-processor"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_dummy_data.py   # สร้าง data/input_data.xlsx (มีให้แล้ว รันซ้ำได้)
python main.py
```

## ✅ ผลลัพธ์ (`data/output_report.xlsx`)

ไฟล์มี 3 ชีต: **Audit Log**, **SalesData**, **Raw Data**

**Raw Data**
- คัดลอกข้อมูลจาก SalesData
- คอลัมน์ D `Total Revenue` = `=B{row}*C{row}` รูปแบบ `#,##0.00` พร้อม color scale (แดง → เหลือง → เขียว)
- คอลัมน์ E `Status` = `=IF(D{row}>1000,"High Value","Standard")` เซลล์ที่เป็น High Value จะไฮไลต์สีเขียว
- กราฟแท่ง "Top 4 Product Revenue" ที่เซลล์ G2 (Laptop, Mouse, Keyboard, Monitor)

| Product Name | Quantity | Unit Price | Total Revenue | Status |
| :--- | :--- | :--- | ---: | :--- |
| Laptop | 2 | 1200.5 | 2,401.00 | High Value |
| Mouse | 5 | 25 | 125.00 | Standard |
| Keyboard | 3 | 75.99 | 227.97 | Standard |
| Monitor | 1 | 300 | 300.00 | Standard |
| Projector | 1 | 850 | 850.00 | Standard |
| Webcam | 10 | 45 | 450.00 | Standard |
| Headset | 4 | 99.99 | 399.96 | Standard |
| SSD | 2 | 180 | 360.00 | Standard |
| Router | 1 | 70 | 70.00 | Standard |

> ค่าในคอลัมน์ D และ E เป็นสูตร Excel จะคำนวณเมื่อเปิดไฟล์ใน Excel (ถ้าอ่านด้วย `openpyxl` จะเห็นเป็นข้อความสูตร)

**Audit Log** บันทึกเวลา สถานะ ประเภท task และรายละเอียดของทุกขั้นตอน

> 📸 การส่งงาน: แนบรูปหน้าชีต **Raw Data**, **SalesData** และ **Audit Log** ของไฟล์ `output_report.xlsx`

## ☁️ Google Sheets (แนวคิด)

- `gspread` ทำงานกับไฟล์บน cloud ผ่าน API ส่วน `openpyxl` ทำงานกับไฟล์ในเครื่อง
- ยืนยันตัวตนด้วย Service Account (เหมาะกับสคริปต์อัตโนมัติ) หรือ OAuth (ทำงานในนามผู้ใช้)
- Google Sheets API เน้นอ่าน/เขียนเป็นช่วง (range) เพื่อลดจำนวน request
- เหมาะเมื่อต้องทำงานร่วมกันหลายคนหรือข้อมูลอยู่บน cloud — ดูโครงใน `src/google_sheets_utils.py`

## 🔧 Debugging

| ปัญหา | วิธีแก้ |
| --- | --- |
| `ModuleNotFoundError: No module named 'src'` | `cd` เข้าโฟลเดอร์ `agentic-spreadsheet-processor` ก่อนรัน |
| `Input Excel file not found` | รัน `python create_dummy_data.py` |
| `Configuration error: ...` | config ขาด key ที่จำเป็น ดูตาราง Task ด้านบน |
| ชีตชื่อไม่ตรง | ชื่อ `source_sheet` ใน config ต้องเป็น `SalesData` ตรงกับไฟล์ |
| `#NAME?` / `#VALUE!` ใน Excel | สูตรใน config ผิด ลองพิมพ์สูตรใน Excel ดูก่อน |
| `PermissionError` ตอนบันทึก | ปิดไฟล์ `output_report.xlsx` ใน Excel ก่อนรัน |
