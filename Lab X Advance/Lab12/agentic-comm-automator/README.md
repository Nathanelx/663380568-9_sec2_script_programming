# Week 12 LabX ADV: Agentic Communication Workflows (Advanced Email & SMS)

ต่อยอดจาก Lab Basic (`email-sms-automator`) เป็น **CommunicationAgent** ที่ทำงานตาม "แผน" ในไฟล์
`configs/comm_pipeline_config.json` รองรับข้อความแบบ template, ผู้รับหลายคน (To/CC/BCC), แนบหลายไฟล์,
และอ่านกล่องจดหมายแล้วทำงานตาม **rule** (if → then) เช่น ส่ง SMS แจ้งเตือน หรือตอบกลับอัตโนมัติ

## 🧠 แนวคิด Agent

```text
.env (รหัสผ่าน/ผู้รับ) ─┐
config (แผน) ───────────┴► CommunicationAgent.run()
                             ├─ context: report_date, sales_figure, total_customers, student_info, ...
                             ├─ Task 1 send_email     → รายงานยอดขาย (To + CC, แนบ PDF + XLSX)
                             ├─ Task 2 send_sms       → SMS สรุปยอดขาย
                             ├─ Task 3 send_email     → จำลองอีเมล "Data Request ... - Urgent" ส่งหาตัวเอง
                             ├─ Task 4 process_inbox  → ค้นหาอีเมล UNSEEN จากตัวเองที่หัวข้อมี "Data Request"
                             │     ├─ Rule 1: หัวข้อมี "Urgent" และมีไฟล์แนบ  → ส่ง SMS แจ้งเตือน
                             │     └─ Rule 2: เนื้อหามี "new data processing" → ตอบกลับอัตโนมัติ
                             └─ reports/audit_report_comm_YYYYMMDD_HHMMSS.json
```

- **Template:** ใช้รูปแบบ `{report_date}`, `{sales_figure:,.2f}`, `{attachments_meta[0][filepath]}` แทนค่าจาก context
- **ค่าจาก `.env`:** เขียนใน config เป็น `${TEST_RECIPIENT_EMAIL}` (ตัวพิมพ์ใหญ่) agent จะแทนค่าให้ตอนโหลด config
  จึงไม่ต้องใส่อีเมล/เบอร์จริงลงใน config และไม่หลุดขึ้น git
- **Context:** ผลลัพธ์ของ task ที่มี `output_context_key` จะถูกเก็บใน context ให้ task ถัดไปใช้ได้

## 📋 Task ที่รองรับ

| type | parameters หลัก |
| --- | --- |
| `send_email` | `recipients` {`to`, `cc`, `bcc`}, `subject_template`, `body_template`, `attachments`, `is_html` |
| `send_sms` | `phone_numbers` (list), `message_template`, `carrier_name` |
| `process_inbox` | `search_criteria` {`status`, `from_sender`, `subject_contains`}, `wait_seconds`, `download_attachments_base_dir`, `rules` |

**Rule conditions (`if`):** `subject_contains`, `body_contains`, `from_sender_contains`, `has_attachments`
**Rule actions (`then`):** `send_sms_alert` (+ `alert_phone_numbers`, `alert_carrier`, `alert_message_template`), `reply_with_template` (+ `reply_subject_template`)

## 📂 โครงสร้างโปรเจกต์

```text
agentic-comm-automator/
├── src/
│   ├── __init__.py
│   ├── communication_agent.py   # CommunicationAgent: วน task, context, rules, audit
│   ├── email_tasks.py           # EmailTasks: ส่ง (SMTP) / ค้นหา-อ่าน (IMAP) อีเมล
│   ├── sms_tasks.py             # SMSTasks: ส่ง SMS ผ่าน email-to-SMS gateway
│   ├── config_parser.py         # โหลด config + แทนค่า ${ENV} + ตรวจสอบ
│   ├── template_renderer.py     # แทนค่า {placeholder} ใน template
│   └── utils.py                 # logging, .env, audit log
├── configs/
│   └── comm_pipeline_config.json
├── data/
│   ├── attachments/             # ไฟล์แนบทั่วไป
│   ├── reports/
│   │   ├── sales_report.pdf     # ไฟล์แนบตัวอย่าง 1
│   │   └── summary_data.xlsx    # ไฟล์แนบตัวอย่าง 2
│   └── incoming_attachments/    # ไฟล์แนบที่ดาวน์โหลดจากอีเมลที่ประมวลผล
├── reports/                     # audit report (สร้างตอนรัน)
├── .env.example                 # ตัวอย่างค่าตั้งค่า (คัดลอกเป็น .env)
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 วิธีรัน

1. เข้าโฟลเดอร์ เปิดใช้ venv และติดตั้ง `python-dotenv`

   ```powershell
   cd "Lab X Advance\Lab12\agentic-comm-automator"
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. สร้าง `.env` จากตัวอย่าง แล้วใส่อีเมล Gmail, **App Password**, ผู้รับ และ `STUDENT_INFO`
   (วิธีสร้าง App Password ดูได้ใน README ของ `email-sms-automator`)

   ```powershell
   copy .env.example .env
   notepad .env
   ```

3. รันโปรแกรม

   ```bash
   python main.py
   ```

## ✅ ผลลัพธ์

ใน terminal:

```text
AUDIT LOG - SUCCESS: Task 'Send Daily Sales Report Email' completed successfully.
AUDIT LOG - SUCCESS: Task 'Send Sales Alert SMS' completed successfully.
AUDIT LOG - SUCCESS: Task 'Simulate Incoming Request Email (to self)' completed successfully.
Rule 1 matched for email UID ... Applying actions...
Rule 2 matched for email UID ... Applying actions...
AUDIT LOG - SUCCESS: Task 'Process Incoming Data Requests' completed successfully.
Communication Agent finished. Total time: ... seconds. Errors: 0
```

ใน Gmail ของ `SENDER_EMAIL`:

| อีเมล | มาจาก |
| --- | --- |
| **Daily Sales Report - YYYY-MM-DD** (แนบ `sales_report.pdf`, `summary_data.xlsx`) | Task 1 (CC ถึงตัวเอง) |
| **Data Request for YYYY-MM-DD - Urgent** (แนบ `sales_report.pdf`) | Task 3 |
| **Re: Data Request for YYYY-MM-DD - Urgent - Received & Processing** | Rule 2 ตอบกลับอัตโนมัติ |
| อีเมลตีกลับ "ไม่พบที่อยู่ ... txt.att.net" 2 ฉบับ | SMS จาก Task 2 และ Rule 1 |

ไฟล์ที่ได้: `data/incoming_attachments/sales_report.pdf` และ `reports/audit_report_comm_*.json`

> 📱 gateway SMS ในโค้ดเป็นของค่ายมือถืออเมริกา ค่ายในไทยไม่รองรับ จึงได้อีเมลตีกลับ ซึ่งเป็นเรื่องปกติของแลปนี้
> 🔁 ถ้ารันซ้ำ อีเมล "Re: Data Request ..." จากรอบก่อนจะถูกค้นเจอด้วย แต่ไม่มีไฟล์แนบและไม่มีคำว่า "new data processing" จึงไม่ตรง rule ใด

## 🔧 Debugging

| ปัญหา | วิธีแก้ |
| --- | --- |
| `Environment variable 'SENDER_EMAIL' not set` | ยังไม่ได้สร้าง `.env` ในโฟลเดอร์ `agentic-comm-automator` |
| `SMTPAuthenticationError` / `IMAP authentication failed` | ต้องใช้ App Password ไม่ใช่รหัสผ่านปกติ |
| `Missing context key: ...` | template ใน config อ้างชื่อที่ไม่มีใน context ตรวจการสะกด `{...}` |
| `ModuleNotFoundError: No module named 'src'` | `cd` เข้าโฟลเดอร์ `agentic-comm-automator` ก่อนรัน |
| `Required attachment files are missing` | ตรวจว่ามีไฟล์ใน `data/reports/` |
| `No emails found matching search criteria` | Gmail ยังส่งไม่ถึง เพิ่ม `wait_seconds` ใน config แล้วรันใหม่ |
