
"""
HENNGE backend-recursion/004 challenge submitter.

Fill in EMAIL and GIST_URL below, then run:
    pip install requests
    python submit_challenge.py
"""

import hmac
import hashlib
import struct
import time
import json
import requests

# ---- Fill these in ----
EMAIL = "YOUR_EMAIL@example.com"
GIST_URL = "https://gist.github.com/YOUR_ACCOUNT/GIST_ID"
SOLUTION_LANGUAGE = "python"  # or "golang"
# ------------------------

ENDPOINT = "https://api.challenge.hennge.com/challenges/backend-recursion/004"
SECRET_SUFFIX = "HENNGECHALLENGE004"
TIME_STEP = 30
DIGITS = 10


def generate_totp(userid: str, timestamp: int = None) -> str:
    """RFC 6238 TOTP, using HMAC-SHA-512 and 10-digit output, T0=0."""
    if timestamp is None:
        timestamp = int(time.time())

    counter = timestamp // TIME_STEP  # T = (Current Unix time - T0) / X
    # Counter must be represented as an 8-byte big-endian integer (RFC 4226)
    counter_bytes = struct.pack(">Q", counter)

    shared_secret = (userid + SECRET_SUFFIX).encode("utf-8")

    # HMAC-SHA-512 instead of the default HMAC-SHA-1
    hmac_hash = hmac.new(shared_secret, counter_bytes, hashlib.sha512).digest()

    # Dynamic truncation (RFC 4226 section 5.3) - same procedure regardless
    # of the underlying hash algorithm/length; only the last 4 bytes chosen
    # via the offset nibble are used.
    offset = hmac_hash[-1] & 0x0F
    binary_code = (
        ((hmac_hash[offset] & 0x7F) << 24)
        | ((hmac_hash[offset + 1] & 0xFF) << 16)
        | ((hmac_hash[offset + 2] & 0xFF) << 8)
        | (hmac_hash[offset + 3] & 0xFF)
    )

    otp = binary_code % (10 ** DIGITS)
    return str(otp).zfill(DIGITS)


def main():
    if "YOUR_EMAIL" in EMAIL or "YOUR_ACCOUNT" in GIST_URL:
        print("Please fill in EMAIL and GIST_URL before running this script.")
        return

    payload = {
        "github_url": GIST_URL,
        "contact_email": EMAIL,
        "solution_language": SOLUTION_LANGUAGE,
    }

    otp = generate_totp(EMAIL)

    print(f"Generated TOTP: {otp}")
    print(f"Payload: {json.dumps(payload)}")

    response = requests.post(
        ENDPOINT,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        auth=(EMAIL, otp),
    )

    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")


if __name__ == "__main__":
    main()
