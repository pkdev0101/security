import re

def check_password_strength(password):
    length_error = len(password) < 12
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    digit_error = re.search(r"\d", password) is None
    special_char_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None

    if length_error:
        return "Password must be at least 12 characters long."
    if uppercase_error:
        return "Password must include an uppercase letter."
    if lowercase_error:
        return "Password must include a lowercase letter."
    if digit_error:
        return "Password must include a number."
    if special_char_error:
        return "Password must include a special character."

    return "Strong Password ✅"

if __name__ == "__main__":
    pwd = input("Enter password: ")
    print(check_password_strength(pwd))
