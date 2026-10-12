"""How-it-works copy for dashboard info buttons (Modules 1–5)."""

from __future__ import annotations

from lab_store import get_answer
from progress import is_filled


def _path(var_name: str, fallback: str) -> str:
    value = get_answer(var_name, fallback)
    return value if is_filled(value) else fallback


def _setup_auth_info() -> dict:
    try:
        from lab_credentials import get_auth_method, get_integration_client_id
        from lab_setup import WEBEX_AUTHORIZE_URL, WEBEX_TOKEN_URL, selectable_integration_scopes
    except ImportError:
        from lab_credentials import get_auth_method, get_integration_client_id

        WEBEX_AUTHORIZE_URL = "https://webexapis.com/v1/authorize"
        WEBEX_TOKEN_URL = "https://webexapis.com/v1/access_token"

        def selectable_integration_scopes():
            return []

    method = get_auth_method()
    client_id = get_integration_client_id()
    scope_ids = [item["id"] for item in selectable_integration_scopes()]
    if method == "integration":
        return {
            "title": "How setup was completed",
            "method": "POST",
            "endpoints": [
                {"method": "GET", "path": WEBEX_AUTHORIZE_URL, "role": "Admin consents; lab receives an authorization code", "docs": "https://developer.webex.com/docs/integrations"},
                {"method": "POST", "path": WEBEX_TOKEN_URL, "role": "Exchange code + Client ID + Client Secret for an access token", "docs": "https://developer.webex.com/docs/integrations"},
                {"method": "GET", "path": "/people/me", "role": "Optional — resolve organization ID from the new token", "docs": "https://developer.webex.com/docs/api/v1/people/get-my-own-details"},
            ],
            "how": (
                "Setup used a Webex Integration (OAuth authorization-code grant). "
                "You created an integration, set this lab's Redirect URI, checked the required scopes, "
                "pasted the OAuth Authorization URL from the integration page, "
                "then authorized as a Contact Center admin before generating a token. "
                "The lab called POST /v1/access_token and stored only the access token locally. "
                "The client secret, authorization code, and refresh token are not saved. "
                + (f"Client ID on file: {client_id[:8]}…" if client_id else "")
            ).strip(),
            "labels": [
                "Auth method: Webex Integration (authorization code).",
                "Required scopes: " + (", ".join(scope_ids) if scope_ids else "cjp:config family plus spark-admin people/roles/licenses/telephony."),
                "The Connected card reflects credentials in data/lab_credentials.json — not values typed into the form after exchange.",
                "Access tokens expire; create a new authorization code or paste a fresh admin profile token to reconnect.",
            ],
        }
    return {
        "title": "How setup was completed",
        "method": "GET",
            "endpoints": [
                {"method": "GET", "path": "developer.webex.com (profile menu)", "role": "Copy admin bearer token and organization ID", "docs": "https://developer.webex.com"},
                {"method": "GET", "path": "/{orgId}/v2/user", "role": "Step 0.2 probes List Users to confirm the token and org", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users"},
            ],
        "how": (
            "Setup used an admin profile bearer token from the Webex Developer Portal. "
            "You copied the token (and later the organization ID) from your profile menu. "
            "The lab stores the token locally and uses it as Authorization: Bearer on WxCC and Webex APIs. "
            "No OAuth client secret was involved."
        ),
        "labels": [
            "Auth method: Admin profile bearer token.",
            "The token is the same kind shown in your Developer Portal profile — it must come from a Contact Center admin.",
            "Step 0.2 verifies the org ID against the token and calls List Users before marking Setup complete.",
        ],
    }


def get_section_info(section_id: str) -> dict:
    if section_id == "setup-auth":
        return {"id": section_id, **_setup_auth_info()}
    sections = {
        "users": {
            "title": "Contact Center Users",
            "method": "GET",
            "endpoints": [
                {"method": "GET", "path": _path("USERS_LIST_ENDPOINT", "/{orgId}/v2/user"), "role": "List users", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users"},
                {"method": "GET", "path": _path("AGENT_PROFILE_LIST_ENDPOINT", "/{orgId}/v2/agent-profile"), "role": "List desktop profiles", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/desktop-profile/list-desktop-profiles"},
                {"method": "GET", "path": _path("USER_PROFILE_LIST_ENDPOINT", "/{orgId}/v3/user-profile"), "role": "List user profiles", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/user-profiles/list-user-profiles"},
                {"method": "GET", "path": _path("SKILL_PROFILE_LIST_ENDPOINT", "/{orgId}/v2/skill-profile"), "role": "List skill profiles", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/skill-profile/list-skill-profiles"},
                {"method": "GET", "path": _path("TEAM_LIST_ENDPOINT", "/{orgId}/v2/team"), "role": "List teams", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams"},
                {"method": "GET", "path": _path("MULTIMEDIA_PROFILE_LIST_ENDPOINT", "/{orgId}/v2/multimedia-profile"), "role": "List multimedia profiles", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/multimedia-profile/list-multimedia-profiles"},
            ],
            "how": (
                "GET List Users returns raw user records (name, email, and UUID pointers). "
                "List Users v2 does not include teamIds on each user, so the dashboard GET-lists teams "
                "and joins membership from each team's userIds array to resolve team names. "
                "Profile names come from the matching list APIs. "
                "Channel types come from multimedia-profile capacity fields (value > 0)."
            ),
            "labels": [
                "Each table row is one Contact Center user from GET List Users.",
                "Use the search box above the table to filter by name, email, profile, team, or channel.",
                "Profile columns replace UUID pointers with names from the matching list APIs.",
                "Team names are joined from GET List Teams (each team’s userIds), not from a teamIds field on the user.",
                "Channel Types lists channels whose multimedia-profile capacity is greater than zero.",
            ],
        },
        "entry-points": {
            "title": "Entry Points / Channels",
            "method": "GET",
            "endpoints": [
                {"method": "GET", "path": _path("ENTRY_POINT_LIST_ENDPOINT", "/{orgId}/v2/entry-point"), "role": "List entry points", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/entry-point/list-entry-points"},
                {"method": "GET", "path": _path("DIAL_NUMBER_LIST_ENDPOINT", "/{orgId}/v3/dial-number"), "role": "List dial-number mappings", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/dial-number/list-dialed-number-mappings"},
            ],
            "how": (
                "GET entry points for name, flow, channel, and status. Dial-number mappings supply DN, "
                "Webex Calling location, and media region, joined to entry points by entry-point ID."
            ),
        },
        "queues": {
            "title": "Queues",
            "method": "GET",
            "endpoints": [
                {"method": "GET", "path": _path("QUEUE_LIST_ENDPOINT", "/{orgId}/v2/contact-service-queue"), "role": "List contact-service queues (v2)", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/contact-service-queues/list-contact-service-queues"},
            ],
            "how": (
                "GET the v2 queue list (`/v2/contact-service-queue`) and map JSON fields "
                "(name, direction, type, routing, active) onto table rows. "
                "Use v2 — the v3 queue list is being removed. When you develop against WxCC APIs, "
                "copy the v2 endpoint, not a v3 URL."
            ),
            "labels": [
                "Each row is one contact-service queue from the v2 list API.",
                "Use the table search box to filter by name, direction, type, or status.",
            ],
        },
        "teams": {
            "title": "Teams",
            "method": "GET",
            "endpoints": [
                {"method": "GET", "path": _path("TEAM_LIST_ENDPOINT", "/{orgId}/v2/team"), "role": "List teams", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams"},
            ],
            "how": "GET the v2 team list and display name, site, type, DN (capacity teams), and status.",
        },
        "aux-codes": {
            "title": "Auxiliary Codes",
            "method": "GET",
            "endpoints": [
                {"method": "GET", "path": _path("AUX_CODE_LIST_ENDPOINT", "/{orgId}/v2/auxiliary-code"), "role": "List auxiliary codes", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/auxiliary-code/list-auxiliary-codes"},
            ],
            "how": "GET auxiliary codes and map name, work-type code, default flag, and active status onto the table.",
        },
        "global-vars": {
            "title": "Global Variables",
            "method": "GET / PUT",
            "endpoints": [
                {"method": "GET", "path": _path("GLOBAL_VARIABLE_LIST_ENDPOINT", "/{orgId}/v2/cad-variable"), "role": "List global variables", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/list-global-variables"},
                {"method": "PUT", "path": _path("GV_UPDATE_ENDPOINT", "/{orgId}/cad-variable/{variableId}"), "role": "Update a variable by ID", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/update-specific-global-variable-by-id"},
            ],
            "how": (
                "GET lists CAD variables for the table (searchable). After step 2.6, Edit GETs that variable "
                "and PUT sends the writable Update-by-ID fields for its variableType. Name and type stay read-only."
            ),
        },
        "global-vars-edit": {
            "title": "Update Global Variable",
            "method": "GET / PUT",
            "endpoints": [
                {"method": "GET", "path": _path("GV_UPDATE_ENDPOINT", "/{orgId}/cad-variable/{variableId}"), "role": "Load the variable (CadVariableDTO) before edit", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/get-specific-global-variable-by-id"},
                {"method": "PUT", "path": _path("GV_UPDATE_ENDPOINT", "/{orgId}/cad-variable/{variableId}"), "role": "Save writable Update-by-ID fields", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/update-specific-global-variable-by-id"},
            ],
            "how": (
                "Edit GETs the variable by ID, then shows only the writable CadVariableDTO fields for that "
                "variableType (string, integer, decimal, boolean, or date/time), plus description, desktop label, "
                "and the required flags (active, reportable, agentViewable, agentEditable). "
                "Save PUTs that body. Name and type cannot be changed. Requires cjp:config_write. "
                "Use a test variable — avoid production or system-default records."
            ),
            "labels": [
                "GET loads the current object so PUT can send a complete CadVariableDTO.",
                "Extra GET-only fields (createdTime, lastUpdatedTime, and similar) are stripped before PUT.",
            ],
        },
        "csr": {
            "title": "CSR — Contact volume",
            "method": "POST",
            "endpoints": [
                {"method": "POST", "path": "/search?orgId={orgId}", "role": "GraphQL taskDetails (CSR)", "docs": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/CSR.md"},
            ],
            "how": (
                "POST a GraphQL query to the Search API for Customer Session Records over the last 30 days. "
                "The dashboard then counts and groups those rows to build the card."
            ),
            "labels": [
                "The large number is a count of CSR rows (customer sessions) returned for the last 30 days.",
                "Channel chips count how many of those sessions occurred on each channelType.",
                "Termination chips count sessions by terminationType (how the contact ended).",
                "Direction chips count inbound vs outbound sessions using the direction field.",
            ],
        },
        "csr-details": {
            "title": "Customer Session Details",
            "method": "POST",
            "endpoints": [
                {"method": "POST", "path": "/search?orgId={orgId}", "role": "GraphQL taskDetails (CSR list)", "docs": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/CSR.md"},
            ],
            "how": (
                "POST GraphQL for Customer Session Records over the last 30 days and list each session. "
                "Click an Interaction ID to load CAR events for that contact."
            ),
            "labels": [
                "Each row is one CSR (customer session) from the last 30 days.",
                "Interaction ID is the task/contact identifier used to query CAR events.",
            ],
        },
        "car": {
            "title": "CAR — Customer Activity Records",
            "method": "POST",
            "endpoints": [
                {"method": "POST", "path": "/search?orgId={orgId}", "role": "GraphQL taskDetails activities (CAR)", "docs": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/CAR.md"},
            ],
            "how": (
                "POST GraphQL for Customer Activity Records nested under a customer session. "
                "Activity name, queue, and timestamps show how that contact was routed."
            ),
            "labels": [
                "Each row is one CAR activity (queue/event) for the selected interaction, not a unique contact.",
                "Queue name and activity name come from the CAR fields you entered in step 3.2.",
            ],
        },
        "asr": {
            "title": "ASR — Agent sessions by team",
            "method": "POST",
            "endpoints": [
                {"method": "POST", "path": "/search?orgId={orgId}", "role": "GraphQL agentSession (ASR)", "docs": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/ASR.md"},
            ],
            "how": (
                "POST GraphQL for Agent Session Records. Unique agent IDs and team names answer "
                "who was logged in and which team they belong to."
            ),
            "labels": [
                "The large number is a count of ASR rows (agent sessions), not unique people.",
                "Total logged-in time sums (endTime − startTime) across those sessions.",
                "Unique agents is a distinct count of agentId values across those sessions.",
                "Team chips count how many sessions belong to each teamName.",
            ],
        },
        "asr-details": {
            "title": "Agent Session Details",
            "method": "POST",
            "endpoints": [
                {"method": "POST", "path": "/search?orgId={orgId}", "role": "GraphQL agentSession (ASR list)", "docs": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/ASR.md"},
            ],
            "how": (
                "POST GraphQL for Agent Session Records over the last 30 days and list each session. "
                "Click an Agent Session ID to load AAR state events for that login."
            ),
            "labels": [
                "Each row is one ASR (agent session) from the last 30 days.",
                "Agent Session ID is used to query AAR events for that session.",
            ],
        },
        "aar": {
            "title": "AAR — Agent Activity Records",
            "method": "POST",
            "endpoints": [
                {"method": "POST", "path": "/search?orgId={orgId}", "role": "GraphQL agentSession activities (AAR)", "docs": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/AAR.md"},
            ],
            "how": (
                "POST GraphQL for agent activity nodes (state and duration) under the selected session's channelInfo. "
                "That is the AAR query from step 3.4."
            ),
            "labels": [
                "Each row is one AAR state interval for the selected agent session, not a unique agent.",
                "State and duration come from the AAR fields you entered in step 3.4.",
            ],
        },
        "rt-agents": {
            "title": "Real-Time Agent States",
            "method": "POST + GET",
            "endpoints": [
                {"method": "POST", "path": "/search?orgId={orgId}", "role": "GraphQL agentSession where isActive = true", "docs": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/ASR.md"},
                {"method": "GET", "path": "/v1/agents/activities", "role": "Latest telephony activities for those agents", "docs": "https://developer.webex.com/webex-contact-center/docs/api/v1/agents/get-agent-activities"},
            ],
            "how": (
                "GraphQL Search (orgId from Setup) finds logged-in agents. "
                "GET /v1/agents/activities?channelTypes=telephony then overlays current state, idle code, "
                "duration, and interaction ID. The table polls every 10 seconds. No webhooks."
            ),
            "labels": [
                "Each table row is one logged-in agent from GraphQL (isActive = true).",
                "Current state, idle code, duration, and interaction ID come from GET /v1/agents/activities, matched by agent ID.",
            ],
        },
        "people": {
            "title": "Control Hub — People",
            "method": "GET",
            "endpoints": [
                {"method": "GET", "path": _path("WEBEX_PEOPLE_ENDPOINT", "/people"), "role": "List people", "docs": "https://developer.webex.com/docs/api/v1/people/list-people"},
                {"method": "GET", "path": _path("WEBEX_ROLES_ENDPOINT", "/roles"), "role": "List roles", "docs": "https://developer.webex.com/docs/api/v1/roles/list-roles"},
                {"method": "GET", "path": _path("WEBEX_LICENSES_ENDPOINT", "/licenses"), "role": "List licenses", "docs": "https://developer.webex.com/docs/api/v1/licenses/list-licenses"},
            ],
            "how": (
                "GET people from webexapis.com, then GET roles and licenses. Role and license UUID arrays "
                "on each person are matched to display names before the table is rendered."
            ),
        },
        "locations": {
            "title": "Webex Calling — Locations",
            "method": "GET",
            "endpoints": [
                {"method": "GET", "path": _path("WEBEX_LOCATION_ENDPOINT", "/locations"), "role": "List locations", "docs": "https://developer.webex.com/calling/docs/api/v1/locations/list-locations"},
                {"method": "GET", "path": _path("WEBEX_PHONE_NUMBERS_ENDPOINT", "/telephony/config/numbers"), "role": "List phone numbers", "docs": "https://developer.webex.com/calling/docs/api/v1/numbers/get-phone-numbers-for-an-organization-with-given-criteria"},
            ],
            "how": (
                "GET locations for name, country, and formatted address. Phone numbers are counted per "
                "location ID to fill the provisioned-numbers column."
            ),
            "labels": [
                "Each row is one Webex Calling location.",
                "Provisioned Numbers is a count of telephony numbers whose location ID matches that location.",
            ],
        },
        "pstn": {
            "title": "PSTN — Entry Point Numbers",
            "method": "GET",
            "endpoints": [
                {"method": "GET", "path": _path("WEBEX_PHONE_NUMBERS_ENDPOINT", "/telephony/config/numbers"), "role": "Match entry-point DNs to Calling numbers", "docs": "https://developer.webex.com/calling/docs/api/v1/numbers/get-phone-numbers-for-an-organization-with-given-criteria"},
                {"method": "GET", "path": _path("PSTN_CONNECTION_ENDPOINT", "/telephony/pstn/locations/{location_id}/connection"), "role": "PSTN connection per location", "docs": "https://developer.webex.com/calling/docs/api/v1/pstn/retrieve-pstn-connection-for-a-location"},
            ],
            "how": (
                "Module 2 entry-point DNs are matched to Webex Calling numbers. Each number's location ID "
                "is used to GET the PSTN connection (carrier and type) for that site. "
                "That PSTN call needs spark-admin:telephony_pstn_read (locations/numbers use telephony_config_read)."
            ),
        },
    }
    info = sections.get(section_id)
    if not info:
        raise ValueError(f"Unknown dashboard section: {section_id}")
    return {"id": section_id, **info}
