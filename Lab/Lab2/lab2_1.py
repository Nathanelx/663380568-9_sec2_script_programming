#แก้ไขโค้ดนี้ให้ถูกต้อง

num = int(input("Enter a number: "))

if num > 0:
    sign = "บวก"
elif num < 0:
    sign = "ลบ"
else:
    sign = "ศูนย์"

if num % 2 == 0:
    parity = "คู่"
else:
    parity = "คี่"

print(f"ตรวจสอบเลข {num} เป็น {sign}")
print(f"เลข {num} เป็นเลข {parity}")
print(f"{num} ผลลัพธ์เป็น{sign} และเป็นเลข {parity}")