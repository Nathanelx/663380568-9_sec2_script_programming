# Week 8 LabX ADV: Agentic Data Processor (CSV & JSON)

ต่อยอดจาก `data-processor` (Basic) ไปเป็น **Data Agent** ที่ทำงานตาม "แผน" ในไฟล์ config
แทนที่จะเขียนขั้นตอนตายตัวใน `main.py` agent จะอ่านรายการ `tasks` จาก `configs/data_pipeline_config.json`
แล้วทำทีละ task ตามลำดับ ส่งข้อมูลต่อกันผ่าน **data store** และบันทึกทุกขั้นตอนลง **audit report**

ใช้แค่ built-in modules (`csv`, `json`, `logging`, `collections`, `copy`, `datetime`) จึงไม่ต้อง `pip install` อะไร

## 🧠 แนวคิด Agent

```text
config (แผน)  ──►  DataAgent.run()
                     │  วนทำแต่ละ task
                     ├─ อ่าน input จาก data_store[input_data_key]
                     ├─ ส่งให้ handler ที่ตรงกับ type (CSVTasks / JSONTasks / ConversionTasks)
                     ├─ เก็บผลลัพธ์ใน data_store[output_data_key]
                     └─ บันทึก audit log (INFO / SUCCESS / ERROR)
                   ──►  reports/audit_report_YYYYMMDD_HHMMSS.json
```

ถ้า task ไหนล้มเหลว agent จะบันทึก ERROR แล้วทำ task ถัดไปต่อ ไม่หยุดทั้งโปรแกรม

## 📋 Task ที่รองรับ

| type | ทำอะไร | key ที่ต้องมี |
| --- | --- | --- |
| `load_csv` | อ่าน CSV เป็น list ของ dict | `file_path`, `output_data_key` |
| `save_csv` | เขียน list ของ dict เป็น CSV | `file_path`, `input_data_key` (`fieldnames` ไม่ใส่ก็ได้) |
| `transform_csv_aggregate` | จัดกลุ่มแล้วรวมค่า (`sum` / `count` / `average`) | `group_by_field`, `aggregate_field` |
| `filter_csv` | กรองแถวด้วย `>`, `<`, `>=`, `<=`, `==`, `!=` | `filter_field`, `operator`, `value` |
| `load_json` / `save_json` | อ่าน/เขียน JSON | `file_path` |
| `update_json_data` | แก้ JSON ด้วย path แบบจุด เช่น `0.details.dpi` (`set`, `add_to_list`, `remove_from_list`) | `updates` |
| `query_json_data` | ดึงค่าจาก path เช่น `0.details.brand` | `path` |
| `csv_to_json_conversion` | แปลง string จาก CSV เป็นตัวเลข/boolean/null | `input_data_key`, `output_data_key` |
| `json_to_csv_conversion` | แปลง JSON ซ้อนเป็น CSV แบน (`details.brand`) | `input_data_key`, `output_data_key` |

> path ว่าง `""` หมายถึง root เช่น `{"path": "", "operation": "add_to_list"}` คือเพิ่มสินค้าเข้า list หลัก

## 📂 โครงสร้างโปรเจกต์

```text
agentic-data-processor/
├── configs/
│   └── data_pipeline_config.json      # แผนงานของ agent (9 tasks)
├── data/
│   ├── input_sales.csv                # ข้อมูลขาเข้า
│   ├── input_inventory.json           # ข้อมูลขาเข้า
│   ├── processed_sales_by_customer.csv  # ยอดขายรวมต่อลูกค้า
│   ├── sales_data.json                # sales แปลงเป็น JSON
│   └── updated_inventory.json         # inventory หลังแก้ไข
├── reports/
│   └── audit_report_*.json            # บันทึกการทำงานของ agent
├── src/
│   ├── __init__.py
│   ├── config_parser.py               # อ่านและตรวจสอบ config
│   ├── data_agent.py                  # DataAgent: วน task + data store + audit
│   ├── csv_tasks.py                   # load/save/aggregate/filter CSV
│   ├── json_tasks.py                  # load/save/update/query JSON
│   ├── conversion_tasks.py            # CSV <-> JSON
│   └── utils.py                       # logging, สร้างโฟลเดอร์, audit log
├── main.py
├── .gitignore
└── README.md
```

## 🚀 วิธีรัน

ต้องรันจากในโฟลเดอร์โปรเจกต์ เพราะ `main.py` import ผ่าน package `src`

```powershell
cd "Lab X Advance\Lab8\agentic-data-processor"
python main.py
```

## ✅ ผลลัพธ์

ใน terminal จะเห็นแต่ละ task ทำงานและจบด้วย

```text
src.data_agent - INFO - Data Agent finished. Total time: 0.01 seconds. Errors: 0
src.data_agent - INFO - Audit report saved to: ...\reports\audit_report_YYYYMMDD_HHMMSS.json
```

`data/processed_sales_by_customer.csv`

```csv
Customer,Total_Amount
Alice,1425.75
Bob,130.75
Charlie,500.0
David,90.0
Eve,15.5
```

`data/updated_inventory.json` สินค้าตัวแรกหลังแก้ไข (stock 75 และเพิ่ม color) และมี PROD004 Smart Speaker ต่อท้าย

```json
{
  "id": "PROD001",
  "name": "Laptop Pro",
  "category": "Electronics",
  "stock": 75,
  "details": {
    "brand": "TechCorp",
    "model": "XPS 15",
    "color": "Space Grey"
  }
}
```

Query `0.details.brand` ได้ผลเป็น `TechCorp` (ดูได้ใน audit report)

## 🔧 Troubleshooting

| ปัญหา | วิธีแก้ |
| --- | --- |
| `ModuleNotFoundError: No module named 'src'` | ต้อง `cd` เข้าโฟลเดอร์ `agentic-data-processor` ก่อนรัน |
| `Configuration error: Task N ... requires '...'` | task ใน config ขาด key ที่จำเป็น ดูตาราง Task ด้านบน |
| `Required input file ... not found` | ตรวจว่ามี `data/input_sales.csv` และ `data/input_inventory.json` |
| `Required input data '...' not found in store` | `input_data_key` ไม่ตรงกับ `output_data_key` ของ task ก่อนหน้า หรือ task ก่อนหน้าล้มเหลว |
| `Path '...' not found` | path ใน `updates` ผิด เช่น index เกินจำนวนสินค้า |
