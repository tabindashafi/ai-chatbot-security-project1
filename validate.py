
import re

# Layer 1: Input validation
MAX_PROMPT_LENGTH = 500


def validate_input(prompt):
    if not isinstance(prompt, str):
        return False, "Prompt must be text."

    if not prompt.strip():
        return False, "Prompt cannot be empty."

    if len(prompt) > MAX_PROMPT_LENGTH:
        return False, "Prompt exceeds 500 characters."

    return True, "Input accepted."


# Layer 2: Regex-based prompt injection detection
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior)\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(your\s+)?(system|developer)\s+prompt",
    r"show\s+(me\s+)?(your\s+)?system\s+prompt",
    r"override\s+(your\s+)?instructions",
    r"act\s+as\s+if\s+you\s+have\s+no\s+restrictions",
]

# Long Base64-like strings
BASE64_PATTERN = r"\b[A-Za-z0-9+/]{100,}={0,2}\b"


def detect_injection(prompt):
    text = prompt.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True, "Known prompt injection pattern detected."

    if re.search(BASE64_PATTERN, prompt):
        return True, "Suspicious long Base64-like string detected."

    return False, "No known injection pattern detected."


# Layer 3: Output scanning
OUTPUT_PATTERNS = [
    r"system\s+prompt",
    r"developer\s+instructions",
    r"password\s*=",
    r"api[_-]?key\s*=",
    r"token\s*=",
]

URL_PATTERN = r"https?://[^\s]+"

def scan_output(response):
    for pattern in OUTPUT_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            return True, "Potential sensitive information disclosure detected."

    if re.search(URL_PATTERN, response, re.IGNORECASE):
        return True, "URL detected for review."

    return False, "No suspicious output pattern detected."
