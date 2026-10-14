# --- Activity 6.1: Refactoring a Previous Lab Assignment ---
# Refactor จาก Week 2 (lab2_1.py: Number Classifier และ lab2_2.py: Movie by Age)
# แยก logic ออกเป็นฟังก์ชัน ให้อ่านง่ายและนำกลับมาใช้ซ้ำได้


# ----- lab2_1: Number Classifier -----
def is_positive_negative_zero(num):
    """Return "บวก", "ลบ" or "ศูนย์" depending on the sign of num."""
    if num > 0:
        return "บวก"
    elif num < 0:
        return "ลบ"
    return "ศูนย์"


def is_even_odd(num):
    """Return "คู่" if num is even, otherwise "คี่"."""
    return "คู่" if num % 2 == 0 else "คี่"


def classify_number(num):
    """Return (sign, parity) of num as a tuple."""
    return is_positive_negative_zero(num), is_even_odd(num)


# ----- lab2_2: Movie Recommendation by Age -----
def movie_rating_for_age(age):
    """Return the suitable movie rating message for the given age."""
    if age < 5:
        return "You're too young for movies! Enjoy cartoons."
    elif age <= 12:
        return "G-rated or PG-rated movies."
    elif age <= 17:
        return "PG-13 or R-rated (with parental guidance)."
    return "Any movie rating."


def recommend_action(likes_action):
    """Return an extra recommendation if the user likes action movies."""
    if likes_action == "yes":
        return "You might enjoy the latest action blockbuster!"
    return None


# ----- Helper -----
def get_int(prompt):
    """Ask the user for an integer until a valid one is entered."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def run_number_classifier():
    num = get_int("Enter a number: ")
    sign, parity = classify_number(num)
    print(f"ตรวจสอบเลข {num} เป็น {sign}")
    print(f"เลข {num} เป็นเลข {parity}")
    print(f"{num} ผลลัพธ์เป็น{sign} และเป็นเลข {parity}")


def run_movie_recommender():
    age = get_int("Enter your age: ")
    print(movie_rating_for_age(age))
    if age >= 18:
        like = input("Do you like action movies? (yes/no): ").strip().lower()
        extra = recommend_action(like)
        if extra:
            print(extra)


def main():
    while True:
        print("\n1. Number Classifier (Lab 2.1)")
        print("2. Movie Recommender (Lab 2.2)")
        print("3. Exit")
        choice = input("Choose (1-3): ").strip()
        if choice == "1":
            run_number_classifier()
        elif choice == "2":
            run_movie_recommender()
        elif choice == "3":
            print("Bye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
