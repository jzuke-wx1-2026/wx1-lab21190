"""Validate and persist Setup module credentials."""

from __future__ import annotations

import re

import requests

from config import get_webex_api_base_url, get_wxcc_org_base_url, org_id_from_token
from lab_credentials import (
    get_stored_token,
    save_integration_client_id,
    save_org_id,
    save_suggested_org_id,
    save_token,
)
from lab_ui import describe_field

_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.I,
)

WEBEX_AUTHORIZE_URL = "https://webexapis.com/v1/authorize"
WEBEX_TOKEN_URL = "https://webexapis.com/v1/access_token"
CREATE_INTEGRATION_URL = "https://developer.webex.com/my-apps/new"

# Scopes this lab actually calls. spark:kms is auto-granted by Webex and is not shown to participants.
INTEGRATION_SCOPES = [
    {"id": "cjp:config", "why": "Contact Center configuration APIs"},
    {"id": "cjp:config_read", "why": "Read users, queues, teams, and other org data"},
    {"id": "cjp:config_write", "why": "Update global variables (Module 2)"},
    {"id": "spark:people_read", "why": "Identify the authorizing admin and organization"},
    {"id": "spark:kms", "why": "Added automatically by Webex with people APIs — not a checkbox", "selectable": False},
    {"id": "spark-admin:people_read", "why": "List Control Hub people (Module 4)"},
    {"id": "spark-admin:roles_read", "why": "Resolve role names (Module 4)"},
    {"id": "spark-admin:licenses_read", "why": "Resolve license names (Module 4)"},
    {"id": "spark-admin:telephony_config_read", "why": "Locations and phone numbers (Module 4)"},
    {"id": "spark-admin:telephony_pstn_read", "why": "PSTN connection per location (Module 4 step 4.3)"},
]


def selectable_integration_scopes() -> list[dict]:
    return [item for item in INTEGRATION_SCOPES if item.get("selectable", True)]


def parse_granted_scopes(raw: str) -> set[str]:
    return {part.strip().lower() for part in (raw or "").replace(",", " ").split() if part.strip()}


def missing_required_scopes(granted_raw: str) -> list[str]:
    granted = parse_granted_scopes(granted_raw)
    return [item["id"] for item in selectable_integration_scopes() if item["id"].lower() not in granted]


def setup_callback_url(host_url: str) -> str:
    return host_url.rstrip("/") + "/setup/callback"


def oauth_setup_payload(host_url: str) -> dict:
    callback_url = setup_callback_url(host_url)
    from lab_credentials import get_auth_method, get_integration_client_id

    return {
        "callback_url": callback_url,
        "create_app_url": CREATE_INTEGRATION_URL,
        "scopes": selectable_integration_scopes(),
        "auth_method": get_auth_method(),
        "client_id": get_integration_client_id(),
    }


def _normalize_token(raw: str) -> str:
    token = (raw or "").strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    return token.strip('"').strip("'")


def _webex_error_message(response: requests.Response, fallback: str) -> str:
    try:
        payload = response.json()
    except ValueError:
        text = (response.text or "").strip()
        return f"{fallback} ({response.status_code}). {text[:200]}".strip()
    message = payload.get("message") or payload.get("error_description") or payload.get("error")
    if isinstance(message, str) and message.strip():
        return message.strip()
    errors = payload.get("errors")
    if isinstance(errors, list) and errors:
        first = errors[0]
        if isinstance(first, dict):
            return str(first.get("description") or first.get("message") or first)
        return str(first)
    return f"{fallback} ({response.status_code})"


def _probe_wxcc_users(token: str, org_id: str) -> tuple[bool, str]:
    base = get_wxcc_org_base_url().rstrip("/")
    url = f"{base}/{org_id}/v2/user"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
    except requests.RequestException as exc:
        return False, f"Could not reach WxCC API: {exc}"

    if response.status_code == 401:
        return False, "Token rejected (401). Sign in again and copy a fresh bearer token from your profile."
    if response.status_code == 403:
        return False, (
            "Access denied (403). Use a Webex Contact Center admin account — "
            "the token must include Contact Center configuration scopes "
            "(cjp:config, cjp:config_read, cjp:config_write)."
        )
    if response.status_code >= 400:
        body = response.text[:200].strip()
        return False, f"WxCC API returned {response.status_code}. {body}"

    return True, "Connected to your organization."


def _org_from_people_me(token: str) -> str | None:
    url = get_webex_api_base_url().rstrip("/") + "/people/me"
    try:
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=30)
    except requests.RequestException:
        return None
    if response.status_code >= 400:
        return None
    try:
        data = response.json()
    except ValueError:
        return None
    org_id = str(data.get("orgId") or "").strip()
    return org_id if _UUID_RE.match(org_id) else None


def exchange_integration_code(client_id: str, client_secret: str, code: str, redirect_uri: str) -> dict:
    """Exchange an OAuth authorization code for an access token. Does not store the client secret."""
    client_id = (client_id or "").strip()
    client_secret = (client_secret or "").strip()
    code = (code or "").strip()
    redirect_uri = (redirect_uri or "").strip()
    errors: list[dict] = []

    if not client_id:
        errors.append({"var": "SETUP_CLIENT_ID", "label": "Client ID", "hint": "Paste the Client ID from your Webex integration."})
    if not client_secret:
        errors.append({"var": "SETUP_CLIENT_SECRET", "label": "Client secret", "hint": "Paste the Client Secret from your Webex integration."})
    if not code:
        errors.append(
            {
                "var": "SETUP_AUTH_CODE",
                "label": "Authorization code",
                "hint": "Authorize the integration, then paste the code from the callback page.",
            }
        )
    if errors:
        return {"valid": False, "errors": errors, "config_applied": False}

    try:
        response = requests.post(
            WEBEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
    except requests.RequestException as exc:
        return {
            "valid": False,
            "errors": [
                {
                    "var": "SETUP_AUTH_CODE",
                    "label": "Authorization code",
                    "hint": f"Could not reach Webex token endpoint: {exc}",
                }
            ],
            "config_applied": False,
        }

    if response.status_code >= 400:
        hint = _webex_error_message(response, "Could not exchange the authorization code")
        field = "SETUP_CLIENT_SECRET" if ("client" in hint.lower() or "secret" in hint.lower()) else "SETUP_AUTH_CODE"
        return {
            "valid": False,
            "errors": [
                {
                    "var": field,
                    "label": "Integration",
                    "hint": hint
                    + " Confirm the Redirect URI matches exactly, and that the code has not already been used.",
                }
            ],
            "config_applied": False,
        }

    try:
        payload = response.json()
    except ValueError:
        return {
            "valid": False,
            "errors": [
                {
                    "var": "SETUP_AUTH_CODE",
                    "label": "Authorization code",
                    "hint": "Webex returned an invalid token response.",
                }
            ],
            "config_applied": False,
        }

    token = _normalize_token(str(payload.get("access_token") or ""))
    if not token:
        return {
            "valid": False,
            "errors": [
                {
                    "var": "SETUP_AUTH_CODE",
                    "label": "Authorization code",
                    "hint": "Webex did not return an access token.",
                }
            ],
            "config_applied": False,
        }

    granted_raw = str(payload.get("scope") or "")
    missing = missing_required_scopes(granted_raw)
    if missing:
        missing_list = ", ".join(missing)
        return {
            "valid": False,
            "errors": [
                {
                    "var": "SETUP_AUTH_CODE",
                    "label": "Required scopes",
                    "hint": (
                        "The access token is missing these scopes: "
                        + missing_list
                        + ". Edit the integration and check each highlighted chip, copy the new OAuth Authorization URL, "
                        "then click Authorize in Webex again. The previous authorization code cannot be reused. If those "
                        "scopes were already checked, the admin account may be missing a Contact Center or Control Hub privilege."
                    ),
                }
            ],
            "missing_scopes": missing,
            "message": (
                "Token was issued, but required scopes are missing. "
                "Update the integration checkboxes and authorize again before continuing."
            ),
            "config_applied": False,
        }

    save_token(token, auth_method="integration")
    save_integration_client_id(client_id)
    org_id = org_id_from_token(token) or _org_from_people_me(token)
    if org_id:
        save_suggested_org_id(org_id)

    return {
        "valid": True,
        "errors": [],
        "config_applied": True,
        "org_id": org_id or "",
        "normalized": {"SETUP_BEARER_TOKEN": "__saved__"},
    }


def verify_setup_step(step_id: str, submitted: dict[str, str]) -> dict:
    errors: list[dict] = []
    normalized: dict[str, str] = {}
    config_applied = False

    if step_id == "0.1":
        raw = submitted.get("SETUP_BEARER_TOKEN") or ""
        token = _normalize_token(raw)
        existing = get_stored_token()
        if (not token or token == "your_bearer_token_here") and existing:
            config_applied = True
            normalized["SETUP_BEARER_TOKEN"] = "__saved__"
        elif not token or token == "your_bearer_token_here":
            errors.append(
                {
                    "var": "SETUP_BEARER_TOKEN",
                    "label": describe_field("SETUP_BEARER_TOKEN")["label"],
                    "hint": (
                        "Click your profile in the Developer Portal and copy the bearer token. "
                        "Paste the token string only — do not include the word Bearer. "
                        "Or use the Integration option to exchange an authorization code."
                    ),
                }
            )
        elif len(token) < 20:
            errors.append(
                {
                    "var": "SETUP_BEARER_TOKEN",
                    "label": describe_field("SETUP_BEARER_TOKEN")["label"],
                    "hint": "This token looks too short. Copy the full bearer token from your profile menu.",
                }
            )
        else:
            save_token(token, auth_method="bearer")
            config_applied = True
            normalized["SETUP_BEARER_TOKEN"] = "__saved__"

    elif step_id == "0.2":
        org_id = (submitted.get("SETUP_ORG_ID") or "").strip()
        token = _normalize_token(submitted.get("SETUP_BEARER_TOKEN") or "") or get_stored_token()

        if not token:
            errors.append(
                {
                    "var": "SETUP_ORG_ID",
                    "label": describe_field("SETUP_ORG_ID")["label"],
                    "hint": "Complete step 0.1 (admin token or integration) before saving your organization ID.",
                }
            )

        if not org_id or org_id == "your_org_id_here":
            errors.append(
                {
                    "var": "SETUP_ORG_ID",
                    "label": describe_field("SETUP_ORG_ID")["label"],
                    "hint": "Copy your organization ID from the Developer Portal profile menu, or from the integration token.",
                }
            )
        elif not _UUID_RE.match(org_id):
            errors.append(
                {
                    "var": "SETUP_ORG_ID",
                    "label": describe_field("SETUP_ORG_ID")["label"],
                    "hint": "Org ID must be a UUID like 5e5c9ad6-d61f-870d-6d77-8fc1b…",
                }
            )

        if not errors and token:
            token_org = org_id_from_token(token)
            if token_org and token_org.lower() != org_id.lower():
                errors.append(
                    {
                        "var": "SETUP_ORG_ID",
                        "label": describe_field("SETUP_ORG_ID")["label"],
                        "hint": (
                            f"This org ID does not match the org embedded in your token ({token_org}). "
                            "Copy the org ID shown with your profile bearer token."
                        ),
                    }
                )

        if not errors and token and org_id:
            ok, message = _probe_wxcc_users(token, org_id)
            if not ok:
                errors.append(
                    {
                        "var": "SETUP_ORG_ID",
                        "label": describe_field("SETUP_ORG_ID")["label"],
                        "hint": message,
                    }
                )
            else:
                save_token(token)
                save_org_id(org_id)
                config_applied = True
                normalized["SETUP_ORG_ID"] = org_id
                normalized["SETUP_BEARER_TOKEN"] = "__saved__"

    else:
        return {"valid": False, "errors": [{"var": "", "label": "", "hint": "Unknown setup step."}], "normalized": {}}

    return {
        "valid": not errors,
        "errors": errors,
        "normalized": normalized,
        "config_applied": config_applied,
    }
