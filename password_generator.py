import secrets
import string


def generate_strong_password(length: int=16) -> str:
    if length < 12:
        length=12

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = '!@#$%^&*()-_=+[]{};:,.?' 
    all_chars = lower + upper + digits + symbols

    password = [
        secrets.choice(lower),
        secrets.choice(upper),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]
    password += [secrets.choice(all_chars) for _ in range(length-4)]
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)   