# --- Lab 6.2 Part 2: Use the Custom Module and Standard Modules ---
import my_utils
import math
import random

# เรียกใช้ฟังก์ชันจากโมดูลที่เขียนเอง
my_utils.greet("Alice")

for n in [7, 10, 1, 13, 25, 97]:
    print(f"is_prime({n}) = {my_utils.is_prime(n)}")

# ใช้ math module
number = 144
print(f"Square root of {number} = {math.sqrt(number)}")
print(f"math.pi = {math.pi}")

# ใช้ random module
rand_num = random.randint(1, 100)
print(f"Random number between 1 and 100: {rand_num}")
print(f"Is {rand_num} prime? {my_utils.is_prime(rand_num)}")
