from strength import check_password
from generator import generate_password, generate_passphrase

from brute_force_estimation import (
    calculate_estimate,
    estimate_all,
    format_time,
    full_crack_analysis
)


# ============================================================
# BANNER
# ============================================================

def banner():

    print("\n" + "=" * 65)
    print("                         PASSTESTER")
    print("                  PASSWORD SECURITY TOOL")
    print("=" * 65)


# ============================================================
# TEST PASSWORD
# ============================================================

def test_password():

    password = input("\nEnter password to test: ")

    score, strength, feedback = check_password(password)

    print("\n" + "-" * 65)
    print("                    PASSWORD ANALYSIS")
    print("-" * 65)

    print(f"Length          : {len(password)}")
    print(f"Score           : {score}/10")
    print(f"Strength        : {strength}")

    if feedback:

        print("\nRecommendations:")

        for item in feedback:
            print(f"  [!] {item}")

    else:

        print("\n[+] No basic weaknesses detected.")

    print("-" * 65)


# ============================================================
# PASSWORD GENERATOR
# ============================================================

def password_generator():

    print("\n" + "-" * 65)
    print("                   PASSWORD GENERATOR")
    print("-" * 65)

    print("\n1. Random Password")
    print("2. Passphrase")

    choice = input("\nSelect option: ")

    if choice == "1":

        try:

            length = int(input("Enter password length: "))

            if length < 8:

                print("[!] Use a length of at least 8.")
                return

            password = generate_password(length)

            print("\n[+] Generated Password:")
            print(password)

        except ValueError:

            print("[!] Please enter a valid number.")

    elif choice == "2":

        try:

            words = int(input("Number of words (3-8): "))

            if words < 3 or words > 8:

                print("[!] Choose between 3 and 8 words.")
                return

            passphrase = generate_passphrase(words)

            print("\n[+] Generated Passphrase:")
            print(passphrase)

        except ValueError:

            print("[!] Please enter a valid number.")

    else:

        print("[!] Invalid option.")


# ============================================================
# Brute-Froce_EStimation- ANALYZER
# ============================================================

def brute_force_estimator():

    print("\n" + "-" * 65)
    print("                 Brute-Froce-Estimation-ANALYSIS")
    print("-" * 65)

    password = input("\nEnter password to analyze: ")

    analysis = full_crack_analysis(password)

    brute = analysis["brute_force"]
    realistic = analysis["realistic"]
    common = analysis["common"]
    patterns = analysis["patterns"]

    if brute is None:

        print("[!] Unable to analyze password.")
        return

    # --------------------------------------------------------
    # PASSWORD INFORMATION
    # --------------------------------------------------------

    print("\n" + "-" * 65)
    print("                    PASSWORD INFORMATION")
    print("-" * 65)

    print(f"Password length      : {len(password)}")
    print(f"Character set        : {brute['charset']}")

    print(
        "Character types      : "
        + ", ".join(brute["character_types"])
    )

    print(
        f"Possible combinations: "
        f"{brute['combinations']:,}"
    )

    print(
        f"Approx. entropy      : "
        f"{brute['entropy']:.2f} bits"
    )

    # --------------------------------------------------------
    # COMMON PASSWORD
    # --------------------------------------------------------

    print("\n" + "-" * 65)
    print("                  COMMON PASSWORD CHECK")
    print("-" * 65)

    if common["found"]:

        print("Result               : FOUND")
        print(f"Risk                 : {common['rank']}")
        print(
            f"Estimated position  : "
            f"Top {common['estimated_guesses']} guesses"
        )

    else:

        print("Result               : NOT FOUND")
        print(f"Status               : {common['rank']}")

    # --------------------------------------------------------
    # PATTERN ANALYSIS
    # --------------------------------------------------------

    print("\n" + "-" * 65)
    print("                     PATTERN ANALYSIS")
    print("-" * 65)

    if patterns:

        print("Patterns detected    : YES")

        for pattern in patterns:

            print(f"  [!] {pattern}")

    else:

        print("Patterns detected    : NO")

    # --------------------------------------------------------
    # REALISTIC ATTACK
    # --------------------------------------------------------

    print("\n" + "-" * 65)
    print("                 REAL-WORLD ATTACK MODEL")
    print("-" * 65)

    if realistic:

        print(
            f"Most likely attack  : "
            f"{realistic['attack']}"
        )

        print(
            f"Estimated time      : "
            f"{realistic['time']}"
        )

        print(
            f"Risk                : "
            f"{realistic['risk']}"
        )

        print(
            f"Confidence          : "
            f"{realistic['confidence']}"
        )

        print(
            f"Reason              : "
            f"{realistic['reason']}"
        )

    # --------------------------------------------------------
    # THEORETICAL ATTACK TIMES
    # --------------------------------------------------------

    print("\n" + "-" * 65)
    print("                THEORETICAL ATTACK TIMES")
    print("-" * 65)

    results = estimate_all(password)

    for name, data in results.items():

        print(f"\n{name}")

        print(
            f"  Guessing rate : "
            f"{data['rate']:,} guesses/second"
        )

        print(
            f"  Time          : "
            f"{format_time(data['seconds'])}"
        )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 65)
    print("                     FINAL ASSESSMENT")
    print("=" * 65)

    if realistic:

        print(
            f"Crackability       : "
            f"{realistic['risk']}"
        )

        print(
            f"Likely attack      : "
            f"{realistic['attack']}"
        )

        print(
            f"Estimated time     : "
            f"{realistic['time']}"
        )

    print("\n[!] This is a risk estimate, not a guaranteed")
    print("    real-world cracking time.")
    print("[!] No password cracking is performed.")
    print("=" * 65)


# ============================================================
# GRADE
# ============================================================

def get_grade(score):

    if score >= 9:
        return "A+"

    elif score >= 8:
        return "A"

    elif score >= 7:
        return "B"

    elif score >= 5:
        return "C"

    elif score >= 3:
        return "D"

    else:
        return "F"


# ============================================================
# PASSWORD HEALTH REPORT
# ============================================================

def password_health_report():

    print("\n" + "=" * 65)
    print("                  PASSWORD HEALTH REPORT")
    print("=" * 65)

    password = input("\nEnter password for full report: ")

    # --------------------------------------------------------
    # STRENGTH
    # --------------------------------------------------------

    score, strength, feedback = check_password(password)

    # --------------------------------------------------------
    # CRACK ANALYSIS
    # --------------------------------------------------------

    analysis = full_crack_analysis(password)

    brute_result = analysis["brute_force"]
    realistic = analysis["realistic"]
    common = analysis["common"]
    patterns = analysis["patterns"]

    grade = get_grade(score)

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    print("\n" + "=" * 65)
    print("                    PASSTESTER REPORT")
    print("=" * 65)

    print("\nPASSWORD INFORMATION")
    print("-" * 65)

    print(f"Length             : {len(password)} characters")
    print(f"Strength           : {strength}")
    print(f"Score              : {score}/10")
    print(f"Security Grade     : {grade}")

    # --------------------------------------------------------
    # CHARACTER ANALYSIS
    # --------------------------------------------------------

    print("\nCHARACTER ANALYSIS")
    print("-" * 65)

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_number = any(c.isdigit() for c in password)
    has_symbol = any(
        c in "!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        for c in password
    )

    print(
        f"Lowercase          : "
        f"{'YES' if has_lower else 'NO'}"
    )

    print(
        f"Uppercase          : "
        f"{'YES' if has_upper else 'NO'}"
    )

    print(
        f"Numbers            : "
        f"{'YES' if has_number else 'NO'}"
    )

    print(
        f"Special Characters : "
        f"{'YES' if has_symbol else 'NO'}"
    )

    # --------------------------------------------------------
    # ENTROPY
    # --------------------------------------------------------

    if brute_result:

        print("\nENTROPY ANALYSIS")
        print("-" * 65)

        print(
            f"Entropy            : "
            f"{brute_result['entropy']:.2f} bits"
        )

        print(
            f"Possible combinations: "
            f"{brute_result['combinations']:,}"
        )

    # --------------------------------------------------------
    # COMMON PASSWORD
    # --------------------------------------------------------

    print("\nCOMMON PASSWORD ANALYSIS")
    print("-" * 65)

    if common["found"]:

        print("Status             : FOUND")
        print("Risk               : CRITICAL")
        print("Attack             : Common-password attack")
        print("Estimated time     : Less than 1 second")

    else:

        print("Status             : NOT FOUND")
        print("Risk               : No basic common match")

    # --------------------------------------------------------
    # PATTERN ANALYSIS
    # --------------------------------------------------------

    print("\nPATTERN ANALYSIS")
    print("-" * 65)

    if patterns:

        for pattern in patterns:

            print(f"[!] {pattern}")

    else:

        print("[+] No obvious simple patterns detected.")

    # --------------------------------------------------------
    # REALISTIC CRACK TIME
    # --------------------------------------------------------

    print("\nREALISTIC CRACK-TIME ANALYSIS")
    print("-" * 65)

    if realistic:

        print(
            f"Likely attack      : "
            f"{realistic['attack']}"
        )

        print(
            f"Estimated time     : "
            f"{realistic['time']}"
        )

        print(
            f"Risk               : "
            f"{realistic['risk']}"
        )

        print(
            f"Confidence         : "
            f"{realistic['confidence']}"
        )

        print(
            f"Reason             : "
            f"{realistic['reason']}"
        )

    # --------------------------------------------------------
    # THEORETICAL BRUTE FORCE
    # --------------------------------------------------------

    print("\nTHEORETICAL BRUTE-FORCE")
    print("-" * 65)

    results = estimate_all(password)

    for name, data in results.items():

        print(
            f"{name:<22}: "
            f"{format_time(data['seconds'])}"
        )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    print("\nSECURITY RECOMMENDATIONS")
    print("-" * 65)

    if feedback:

        for item in feedback:

            print(f"[!] {item}")

    else:

        print("[+] No basic weaknesses detected.")

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    print("\n" + "=" * 65)
    print("                     OVERALL RESULT")
    print("=" * 65)

    if realistic:

        risk = realistic["risk"]

        if risk == "CRITICAL":

            print("Status             : CRITICAL")

        elif risk == "VERY HIGH":

            print("Status             : VERY HIGH RISK")

        elif risk == "HIGH":

            print("Status             : HIGH RISK")

        elif risk == "MEDIUM":

            print("Status             : MODERATE RISK")

        elif risk == "LOW":

            print("Status             : LOW RISK")

        else:

            print("Status             : VERY LOW RISK")

    print(
        f"Security Grade     : {grade}"
    )

    print("=" * 65)


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        banner()

        print("\n1. Test Password")
        print("2. Generate Password")
        print("3. Brute-Froce-Estimation Analysis")
        print("4. Password Health Report")
        print("5. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":

            test_password()

        elif choice == "2":

            password_generator()

        elif choice == "3":

            brute_force_estimator()

        elif choice == "4":

            password_health_report()

        elif choice == "5":

            print("\n[*] PassTester closed.")
            break

        else:

            print("\n[!] Invalid option.")

        input("\nPress ENTER to continue...")


if __name__ == "__main__":

    main()
