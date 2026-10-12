"""Check .env token formatting and WxCC API connectivity (does not print secrets)."""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import requests
from dotenv import load_dotenv

load_dotenv(ROOT / ".env", override=True)

from config import get_org_config_status, get_webex_bearer_token, get_webex_org_id

status = get_org_config_status()
token = get_webex_bearer_token()
org = get_webex_org_id()
base = status["wxcc_org_base_url"].rstrip("/")

print("=== Token checks ===")
print(f"configured: {bool(token and token != 'your_bearer_token_here')}")
print(f"length: {len(token)}")
print(f"stripped_length: {len(token.strip())}")
print(f"looks_like_jwt: {token.count('.') >= 2}")
print(f"has_bearer_prefix: {token.strip().lower().startswith('bearer ')}")
print(f"has_wrapping_quotes: {token[:1] in '\"' or token[-1:] in '\"'}")

print("\n=== Org checks ===")
print(f"org_id (.env): {org}")
print(f"org_id (token suffix): {status.get('token_org_id')}")
print(f"org_id_mismatch: {status.get('org_id_mismatch')}")
print(f"valid_uuid: {bool(re.match(r'^[0-9a-f-]{36}$', org or '', re.I))}")
if status.get("org_id_mismatch"):
    print(
        "\nWARNING: WEBEX_ORG_ID does not match the org embedded in your bearer token. "
        "API calls will use WEBEX_ORG_ID from .env — update it to match the token's org."
    )

headers = {"Authorization": f"Bearer {token.strip()}", "Content-Type": "application/json"}
url = f"{base}/{org}/v2/user"
print(f"\n=== API probe ===")
print(f"url: {url}")
try:
    response = requests.get(url, headers=headers, timeout=30)
    print(f"status: {response.status_code}")
    if response.status_code >= 400:
        print(f"body: {response.text[:500]}")
    else:
        data = response.json()
        key = next((k for k in data if isinstance(data.get(k), list)), None)
        count = len(data.get(key, [])) if key else "unknown"
        print(f"success: user list key={key!r}, count={count}")
except Exception as exc:
    print(f"error: {exc}")

webex_url = "https://webexapis.com/v1/people"
print(f"\n=== Webex Platform probe (Module 4) ===")
print(f"url: {webex_url}")
print("required scope: spark:people_read")
try:
    response = requests.get(webex_url, headers=headers, params={"max": 1}, timeout=30)
    print(f"status: {response.status_code}")
    if response.status_code >= 400:
        print(f"body: {response.text[:400]}")
    else:
        print("people API accessible")
except Exception as exc:
    print(f"error: {exc}")
