# Week 7 LabX Basic: Introduction to Web Scraping

โปรเจกต์นี้ฝึกพื้นฐาน Web Scraping ด้วย `requests` และ `BeautifulSoup4`
โดยดาวน์โหลดหน้าแรกของ [Automate the Boring Stuff with Python (3rd Edition)](https://automatetheboringstuff.com/3e/)
แล้วดึง **ชื่อหนังสือ** และ **ชื่อบททั้งหมด** ออกมาแสดงผล

## ⚠️ ข้อพิจารณาด้านจริยธรรมและกฎหมาย

- ตรวจสอบ `robots.txt` ของเว็บไซต์ก่อนเสมอ (เช่น `https://automatetheboringstuff.com/robots.txt`)
- อ่าน Terms of Service ว่าอนุญาตให้ scrape หรือไม่
- ไม่ส่ง request ถี่เกินไป (rate limiting) ถ้าต้องดึงหลายหน้าให้ใช้ `time.sleep()` คั่น
- ข้อมูลที่ได้อาจมีลิขสิทธิ์ ใช้เพื่อการศึกษาเท่านั้น
- ถ้าเว็บไซต์มี API ให้ใช้ API แทนการ scrape

## Features

- **HTML Download**: ใช้ `requests.get()` พร้อม `User-Agent` header และ `timeout`
- **HTML Parsing**: ใช้ `BeautifulSoup(html, 'html.parser')`
- **Data Extraction**: ใช้ `find()` หาชื่อหนังสือ (`article > header > h1`) และ `select('ul li a')` หาชื่อบทใน `div.content-body`
- **Error Handling**: จัดการ `HTTPError`, `ConnectionError`, `Timeout` และ `RequestException`

## โครงสร้างโปรเจกต์

```text
web-scraping-intro/
├── src/
│   ├── __init__.py      # บ่งบอกว่า src เป็น Python package
│   └── scraper.py       # คลาส SimpleWebScraper (logic การ scrape)
├── main.py              # จุดเริ่มต้นของโปรแกรม
├── requirements.txt     # dependencies
├── .gitignore
└── README.md
```

## วิธีรัน

0. เข้าไปที่โฟลเดอร์โปรเจกต์ก่อน (ถ้ารันจากโฟลเดอร์อื่นจะขึ้น `can't open file`)

   ```powershell
   cd "week7\LabsX---Basic1-Introduction-to-Web-Scraping\web-scraping-intro"
   ```

1. สร้างและเปิดใช้งาน virtual environment

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   ถ้าเจอ error `running scripts is disabled on this system` ให้รันคำสั่งนี้ก่อน

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. ติดตั้ง dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. รันโปรแกรม

   ```bash
   python main.py
   ```

## ผลลัพธ์ที่ได้

```text
กำลังดาวน์โหลดเนื้อหาจาก: https://automatetheboringstuff.com/3e/
ดาวน์โหลดเนื้อหาสำเร็จ

--- ข้อมูลที่ Scrape ได้ ---
ชื่อหนังสือ: 3rd Edition

ชื่อบทต่างๆ:
1. Introduction
2. Chapter 1 - Python Basics
3. Chapter 2 - if-else and Flow Control
...
26. Appendix A - Installing Third-Party Packages
27. Appendix B - Answers to the Practice Questions
--------------------
```

## 🔧 Troubleshooting

| ปัญหา | สาเหตุ | วิธีแก้ |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'requests'` | ยังไม่ activate venv หรือยังไม่ติดตั้ง package | activate venv แล้วรัน `pip install -r requirements.txt` |
| `403 Forbidden` | เว็บบล็อก request ที่ไม่มี User-Agent | ใส่ header `User-Agent` ใน `requests.get()` |
| `AttributeError: 'NoneType' object has no attribute ...` | `find()` หา element ไม่เจอ คืนค่า `None` | ตรวจ selector ด้วย DevTools (F12) และเช็ค `if element:` ก่อนใช้ |
| ได้ผลลัพธ์ว่าง | โครงสร้าง HTML ของเว็บเปลี่ยน | เปิด DevTools ดู tag/class ใหม่แล้วแก้ selector |

## Source

- Automate the Boring Stuff with Python, Chapter 13: Web Scraping: <https://automatetheboringstuff.com/3e/>
