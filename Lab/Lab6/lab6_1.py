# --- Lab 6.1: Simple Calculator Functions ---
# เครื่องคิดเลขแบบเมนู ใช้ฟังก์ชันแยกแต่ละการคำนวณ


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b (a - b)."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return a divided by b, or an error message if b is zero."""
    if b == 0:
        return "Error: Division by zero"
    return a / b


def power(base, exponent=2):
    """Return base raised to exponent (default exponent = 2, i.e. square)."""
    return base ** exponent


def get_number(prompt):
    """Ask the user for a number until a valid one is entered."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number, please try again.")


def show_menu():
    """Print the calculator menu."""
    print("\n===== Simple Calculator =====")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Exit")


def main():
    """Run the menu-driven calculator loop."""
    operations = {
        "1": ("+", add),
        "2": ("-", subtract),
        "3": ("*", multiply),
        "4": ("/", divide),
    }

    while True:
        show_menu()
        choice = input("Choose an operation (1-6): ").strip()

        if choice == "6":
            print("Goodbye!")
            break

        if choice in operations:
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            symbol, func = operations[choice]
            result = func(a, b)
            print(f"Result: {a} {symbol} {b} = {result}")

        elif choice == "5":
            base = get_number("Enter base: ")
            exp_text = input("Enter exponent (press Enter for default = 2): ").strip()
            if exp_text == "":
                result = power(base)            # ใช้ค่า default exponent=2
                print(f"Result: {base} ** 2 = {result}")
            else:
                try:
                    exponent = float(exp_text)
                except ValueError:
                    print("Invalid exponent.")
                    continue
                result = power(base, exponent)
                print(f"Result: {base} ** {exponent} = {result}")

        else:
            print("Invalid choice, please select 1-6.")


if __name__ == "__main__":
    main()
