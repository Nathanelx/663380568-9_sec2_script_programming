# Class Activity 3: Web API Data Fetcher CLI

Week 10: **Interacting with Web APIs: Fetching and Processing JSON Data**

โปรแกรม CLI ที่ใช้ไลบรารี `requests` ส่ง HTTP **GET** ไปยัง Web API ฟรีสำหรับทดสอบ
[JSONPlaceholder](https://jsonplaceholder.typicode.com/) แล้วแปลงข้อมูล **JSON** เป็น dict / list ของ Python มาแสดงผล
พร้อมจัดการข้อผิดพลาดด้านเครือข่ายและ HTTP status

## ✨ เมนู

| เมนู | Endpoint | แสดงผล |
| --- | --- | --- |
| 1. ดึงข้อมูลงานเดี่ยว (Fetch Single TODO) | `GET /todos/{id}` | ID, User ID, หัวข้อ, สถานะ |
| 2. ดึงรายการโพสต์ทั้งหมด (Fetch All Posts) | `GET /posts` | 5 โพสต์แรก (จากทั้งหมด 100) |
| 3. ดึงรายการ TODO ตามรหัสผู้ใช้ (Fetch User TODOs) | `GET /todos?userId={id}` | งานทั้งหมดของผู้ใช้ + สรุปเสร็จ/ค้าง |
| 4. ออกจากโปรแกรม (Exit) | - | - |

## 📂 โครงสร้างโปรเจกต์

```text
my-api-fetcher/
├── src/
│   ├── __init__.py       # ทำให้ src เป็น Python package
│   └── api_client.py     # คลาส APIClient: ส่ง GET request + แปลง JSON + จัดการ error
├── main.py               # เมนู CLI และแสดงผลข้อมูล
├── requirements.txt      # requests==2.32.3
├── .gitignore
└── README.md
```

## 🔁 การทำงานของ `APIClient._make_request()`

```text
url = BASE_URL + endpoint
response = requests.get(url, timeout=10)   # ส่ง HTTP GET
response.raise_for_status()                # 4xx / 5xx → HTTPError
return response.json()                     # JSON → dict / list
```

| ข้อผิดพลาด | Exception | ตัวอย่าง |
| --- | --- | --- |
| Server ตอบ 4xx / 5xx | `requests.exceptions.HTTPError` | TODO ID `999999` → 404 Not Found |
| เชื่อมต่อไม่ได้ / domain ผิด / ไม่มีเน็ต | `requests.exceptions.ConnectionError` | `http://nonexistent-api-domain.invalid` |
| ตอบช้าเกิน 10 วินาที | `requests.exceptions.Timeout` | เซิร์ฟเวอร์ช้า |
| ข้อผิดพลาดอื่นของ requests | `requests.exceptions.RequestException` | URL ผิดรูปแบบ |
| ข้อมูลที่ได้ไม่ใช่ JSON | `json.JSONDecodeError` | ได้หน้า HTML กลับมา |
| พิมพ์ ID ไม่ใช่ตัวเลข / ติดลบ | `ValueError` (ใน `main.py`) | `abc`, `-1` |

ทุกกรณีจะแสดงข้อความ `[ERROR] ...` และคืนค่า `None` โปรแกรมไม่ crash

## 🚀 วิธีรัน

```powershell
cd "Class activity\Class activity 3\my-api-fetcher"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

> ต้องต่ออินเทอร์เน็ต เพราะดึงข้อมูลจาก `jsonplaceholder.typicode.com`

## ✅ ผลลัพธ์ (เมนู 2)

```text
กรุณาเลือกเมนู (1-4): 2
[INFO] กำลังส่งคำขอ (GET) ไปที่: https://jsonplaceholder.typicode.com/posts

📝 --- แสดง 5 รายการแรก (จากทั้งหมด 100 รายการ) ---

[1] Post ID: 1 | User ID: 1
    หัวข้อ (Title): sunt aut facere repellat provident occaecati excepturi optio reprehenderit
    เนื้อหา (Body) : quia et suscipit suscipit recusandae consequuntur expedita e...
...
... และยังมีอีก 95 โพสต์ที่ไม่ได้แสดงบนหน้าจอ
```

เมนู 3 (User ID 2):

```text
📋 --- รายการงาน TODO ทั้งหมดของ User ID 2 (รวม 20 รายการ) ---
  [021] ⏳ suscipit repellat esse quibusdam voluptatem incidunt
  [022] ✅ distinctio vitae autem nihil ut molestias quo
  ...
สรุป: เสร็จแล้ว 8/20 งาน | รอดำเนินการ 12 งาน
```

## 🐞 Debugging ใน VS Code

1. วาง breakpoint ที่ `client = APIClient()` ใน `main.py` และที่ `response = requests.get(url, timeout=timeout)` ใน `src/api_client.py`
2. ไปที่ **Run and Debug** แล้วกด **Python File**
3. เมื่อหยุดที่ `requests.get(...)` กด **Step Over (F10)** แล้วกางดู `response` ในหน้าต่าง **Variables**
   - `status_code` = `200`, `ok` = `True`, `text` = JSON ดิบ
4. ทดสอบ error: ใส่ TODO ID `999999` จะเข้า `except HTTPError` (404)
   หรือแก้ `BASE_URL` เป็น domain ที่ไม่มีจริงจะเข้า `except ConnectionError`
5. หลัง `response.json()` ลองดูโครงสร้าง list / dict ที่ได้ เช่น `posts[0]['title']`

## 🔧 Troubleshooting

| ปัญหา | วิธีแก้ |
| --- | --- |
| `ModuleNotFoundError: No module named 'requests'` | activate `.venv` แล้วรัน `pip install -r requirements.txt` |
| `Connection Error` | ตรวจการเชื่อมต่ออินเทอร์เน็ต |
| ภาษาไทย / emoji แสดงเพี้ยน | ใช้ terminal ของ VS Code (โปรแกรมตั้ง UTF-8 ให้อัตโนมัติบน Windows) |
