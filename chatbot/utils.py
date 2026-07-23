"""
General utility functions used across the chatbot.
"""

from datetime import datetime


# ============================================================
# DIVIDER
# ============================================================

def divider(length=70):

    return "=" * length


# ============================================================
# CURRENT TIME
# ============================================================

def current_timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ============================================================
# PRINT TITLE
# ============================================================

def print_title(title):

    print()

    print(divider())

    print(title)

    print(divider())


# ============================================================
# PRINT SUCCESS
# ============================================================

def success(message):

    print(f"✓ {message}")


# ============================================================
# PRINT WARNING
# ============================================================

def warning(message):

    print(f"⚠ {message}")


# ============================================================
# PRINT ERROR
# ============================================================

def error(message):

    print(f"✗ {message}")


# ============================================================
# PRINT INFO
# ============================================================

def info(message):

    print(f"• {message}")


# ============================================================
# TRUNCATE LONG TEXT
# ============================================================

def truncate(

    text,

    length=300

):

    if not text:

        return ""

    if len(text) <= length:

        return text

    return text[:length] + "..."


# ============================================================
# FORMAT SIMILARITY SCORE
# ============================================================

def format_similarity(score):

    return f"{score:.3f}"


# ============================================================
# SAFE STRING
# ============================================================

def safe_string(value):

    if value is None:

        return ""

    return str(value).strip()