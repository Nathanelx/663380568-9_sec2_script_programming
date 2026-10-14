# Week 11 LabX BASIC: Automating PDFs & Word Documents

โปรเจกต์นี้ใช้ `PyPDF2` จัดการไฟล์ PDF และ `python-docx` สร้างเอกสาร Word (`.docx`)
โดยดึงข้อความจาก PDF มาใส่ในรายงาน Word พร้อมหัวข้อ ข้อความจัดรูปแบบ และตาราง แล้วรวมไฟล์ PDF หลายไฟล์เป็นไฟล์เดียว

## 🎯 สิ่งที่โปรแกรมทำ

**Task 1: PDF → Word Report**
1. อ่าน `documents/input_article.pdf` ด้วย `PdfReader` แล้วดึงข้อความทุกหน้าด้วย `page.extract_text()`
2. สร้างเอกสาร Word ใหม่ด้วย `docx.Document()`
3. ใส่หัวข้อ (Heading 1), ข้อความตัวหนา, ข้อความตัวเอียงจัดกึ่งกลาง และข้อความที่ดึงจาก PDF
4. ใส่หัวข้อ "Summary Data" (Heading 2) และตาราง 4×3 แบบ `Table Grid` (หัวตารางตัวหนา)
5. บันทึกเป็น `documents/output_report.docx`

**Task 2: Merge PDFs**
- รวม `dummy_doc1.pdf` และ `dummy_doc2.pdf` เป็น `documents/merged_output.pdf` ด้วย `PdfWriter.add_page()`

> `pdf_processor.py` มีฟังก์ชัน `split_pdf()` สำหรับแยก PDF เป็นไฟล์ย่อย และ `word_processor.py` มี `add_picture()` สำหรับใส่รูป ไว้ใช้ต่อยอด

## 📂 โครงสร้างโปรเจกต์

```text
document-automator/
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py      # PDFProcessor: extract text, merge, split (PyPDF2)
│   ├── word_processor.py     # WordProcessor: heading, paragraph, table, picture (python-docx)
│   └── utils.py              # logging และสร้างโฟลเดอร์
├── documents/
│   ├── input_article.pdf     # PDF ต้นฉบับสำหรับดึงข้อความ (2 หน้า)
│   ├── dummy_doc1.pdf        # PDF สำหรับทดสอบการรวม
│   ├── dummy_doc2.pdf        # PDF สำหรับทดสอบการรวม
│   ├── output_report.docx    # ผลลัพธ์: รายงาน Word
│   └── merged_output.pdf     # ผลลัพธ์: PDF ที่รวมแล้ว
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 วิธีรัน

```powershell
cd "Lab X Basic\week11\document-automator"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

ถ้า activate แล้วเจอ error `running scripts is disabled on this system` ให้รัน

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## ✅ ผลลัพธ์

```text
pdf_processor - INFO - Extracting text from '...\documents\input_article.pdf' (2 pages)...
word_processor - INFO - Added heading (Level 1): 'Automated Document Report'
word_processor - INFO - Added table with 4 rows and 3 columns.
word_processor - INFO - Word document saved to '...\documents\output_report.docx'.
pdf_processor - INFO - PDFs successfully merged to '...\documents\merged_output.pdf'.
__main__ - INFO - --- Document Automation Workflow Completed ---
```

**`output_report.docx`**
- **Automated Document Report** (Heading 1)
- ข้อความตัวหนา: *This report was automatically generated from PDF content and structured data.*
- ข้อความตัวเอียงกึ่งกลาง: `--- Extracted Content from PDF ---`
- ข้อความจาก PDF ทั้ง 2 หน้า (คั่นด้วย `--- Page End ---`)
- **Summary Data** (Heading 2) และตาราง

| Metric | Value | Notes |
| --- | --- | --- |
| Total Pages Processed | 2 | From Input PDF |
| Document Type | PDF/Word Hybrid | |
| Generated Date | (วันที่รัน) | |

**`merged_output.pdf`** มี 2 หน้า: "This is Dummy Document 1 for merging test." และ "This is Dummy Document 2 for merging test."

## 🔧 Debugging

| ปัญหา | วิธีแก้ |
| --- | --- |
| `can't open file '...\main.py'` | ยังไม่ได้ `cd` เข้าโฟลเดอร์ `document-automator` |
| `ModuleNotFoundError: No module named 'PyPDF2'` / `'docx'` | activate `.venv` แล้วรัน `pip install -r requirements.txt` (ชื่อแพ็กเกจคือ `python-docx` ไม่ใช่ `docx`) |
| `Required input PDF ... not found` | ตรวจว่ามี `input_article.pdf` ในโฟลเดอร์ `documents/` |
| `PdfReadError` | ไฟล์ PDF เสีย ถูกเข้ารหัส หรือไม่ใช่ PDF จริง |
| ข้อความใน Word ว่าง | PDF เป็นรูปภาพสแกน ไม่มีข้อความให้ดึง |
| `PermissionError` ตอนบันทึก | ปิด `output_report.docx` / `merged_output.pdf` ที่เปิดค้างไว้ก่อนรัน |

## Source

- Automate the Boring Stuff with Python, Chapter 15: Working with PDF and Word Documents: <https://automatetheboringstuff.com/2e/chapter15/>
