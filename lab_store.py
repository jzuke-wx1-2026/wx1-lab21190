"""Persist lab fill-in answers to disk so progress survives page reloads."""

from __future__ import annotations

import json
import re
from pathlib import Path

from config import FILL_IN_PLACEHOLDER

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
STORE_PATH = DATA_DIR / "lab_answers.json"

_VAR_NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")

# Module 1: get-by-id endpoints → list-all endpoints (Aug 2026 lab refresh)
_LEGACY_MODULE1_RENAMES: dict[str, tuple[str, str]] = {
    "USER_PROFILE_ENDPOINT": ("AGENT_PROFILE_LIST_ENDPOINT", "/{org_id}/v2/agent-profile"),
    "SKILL_PROFILE_ENDPOINT": ("SKILL_PROFILE_LIST_ENDPOINT", "/{org_id}/v2/skill-profile"),
    "TEAM_ENDPOINT": ("TEAM_LIST_ENDPOINT", "/{org_id}/v2/team"),
    "MULTIMEDIA_PROFILE_DETAIL_ENDPOINT": (
        "MULTIMEDIA_PROFILE_LIST_ENDPOINT",
        "/{org_id}/v2/multimedia-profile",
    ),
}


_LEGACY_DROP_KEYS = {
    "USERS_RESPONSE_DATA_KEY",
    "EP_RESPONSE_DATA_KEY",
    "QUEUE_RESPONSE_DATA_KEY",
    "TEAM_RESPONSE_DATA_KEY",
    "GV_RESPONSE_DATA_KEY",
    "FLOW_LIST_ENDPOINT",
    "FLOW_ID_KEY",
    "FLOW_NAME_KEY",
    "GV_ID_KEY",
    "GV_UPDATE_VALUE_KEY",
    "SEARCH_QUERY_TYPE_TASK",
    "SEARCH_QUERY_TYPE_AGENT",
    "SEARCH_RESPONSE_TASKS_KEY",
    "SEARCH_RESPONSE_AGENTS_KEY",
    "CSR_STATUS_KEY",
    # Module 4 — hardcoded or consolidated (Aug 2026)
    "PEOPLE_LOCATION_ID_KEY",
    "ROLE_ID_KEY",
    "ROLE_NAME_KEY",
    "LICENSE_ID_KEY",
    "LICENSE_NAME_KEY",
    "LOCATION_CALLING_ENABLED_KEY",
    "LOCATION_COUNTRY_KEY",
    "LOCATION_ADDRESS_LINE1_KEY",
    "LOCATION_CITY_KEY",
    "LOCATION_STATE_KEY",
    "LOCATION_POSTAL_CODE_KEY",
    "LOCATION_PHONE_LOCATION_ID_KEY",
    "LOCATION_DETAIL_ENDPOINT",
    "PSTN_TYPE_KEY",
    "PSTN_CARRIER_NAME_KEY",
}


_LEGACY_VAR_RENAMES: dict[str, tuple[str, str]] = {
    "EP_STATUS_KEY": ("EP_ACTIVE_KEY", "active"),
    "LOCATION_PHONE_NUMBERS_ENDPOINT": ("WEBEX_PHONE_NUMBERS_ENDPOINT", "/telephony/config/numbers"),
    "LOCATION_PHONE_NUMBER_KEY": ("PHONE_NUMBER_KEY", "phoneNumber"),
}


_LEGACY_ENDPOINT_OLD_PATHS: dict[str, tuple[str, ...]] = {
    "ENTRY_POINT_LIST_ENDPOINT": ("/{org_id}/entry-point",),
    "DIAL_NUMBER_LIST_ENDPOINT": ("/{org_id}/dial-number",),
    "QUEUE_LIST_ENDPOINT": ("/{org_id}/contact-service-queue",),
    "AUX_CODE_LIST_ENDPOINT": ("/{org_id}/auxiliary-code",),
}

_LEGACY_ENDPOINT_CANONICAL: dict[str, str] = {
    "ENTRY_POINT_LIST_ENDPOINT": "/{org_id}/v2/entry-point",
    "DIAL_NUMBER_LIST_ENDPOINT": "/{org_id}/v3/dial-number",
    "QUEUE_LIST_ENDPOINT": "/{org_id}/v2/contact-service-queue",
    "AUX_CODE_LIST_ENDPOINT": "/{org_id}/v2/auxiliary-code",
}


def _apply_legacy_renames(answers: dict[str, str]) -> dict[str, str]:
    migrated = dict(answers)
    changed = False
    for key in _LEGACY_DROP_KEYS:
        if key in migrated:
            migrated.pop(key, None)
            changed = True
    for old_key, (new_key, default_val) in _LEGACY_VAR_RENAMES.items():
        if old_key not in migrated:
            continue
        old_val = migrated.pop(old_key)
        if new_key not in migrated or migrated[new_key] in ("", FILL_IN_PLACEHOLDER):
            val = old_val if old_val not in ("", FILL_IN_PLACEHOLDER, "status") else default_val
            if val == "status":
                val = default_val
            migrated[new_key] = val
            changed = True
        else:
            changed = True
    for var, old_paths in _LEGACY_ENDPOINT_OLD_PATHS.items():
        canonical = _LEGACY_ENDPOINT_CANONICAL.get(var)
        if not canonical:
            continue
        current = migrated.get(var, "")
        if current in old_paths and current != canonical:
            migrated[var] = canonical
            changed = True
    for old_key, (new_key, list_default) in _LEGACY_MODULE1_RENAMES.items():
        old_val = migrated.get(old_key, FILL_IN_PLACEHOLDER)
        if old_val in ("", FILL_IN_PLACEHOLDER):
            migrated.pop(old_key, None)
            continue
        if new_key not in migrated or migrated[new_key] in ("", FILL_IN_PLACEHOLDER):
            if "{" in old_val and old_val.rsplit("/", 1)[-1].startswith("{"):
                migrated[new_key] = list_default
            else:
                migrated[new_key] = old_val
            changed = True
        migrated.pop(old_key, None)
        changed = True
    if changed:
        _save_raw(migrated)
    return migrated


def _normalize_value(value) -> str:
    if value is None:
        return FILL_IN_PLACEHOLDER
    text = str(value).strip()
    return text if text else FILL_IN_PLACEHOLDER


def _load_raw() -> dict[str, str]:
    if not STORE_PATH.is_file():
        return {}
    try:
        data = json.loads(STORE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {k: _normalize_value(v) for k, v in data.items() if _VAR_NAME_RE.match(k)}


def _save_raw(answers: dict[str, str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(answers, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_answers() -> dict[str, str]:
    return _apply_legacy_renames(_load_raw())


def get_answer(name: str, default: str = FILL_IN_PLACEHOLDER) -> str:
    return load_answers().get(name, default)


def merge_answers(updates: dict[str, str]) -> dict[str, str]:
    current = load_answers()
    for key, value in updates.items():
        if not _VAR_NAME_RE.match(key):
            continue
        current[key] = _normalize_value(value)
    _save_raw(current)
    return current


def clear_variables(variable_names: list[str]) -> dict[str, str]:
    """Remove saved answers for the given variables (e.g. reset a module)."""
    current = load_answers()
    for key in variable_names:
        if _VAR_NAME_RE.match(key):
            current.pop(key, None)
    _save_raw(current)
    return current


def answers_for_variables(variables: list[str]) -> dict[str, str]:
    stored = load_answers()
    return {var: stored.get(var, FILL_IN_PLACEHOLDER) for var in variables}
