import string
import math
import re


# ============================================================
# COMMON PASSWORDS
# ============================================================

COMMON_PASSWORDS = {
    "123456",
    "123456789",
    "12345678",
    "password",
    "password1",
    "password123",
    "1234567890",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "letmein",
    "welcome",
    "welcome123",
    "monkey",
    "dragon",
    "football",
    "iloveyou",
    "abc123",
    "000000",
    "111111",
    "123123",
    "654321",
    "passw0rd",
    "login",
    "secret",
    "master",
    "hello",
    "computer",
    "india",
    "india123",
}


# ============================================================
# CHARACTER SET ANALYSIS
# ============================================================

def get_character_set(password):

    charset = 0
    character_types = []

    if any(c.islower() for c in password):
        charset += 26
        character_types.append("Lowercase")

    if any(c.isupper() for c in password):
        charset += 26
        character_types.append("Uppercase")

    if any(c.isdigit() for c in password):
        charset += 10
        character_types.append("Numbers")

    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)
        character_types.append("Symbols")

    return charset, character_types


# ============================================================
# BASIC BRUTE FORCE CALCULATION
# ============================================================

def calculate_estimate(password, guesses_per_second):

    charset, character_types = get_character_set(password)

    if charset == 0 or len(password) == 0:
        return None

    combinations = charset ** len(password)

    # Average-case assumption:
    # attacker finds password halfway through search space.
    average_guesses = combinations / 2

    seconds = average_guesses / guesses_per_second

    entropy = len(password) * math.log2(charset)

    return {
        "charset": charset,
        "character_types": character_types,
        "combinations": combinations,
        "entropy": entropy,
        "seconds": seconds
    }


# ============================================================
# TIME FORMATTER
# ============================================================

def format_time(seconds):

    if seconds < 1:
        return "Less than 1 second"

    minutes = seconds / 60

    if minutes < 1:
        return f"{seconds:.2f} seconds"

    hours = minutes / 60

    if hours < 1:
        return f"{minutes:.2f} minutes"

    days = hours / 24

    if days < 1:
        return f"{hours:.2f} hours"

    years = days / 365.25

    if years < 1:
        return f"{days:.2f} days"

    if years < 1_000:
        return f"{years:.2f} years"

    if years < 1_000_000:
        return f"{years / 1_000:.2f} thousand years"

    if years < 1_000_000_000:
        return f"{years / 1_000_000:.2f} million years"

    if years < 1_000_000_000_000:
        return f"{years / 1_000_000_000:.2f} billion years"

    return f"{years / 1_000_000_000_000:.2f} trillion years"


# ============================================================
# COMMON PASSWORD DETECTION
# ============================================================

def check_common_password(password):

    password_lower = password.lower()

    if password_lower in COMMON_PASSWORDS:

        return {
            "found": True,
            "rank": "Extremely common",
            "estimated_guesses": 100
        }

    return {
        "found": False,
        "rank": "Not found in basic common-password list",
        "estimated_guesses": None
    }


# ============================================================
# SIMPLE DICTIONARY / WORD DETECTION
# ============================================================

def detect_dictionary_pattern(password):

    password_lower = password.lower()

    words = [
        "password",
        "admin",
        "welcome",
        "hello",
        "secret",
        "login",
        "qwerty",
        "football",
        "dragon",
        "monkey",
        "computer",
        "india",
        "love",
        "summer",
        "winter",
        "spring",
        "autumn",
        "master",
    ]

    for word in words:

        if password_lower == word:
            return True, word

        if password_lower.startswith(word):
            return True, word

        if password_lower.endswith(word):
            return True, word

    return False, None


# ============================================================
# PATTERN ANALYSIS
# ============================================================

def analyze_patterns(password):

    patterns = []

    # Sequential numbers
    if re.search(r"1234|2345|3456|4567|5678|6789", password):
        patterns.append("Sequential numbers")

    # Repeated characters
    if re.search(r"(.)\1\1", password):
        patterns.append("Repeated characters")

    # Keyboard patterns
    keyboard_patterns = [
        "qwerty",
        "asdf",
        "zxcv",
        "qaz",
        "wsx",
        "1234",
        "4321"
    ]

    password_lower = password.lower()

    for pattern in keyboard_patterns:

        if pattern in password_lower:
            patterns.append("Keyboard pattern")
            break

    # Year-like numbers
    if re.search(r"(19|20)\d{2}", password):
        patterns.append("Year pattern")

    # Common substitutions
    if re.search(r"[a@][s$][s$][w3][o0][r][d]", password_lower):
        patterns.append("Common character substitutions")

    return patterns


# ============================================================
# REALISTIC CRACK ANALYSIS
# ============================================================

def realistic_analysis(password):

    if not password:
        return None

    common = check_common_password(password)

    dictionary_found, dictionary_word = detect_dictionary_pattern(password)

    patterns = analyze_patterns(password)

    # --------------------------------------------------------
    # COMMON PASSWORD
    # --------------------------------------------------------

    if common["found"]:

        return {
            "attack": "Common Password",
            "time_seconds": common["estimated_guesses"] / 10_000,
            "time": "Less than 1 second",
            "risk": "CRITICAL",
            "confidence": "HIGH",
            "reason": "Password appears in the common-password database."
        }

    # --------------------------------------------------------
    # DICTIONARY WORD
    # --------------------------------------------------------

    if dictionary_found:

        return {
            "attack": "Dictionary Attack",
            "time_seconds": 2,
            "time": "A few seconds",
            "risk": "VERY HIGH",
            "confidence": "HIGH",
            "reason": f"Contains predictable word: '{dictionary_word}'."
        }

    # --------------------------------------------------------
    # PATTERN ATTACK
    # --------------------------------------------------------

    if patterns:

        return {
            "attack": "Pattern Attack",
            "time_seconds": 30,
            "time": "Seconds to minutes",
            "risk": "HIGH",
            "confidence": "MEDIUM",
            "reason": ", ".join(patterns)
        }

    # --------------------------------------------------------
    # PURE BRUTE FORCE
    # --------------------------------------------------------

    result = calculate_estimate(password, 10_000_000_000)

    if result:

        seconds = result["seconds"]

        if seconds < 1:
            risk = "HIGH"

        elif seconds < 60:
            risk = "MEDIUM"

        elif seconds < 365 * 24 * 60 * 60:
            risk = "LOW"

        else:
            risk = "VERY LOW"

        return {
            "attack": "Pure Brute Force",
            "time_seconds": seconds,
            "time": format_time(seconds),
            "risk": risk,
            "confidence": "LOW",
            "reason": "No obvious common-password or simple pattern detected."
        }

    return None


# ============================================================
# ATTACK SCENARIOS
# ============================================================

def estimate_all(password):

    scenarios = {

        # Online login systems are normally rate-limited.
        "Online Attack": 1,

        # Example fast offline hash scenario.
        "Offline - Moderate": 100_000,

        # Example very fast hash scenario.
        "Offline - High Speed": 10_000_000_000
    }

    results = {}

    for name, rate in scenarios.items():

        result = calculate_estimate(password, rate)

        if result:

            results[name] = {
                "rate": rate,
                "seconds": result["seconds"]
            }

    return results


# ============================================================
# FULL ANALYSIS
# ============================================================

def full_crack_analysis(password):

    brute = calculate_estimate(password, 10_000_000_000)

    realistic = realistic_analysis(password)

    common = check_common_password(password)

    patterns = analyze_patterns(password)

    return {
        "brute_force": brute,
        "realistic": realistic,
        "common": common,
        "patterns": patterns
    }
