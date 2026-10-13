# --- Lab 6.2 Part 1: Custom Module ---
# โมดูลที่เขียนเอง นำไป import ใช้ใน main_program.py


def greet(name):
    """Print a greeting message for the given name."""
    print(f"Hello, {name}!")


def is_prime(number):
    """Return True if number is a prime number, False otherwise."""
    if number < 2:
        return False
    i = 2
    while i * i <= number:          # เช็คตัวหารถึงแค่ราก number ก็พอ
        if number % i == 0:
            return False
        i += 1
    return True
