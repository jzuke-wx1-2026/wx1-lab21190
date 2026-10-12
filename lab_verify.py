"""Validate lab answers against the instructor key and return field hints."""

from __future__ import annotations

import ast
import re
from functools import lru_cache
from pathlib import Path

from config import FILL_IN_PLACEHOLDER
from lab_data_dictionary import (
    FIELD_VAR_REPORT,
    RECORD_TYPE_VARS,
    dictionary_hint,
    field_in_dictionary,
    graphql_leaf,
)
from lab_paths import normalize_endpoint_for_storage, paths_equivalent
from lab_ui import describe_field, get_field_hint

ROOT = Path(__file__).resolve().parent
ANSWER_KEY = ROOT / "solutions" / "INSTRUCTOR_ANSWER_KEY.md"
ASSIGN_RE = re.compile(r"^([A-Z][A-Z0-9_]*)\s*=\s*(.+)$")

CASE_INSENSITIVE_VARS = RECORD_TYPE_VARS | {"GV_REQUEST_METHOD"}


def normalize_answer(value: str | None) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if not text or text == FILL_IN_PLACEHOLDER:
        return ""
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        try:
            parsed = ast.literal_eval(text)
            return str(parsed).strip()
        except (ValueError, SyntaxError):
            return text[1:-1].strip()
    return text


@lru_cache(maxsize=1)
def load_expected_answers() -> dict[str, str]:
    if not ANSWER_KEY.is_file():
        return {}
    answers: dict[str, str] = {}
    in_block = False
    for line in ANSWER_KEY.read_text(encoding="utf-8").splitlines():
        if line.strip() == "```python":
            in_block = True
            continue
        if in_block and line.strip() == "```":
            in_block = False
            continue
        if not in_block:
            continue
        match = ASSIGN_RE.match(line.strip())
        if match:
            answers[match.group(1)] = normalize_answer(match.group(2))
    return answers


def _generic_hint(var_name: str, submitted: str, expected: str) -> str:
    if not submitted:
        return "This field is required — paste the value from the API endpoint documentation."

    if var_name in FIELD_VAR_REPORT:
        return dictionary_hint(FIELD_VAR_REPORT[var_name])

    if var_name.endswith("_METHOD"):
        return "Enter the HTTP method shown on the Update API page (e.g. PUT)."

    if expected and submitted.lower() == expected.lower() and submitted != expected:
        return "Almost there — JSON property names are case-sensitive. Match the capitalization exactly."

    if var_name.endswith("_ENDPOINT"):
        if not submitted.startswith("/") and "://" not in submitted:
            return "Paste the full endpoint from the API endpoint documentation — it starts with /organization/… or /."
        if expected and not paths_equivalent(submitted, expected):
            return (
                "Compare the endpoint in the API endpoint documentation character-for-character. "
                "You can paste it exactly as shown, including /organization/<your-org-id>/…."
            )
        return "Paste the endpoint exactly as it appears in the API endpoint documentation."

    if var_name.endswith("_RECORD_TYPE"):
        return "Enter the three-letter report type code (CSR, CAR, ASR, or AAR)."

    if var_name.endswith("_KEY"):
        return "Expand a sample record in the API endpoint documentation or the schema — copy the exact JSON key (camelCase)."

    return "Double-check the API endpoint documentation for the exact spelling."


def hint_for_field(
    module_id: str,
    step_id: str,
    var_name: str,
    submitted: str,
    expected: str,
) -> str:
    custom = get_field_hint(module_id, step_id, var_name)
    if custom:
        return custom
    return _generic_hint(var_name, submitted, expected)


def _normalize_stored_value(var_name: str, user_value: str, expected: str) -> str:
    if var_name in CASE_INSENSITIVE_VARS:
        return (expected or user_value).upper()
    if var_name.endswith("_ENDPOINT") and expected:
        return normalize_endpoint_for_storage(user_value, expected)
    return user_value


def verify_step_answers(
    module_id: str,
    step_id: str,
    variables: list[str],
    submitted: dict[str, str],
) -> dict:
    expected_answers = load_expected_answers()
    errors: list[dict] = []
    normalized: dict[str, str] = {}

    for var in variables:
        user_value = normalize_answer(submitted.get(var))
        expected = expected_answers.get(var, "")

        if not user_value:
            errors.append(
                {
                    "var": var,
                    "label": describe_field(var)["label"],
                    "hint": hint_for_field(module_id, step_id, var, user_value, expected),
                }
            )
            continue

        if var in FIELD_VAR_REPORT:
            report = FIELD_VAR_REPORT[var]
            matches_dictionary = field_in_dictionary(report, user_value)
            matches_key = bool(
                expected
                and graphql_leaf(user_value) == graphql_leaf(expected)
            )
            if not matches_dictionary and not matches_key:
                errors.append(
                    {
                        "var": var,
                        "label": describe_field(var)["label"],
                        "hint": hint_for_field(module_id, step_id, var, user_value, expected),
                    }
                )
            else:
                normalized[var] = user_value
            continue

        if var.endswith("_ENDPOINT") and expected:
            if not paths_equivalent(user_value, expected):
                errors.append(
                    {
                        "var": var,
                        "label": describe_field(var)["label"],
                        "hint": hint_for_field(module_id, step_id, var, user_value, expected),
                    }
                )
            else:
                normalized[var] = _normalize_stored_value(var, user_value, expected)
        elif var in CASE_INSENSITIVE_VARS:
            if expected and user_value.upper() != expected.upper():
                errors.append(
                    {
                        "var": var,
                        "label": describe_field(var)["label"],
                        "hint": hint_for_field(module_id, step_id, var, user_value, expected),
                    }
                )
            else:
                normalized[var] = _normalize_stored_value(var, user_value, expected)
        elif expected and user_value != expected:
            errors.append(
                {
                    "var": var,
                    "label": describe_field(var)["label"],
                    "hint": hint_for_field(module_id, step_id, var, user_value, expected),
                }
            )
        else:
            normalized[var] = user_value

    return {"valid": not errors, "errors": errors, "normalized": normalized}
