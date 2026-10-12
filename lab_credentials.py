"""Persist lab bearer token and org ID from the Setup module (stored under data/, gitignored)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CREDENTIALS_PATH = ROOT / "data" / "lab_credentials.json"

_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.I,
)


def _load_raw() -> dict:
    if not CREDENTIALS_PATH.is_file():
        return {}
    try:
        data = json.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _save_raw(data: dict) -> None:
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CREDENTIALS_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def get_stored_token() -> str:
    return str(_load_raw().get("token") or "").strip()


def get_stored_org_id() -> str:
    return str(_load_raw().get("org_id") or "").strip()


def has_token() -> bool:
    token = get_stored_token()
    return bool(token and token != "your_bearer_token_here")


def has_org_id() -> bool:
    org_id = get_stored_org_id()
    return bool(org_id and org_id != "your_org_id_here" and _UUID_RE.match(org_id))


def is_fully_configured() -> bool:
    return has_token() and has_org_id()


def save_token(token: str, auth_method: str | None = None) -> None:
    data = _load_raw()
    data["token"] = token.strip()
    if auth_method:
        data["auth_method"] = str(auth_method).strip()
    _save_raw(data)


def save_org_id(org_id: str) -> None:
    data = _load_raw()
    data["org_id"] = org_id.strip()
    _save_raw(data)


def get_auth_method() -> str:
    method = str(_load_raw().get("auth_method") or "").strip().lower()
    if method in ("bearer", "integration"):
        return method
    return "bearer" if has_token() else ""


def get_integration_client_id() -> str:
    return str(_load_raw().get("integration_client_id") or "").strip()


def save_integration_client_id(client_id: str) -> None:
    data = _load_raw()
    value = (client_id or "").strip()
    if value:
        data["integration_client_id"] = value
    else:
        data.pop("integration_client_id", None)
    _save_raw(data)


def get_suggested_org_id() -> str:
    return str(_load_raw().get("suggested_org_id") or "").strip()


def save_suggested_org_id(org_id: str) -> None:
    data = _load_raw()
    value = (org_id or "").strip()
    if value:
        data["suggested_org_id"] = value
    else:
        data.pop("suggested_org_id", None)
    _save_raw(data)


def clear_credentials() -> None:
    if CREDENTIALS_PATH.is_file():
        CREDENTIALS_PATH.unlink()
