# Week 11 LabX ADV: Agentic Document Automator

**Document Agent** ที่ทำงานกับเอกสาร Word และ PDF ตาม "แผน" ในไฟล์ config (`configs/document_automation_config.json`)
ต่อยอดจาก Lab Basic (`document-automator`) โดยเพิ่มการสร้างรายงานจาก **template**, การใส่ **ลายน้ำ** ใน PDF และ **audit report**

## 🧠 แนวคิด Agent

```text
config (แผน) ──► DocumentAgent.run()
                   ├─ วนทำ tasks ตามลำดับ
                   │    ├─ generate_word_report  → เติมค่าใน template + ใส่ตาราง
                   │    ├─ apply_pdf_watermark   → ใส่ลายน้ำ "CONFIDENTIAL"
                   │    ├─ merge_pdfs            → รวม PDF
                   │    ├─ extract_word_text     → ดึงข้อความจาก Word → .txt
                   │    └─ extract_pdf_text      → ดึงข้อความจาก PDF → .txt
                   ├─ บันทึก audit log ทุกขั้นตอน (INFO / SUCCESS / ERROR)
                   └─ สร้าง documents/reports/audit_report_YYYYMMDD_HHMMSS.json
```

## 📋 Task ที่รองรับ

| type | ทำอะไร | key ที่ต้องมี |
| --- | --- | --- |
| `generate_word_report` | เปิด template `.docx` แทนค่า `{{KEY}}` ด้วยข้อมูลจาก `global_data` + `data` และใส่ตาราง `table_data` ที่ตำแหน่ง `{{TABLE_PLACEHOLDER}}` | `template_path`, `output_path` |
| `apply_pdf_watermark` | สร้างหน้าลายน้ำด้วย `reportlab` แล้ว `merge_page` ทับทุกหน้า | `input_pdf`, `output_pdf`, `watermark_text` (+ `font_size`, `color` RGBA, `angle`) |
| `merge_pdfs` | รวมหลายไฟล์ PDF เป็นไฟล์เดียว | `input_pdfs`, `output_pdf` |
| `extract_word_text` | ดึงข้อความ (ย่อหน้า + ตาราง) จาก Word | `input_docx`, `output_text_file` |
| `extract_pdf_text` | ดึงข้อความจาก PDF | `input_pdf`, `output_text_file` |

## 📂 โครงสร้างโปรเจกต์

```text
agentic-document-automator/
├── configs/
│   └── document_automation_config.json   # แผนงานของ agent (5 tasks)
├── templates/
│   └── report_template.docx              # template มี {{REPORT_TITLE}}, {{REPORT_DATE}}, ..., {{TABLE_PLACEHOLDER}}
├── documents/
│   ├── source_document.pdf               # input: PDF สำหรับใส่ลายน้ำ/ดึงข้อความ
│   ├── dummy_doc1.pdf, dummy_doc2.pdf    # input: PDF สำหรับรวม (Part A, Part B)
│   ├── generated_report.docx             # output: รายงาน Word
│   ├── watermarked_document.pdf          # output: PDF ที่มีลายน้ำ CONFIDENTIAL
│   ├── merged_docs.pdf                   # output: PDF ที่รวมแล้ว (2 หน้า)
│   ├── extracted_word_text.txt           # output: ข้อความจาก Word
│   ├── extracted_pdf_text.txt            # output: ข้อความจาก PDF
│   └── reports/audit_report_*.json       # output: audit report
├── src/
│   ├── __init__.py
│   ├── document_agent.py                 # DocumentAgent: วน task + audit log
│   ├── word_tasks.py                     # WordTasks: template, ตาราง, ดึงข้อความ (python-docx)
│   ├── pdf_tasks.py                      # PDFTasks: ลายน้ำ, รวม, ดึงข้อความ (PyPDF2 + reportlab)
│   ├── config_parser.py                  # โหลดและตรวจสอบ config
│   └── utils.py                          # logging, สร้างโฟลเดอร์, audit log
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 วิธีรัน

```powershell
cd "Lab X Advance\week11\agentic-document-automator"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

ถ้า activate แล้วเจอ error `running scripts is disabled on this system` ให้รัน `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## ✅ ผลลัพธ์

```text
word_tasks - INFO - Replaced '{{REPORT_TITLE}}' with 'Monthly Performance Summary'.
...
word_tasks - INFO - Dynamic table inserted at '{{TABLE_PLACEHOLDER}}'.
pdf_tasks - INFO - Watermark applied to '...\source_document.pdf'. Output saved to '...\watermarked_document.pdf'.
pdf_tasks - INFO - PDFs successfully merged to '...\merged_docs.pdf'.
INFO - AUDIT LOG - INFO: Finished in 0.05s with 0 error(s). | Task: agent_run_summary
__main__ - INFO - Document automation process completed. Audit report: ...\documents\reports\audit_report_....json
```

`documents/extracted_word_text.txt` (ข้อความจาก `generated_report.docx`)

```text
   REPORT TITLE: Monthly Performance Summary
   DATE: 2026-09-08
   AUTHOR: AI Document Agent
   COMPANY: Automated Docs Inc.
   ---
   INTRODUCTION:
   This automated report provides a summary of key performance indicators.
   ---
   MONTHLY OVERVIEW: August 2026
   Here is a summary of key performance indicators:
   ---
   CONCLUSION:
   This report concludes the performance analysis.
Category	Value	Trend
Sales Revenue	$120,000	Up 10%
Customer Acquisition	500	Stable
Project Completion Rate	95%	Excellent
```

> ในไฟล์ Word ตารางอยู่ตรงตำแหน่ง `{{TABLE_PLACEHOLDER}}` (ใต้ "Here is a summary...") ส่วนไฟล์ .txt ดึงตารางไว้ท้ายสุด
> template นี้ไม่มี style "Table Grid" ตารางจึงใช้ style เริ่มต้นของ template (ไม่มีเส้นขอบ)

## 🔧 Debugging

| ปัญหา | วิธีแก้ |
| --- | --- |
| `ModuleNotFoundError: No module named 'reportlab'` | activate `.venv` แล้วรัน `pip install -r requirements.txt` |
| `Required input file not found` | ตรวจว่ามี `templates/report_template.docx` และ PDF ใน `documents/` ครบ |
| ค่าใน Word ไม่ถูกแทนที่ | ชื่อ key ใน config ต้องตรงกับ `{{KEY}}` ใน template และ placeholder ต้องพิมพ์ต่อกันใน run เดียว (ห้ามจัดรูปแบบแยกบางตัวอักษร) |
| `Configuration error: Task N requires ...` | task ใน config ขาด key ที่จำเป็น ดูตาราง Task ด้านบน |
| `PermissionError` ตอนบันทึก | ปิดไฟล์ Word/PDF ใน `documents/` ที่เปิดค้างไว้ก่อนรัน |
