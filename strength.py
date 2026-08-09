import string
import math


def check_password(password):
    score = 0
    feedback = []

    # 1. Length - maximum 3 points
    if len(password) >= 16:
        score += 3
    elif len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    # 2. Lowercase - 1 point
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    # 3. Uppercase - 1 point
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    # 4. Numbers - 1 point
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers.")

    # 5. Special characters - 1 point
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Add special characters.")

    # 6. Repeated characters - 1 point
    repeated = False

    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            repeated = True
            break

    if not repeated:
        score += 1
    else:
        feedback.append("Avoid repeated characters.")

    # 7. Common password - 1 point
    common = [
        "password",
        "password123",
        "123456",
        "12345678",
        "qwerty",
        "admin",
        "welcome",
        "letmein"
    ]

    if password.lower() not in common:
        score += 1
    else:
        feedback.append("This is a commonly used password.")

    # Make sure score stays between 0 and 10
    score = max(0, min(score, 10))

    # Strength rating
    if score <= 2:
        strength = "VERY WEAK"
    elif score <= 4:
        strength = "WEAK"
    elif score <= 6:
        strength = "MODERATE"
    elif score <= 8:
        strength = "STRONG"
    else:
        strength = "VERY STRONG"

    return score, strength, feedback


def calculate_entropy(password):
    """Calculate approximate password entropy."""

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)

    if charset == 0:
        return 0

    return len(password) * math.log2(charset)


def brute_force_estimate(password):
    """Estimate guessing time only. Does not perform password cracking."""

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)

    if charset == 0:
        return 0

    combinations = charset ** len(password)

    # Example offline attack rate for estimation
    guesses_per_second = 10_000_000_000

    seconds = combinations / guesses_per_second

    return seconds
