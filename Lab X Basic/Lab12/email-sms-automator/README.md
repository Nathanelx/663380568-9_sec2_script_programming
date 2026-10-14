# Week 12 LabX BASIC: Automating Communications (Email & SMS)

โปรเจกต์นี้ใช้ Python ส่งอีเมลด้วย `smtplib` (SMTP), รับและอ่านอีเมลด้วย `imaplib` (IMAP)
และส่ง SMS ผ่าน email-to-SMS gateway โดยเก็บรหัสผ่านไว้ในไฟล์ `.env` (ไม่เขียนลงในโค้ด)

## 🎯 สิ่งที่โปรแกรมทำ (`main.py`)

| Task | ทำอะไร |
| --- | --- |
| 1 | ส่งอีเมลข้อความธรรมดา "ทดสอบ Automated Python Test Email" ไปที่ `TEST_RECIPIENT_EMAIL` |
| 2 | ส่งอีเมลพร้อมไฟล์แนบ `data/dummy_report.pdf` ("ทดสอบ Python Test Email with Attachment - Daily Report") |
| 3 | ส่ง SMS โดยส่งอีเมลไปที่ gateway ของค่ายมือถือ เช่น `1234567890@txt.att.net` |
| 4 | ส่งอีเมลหาตัวเอง ("ทดสอบ Python Test: Email for Receiving Demo") แล้วค้นหาอีเมลที่ยังไม่อ่าน (`UNSEEN` + `FROM` + `SUBJECT`) แสดงผู้ส่ง หัวข้อ เนื้อหาบางส่วน ดาวน์โหลดไฟล์แนบไปที่ `data/attachments/` และทำเครื่องหมายว่าอ่านแล้ว |

เนื้อหาของอีเมลทุกฉบับขึ้นต้นด้วยค่า `STUDENT_INFO` (ชื่อ-นามสกุล และรหัสนักศึกษา) จากไฟล์ `.env`

## 📂 โครงสร้างโปรเจกต์

```text
email-sms-automator/
├── src/
│   ├── __init__.py
│   ├── email_sender.py      # EmailSender: ส่งอีเมล (SMTP + STARTTLS, ข้อความ/HTML, ไฟล์แนบ)
│   ├── email_receiver.py    # EmailReceiver: ค้นหา/อ่านอีเมล (IMAP SSL), ดาวน์โหลดไฟล์แนบ, mark as read
│   ├── sms_gateway.py       # SMSGateway: ส่ง SMS ผ่าน email-to-SMS gateway
│   └── utils.py             # logging, โหลด .env, สร้างโฟลเดอร์
├── data/
│   ├── attachments/         # ไฟล์แนบที่ดาวน์โหลดจากอีเมล
│   └── dummy_report.pdf     # ไฟล์แนบตัวอย่าง
├── .env.example             # ตัวอย่างค่าตั้งค่า (คัดลอกเป็น .env)
├── .env                     # ค่าจริง (สร้างเอง ห้าม commit)
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔐 เตรียม Gmail App Password

Gmail ไม่ให้สคริปต์ล็อกอินด้วยรหัสผ่านปกติ ต้องใช้ **App Password** (16 ตัวอักษร)

1. ไปที่ Google Account → **Security**
2. เปิด **2-Step Verification**
3. ค้นหา **App passwords** แล้วสร้างใหม่ (ตั้งชื่อเช่น "Python Automator")
4. คัดลอกรหัส 16 ตัว (ไม่ต้องเว้นวรรค) ไปใส่ใน `SENDER_APP_PASSWORD`

## 🚀 วิธีรัน

1. เข้าโฟลเดอร์โปรเจกต์ สร้างและเปิดใช้งาน venv แล้วติดตั้ง `python-dotenv`

   ```powershell
   cd "Lab X Basic\Lab12\email-sms-automator"
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. คัดลอก `.env.example` เป็น `.env` แล้วแก้ค่าให้เป็นของตัวเอง

   ```powershell
   copy .env.example .env
   ```

   ```ini
   SENDER_EMAIL=your_email@gmail.com
   SENDER_APP_PASSWORD=your_gmail_app_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   IMAP_SERVER=imap.gmail.com
   TEST_RECIPIENT_EMAIL=another_email@example.com
   TEST_SMS_PHONE_NUMBER=1234567890
   TEST_SMS_CARRIER=att
   STUDENT_INFO=ชื่อ-นามสกุล รหัสนักศึกษา 663380568-9
   ```

3. รันโปรแกรม

   ```bash
   python main.py
   ```

## ✅ ผลลัพธ์

ใน terminal จะเห็นแต่ละ task ทำงาน และ Task 4 แสดงข้อมูลอีเมลที่อ่านได้

```text
main - INFO - --- Task 4: Receiving and processing emails ---
src.email_receiver - INFO - Found 1 emails matching criteria in 'INBOX'.
src.email_receiver - INFO - Downloaded attachment: ...\data\attachments\dummy_report.pdf
src.email_receiver - INFO - Marked email UID ... as read.
main - INFO -   Sender: your_email@gmail.com
main - INFO -   Subject: ทดสอบ Python Test: Email for Receiving Demo
main - INFO -   Body Snippet: ชื่อ-นามสกุล รหัสนักศึกษา ...
main - INFO - --- All communication automation tasks completed ---
```

ใน Gmail จะได้อีเมล "ทดสอบ ..." 3 ฉบับ (2 ฉบับมีไฟล์แนบ `dummy_report.pdf`)

> 📱 **เรื่อง SMS:** gateway ในโค้ดเป็นของค่ายมือถือในอเมริกา (AT&T, Verizon, ...) ค่ายในไทยไม่มีบริการนี้
> เมื่อใช้เบอร์ทดสอบ `1234567890` + `att` จะได้อีเมลตีกลับ "ไม่พบที่อยู่ ... txt.att.net" ซึ่งเป็นเรื่องปกติ
> (โค้ดส่งสำเร็จ แต่ปลายทางไม่มีจริง) ถ้าต้องการส่ง SMS จริงควรใช้บริการ SMS API เช่น Twilio

## 🔧 Debugging

| ปัญหา | วิธีแก้ |
| --- | --- |
| `Environment variable 'SENDER_EMAIL' not set` | ยังไม่ได้สร้าง `.env` ในโฟลเดอร์ `email-sms-automator` |
| `SMTPAuthenticationError` / `IMAP authentication failed` | ใช้ App Password ไม่ใช่รหัสผ่านปกติ และตรวจว่าเปิด 2-Step Verification แล้ว |
| `ModuleNotFoundError: No module named 'dotenv'` | activate `.venv` แล้วรัน `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'src'` | `cd` เข้าโฟลเดอร์ `email-sms-automator` ก่อนรัน |
| เชื่อมต่อไม่ได้ / timeout | เครือข่ายบล็อกพอร์ต 587 (SMTP) หรือ 993 (IMAP) ลองใช้เน็ตอื่น |
| Task 4 หาอีเมลไม่เจอ | Gmail ยังส่งไม่ถึง ลองรันใหม่ หรือเพิ่มเวลารอใน `time.sleep(10)` |
| อีเมลไม่เข้า | ดูในโฟลเดอร์ Spam และอย่าส่งถี่เกินไป (rate limit) |

## Source

- Automate the Boring Stuff with Python, Chapter 18: Sending Email and Text Messages: <https://automatetheboringstuff.com/2e/chapter18/>
