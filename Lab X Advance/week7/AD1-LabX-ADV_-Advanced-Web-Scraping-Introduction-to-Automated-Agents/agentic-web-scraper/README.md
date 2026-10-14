# AD1 LabX ADV: Advanced Web Scraping & Introduction to Automated Agents

**Agentic Product Scraper** คือ scraper ที่ใช้ **Selenium** ควบคุมเบราว์เซอร์ และทำงานตาม "แผน" ในไฟล์ config (`configs/example_site_config.json`)
เหมือน agent ที่ทำงานเองได้: อ่าน config แล้วไปที่ URL เริ่มต้น ดึงข้อมูลสินค้า กดหน้าถัดไป และทำซ้ำจนครบจำนวนหน้า จากนั้นบันทึกเป็น JSON/CSV

เว็บไซต์เป้าหมาย: [Books to Scrape](https://books.toscrape.com/) เป็นเว็บจำลองที่ทำมาให้ฝึก scraping โดยเฉพาะ

## 🎯 สิ่งที่ได้ฝึก

- Scrape เว็บด้วย Selenium (`driver.get()`, `find_elements(By.CSS_SELECTOR, ...)`, `.click()`, `.text`)
- Waiting strategies: **implicit wait** (`implicitly_wait(10)`) และ **explicit wait** (`WebDriverWait` + `EC`)
- **Headless browser** (`--headless=new`) และ **User-Agent spoofing**
- **Retry mechanism** (`utils.retry`) และ **rate limiting** (`delay_between_pages`)
- จัดโครงสร้างข้อมูลด้วย `dataclass` (`Product`) แล้วบันทึกเป็น **JSON** และ **CSV**
- **Config-driven agent**: แก้ selector ใน config ไฟล์เดียวก็เปลี่ยนเว็บเป้าหมายได้โดยไม่ต้องแก้โค้ด

## 📂 โครงสร้างโปรเจกต์

```text
agentic-web-scraper/
├── configs/
│   └── example_site_config.json   # "แผน" ของ agent: URL, selector, จำนวนหน้า
├── data/
│   ├── scraped_products.json      # ผลลัพธ์ (JSON)
│   └── scraped_products.csv       # ผลลัพธ์ (CSV)
├── src/
│   ├── __init__.py
│   ├── config_parser.py           # อ่านและตรวจสอบ config
│   ├── data_models.py             # dataclass Product
│   ├── driver_manager.py          # สร้าง/ปิด WebDriver (Chrome/Firefox)
│   ├── scraper_agent.py           # ScraperAgent: automation loop
│   └── utils.py                   # save JSON/CSV, wait, safe_click, retry
├── main.py                        # จุดเริ่มต้นโปรแกรม
├── test_setup.py                  # ทดสอบว่า Selenium ใช้งานได้
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Config

```json
{
  "start_url": "https://books.toscrape.com/catalogue/category/books_1/index.html",
  "max_pages": 2,
  "delay_between_pages": 1,
  "max_retries": 3,
  "item_container_selector": "article.product_pod",
  "pagination_selector": "li.next a",
  "item_data_selectors": {
    "name": "h3 a",
    "price": "p.price_color",
    "description": null,
    "url": "h3 a",
    "image_url": "div.image_container a img"
  }
}
```

| Key | ความหมาย |
| --- | --- |
| `start_url` | หน้าแรกที่ agent จะเข้าไป |
| `max_pages` | จำนวนหน้าสูงสุดที่จะ scrape |
| `delay_between_pages` | หน่วงเวลา (วินาที) ระหว่างหน้า เพื่อไม่ให้เป็นภาระเซิร์ฟเวอร์ |
| `max_retries` | จำนวนครั้งที่ลองโหลดหน้าใหม่ถ้าล้มเหลว (ไม่ใส่ก็ได้ ค่าเริ่มต้น 3) |
| `item_container_selector` | selector ของกล่องสินค้า 1 ชิ้น |
| `pagination_selector` | selector ของปุ่ม "next" |
| `item_data_selectors` | selector ของแต่ละฟิลด์ (`null` = ไม่ดึงฟิลด์นั้น) |

## 🚀 วิธีรัน

> ต้องมี Google Chrome ติดตั้งในเครื่อง (`webdriver-manager` จะดาวน์โหลด ChromeDriver ให้อัตโนมัติ)

1. เข้าไปที่โฟลเดอร์โปรเจกต์

   ```powershell
   cd "Lab X Advance\week7\AD1-LabX-ADV_-Advanced-Web-Scraping-Introduction-to-Automated-Agents\agentic-web-scraper"
   ```

2. สร้างและเปิดใช้งาน virtual environment

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. ติดตั้ง dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. (แนะนำ) ทดสอบ Selenium ก่อน ถ้าขึ้น `Title: All products | Books to Scrape - Sandbox` แสดงว่าใช้ได้

   ```bash
   python test_setup.py
   ```

5. รัน agent

   ```bash
   python main.py
   ```

   ถ้าอยากเห็นเบราว์เซอร์ทำงานจริง ให้แก้ `headless=True` เป็น `headless=False` ใน `main.py`

## ✅ ผลลัพธ์ที่ได้

```text
Scraping page 1...
Scraping page 2...
Successfully scraped 40 items and saved to data\scraped_products.json and data\scraped_products.csv
```

ตัวอย่างใน `data/scraped_products.json`:

```json
[
    {
        "name": "A Light in the ...",
        "price": "£51.77",
        "description": null,
        "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
    },
    ...
]
```

## ⚖️ จริยธรรมและกฎหมาย

- ตรวจ `robots.txt` และ Terms of Service ก่อน scrape ทุกครั้ง
- Selenium ทำงานเหมือนผู้ใช้จริงและโหลดทุกอย่างในหน้า จึงเป็นภาระเซิร์ฟเวอร์มากกว่า `requests` ต้องหน่วงเวลาระหว่างหน้า (rate limiting)
- การ scrape หนักเกินไปอาจทำให้ถูกบล็อก IP หรือถูกดำเนินคดี (Cease and Desist)
- ถ้ามี API ให้ใช้ API แทน และใช้ข้อมูลเพื่อการศึกษาเท่านั้น

## 🔧 Troubleshooting

| ปัญหา | วิธีแก้ |
| --- | --- |
| `can't open file '...\main.py'` | ยังไม่ได้ `cd` เข้าโฟลเดอร์ `agentic-web-scraper` |
| `ModuleNotFoundError: No module named 'selenium'` / `'src'` | activate venv แล้วรัน `pip install -r requirements.txt` และรันจากในโฟลเดอร์โปรเจกต์ |
| `running scripts is disabled on this system` | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `SessionNotCreatedException` | อัปเดต Google Chrome เป็นเวอร์ชันล่าสุด |
| `TimeoutException` | เน็ตช้าหรือ selector ไม่ตรง ตรวจ selector ด้วย DevTools (F12) |
