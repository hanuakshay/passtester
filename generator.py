import secrets
import string


def generate_password(length=16, use_symbols=True):
    characters = string.ascii_letters + string.digits

    if use_symbols:
        characters += string.punctuation

    password = ""

    for _ in range(length):
        password += secrets.choice(characters)

    return password


def generate_passphrase(words=4):
    word_list = [
        "river",
        "mountain",
        "cloud",
        "forest",
        "planet",
        "tiger",
        "rocket",
        "ocean",
        "shadow",
        "silver",
        "thunder",
        "dragon",
        "sunset",
        "castle",
        "winter"
    ]

    selected = [
        secrets.choice(word_list)
        for _ in range(words)
    ]

    return "-".join(selected)
