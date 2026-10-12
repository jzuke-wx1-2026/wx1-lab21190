"""Dashboard copy, API reference details, and field hints for lab steps."""

from __future__ import annotations

import re

from config import FILL_IN_PLACEHOLDER


def _label_from_camel(key: str) -> str:
    """Turn a JSON property name into a Title Case label (e.g. firstName → First Name)."""
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", key)
    spaced = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", spaced)
    return " ".join(part.capitalize() for part in spaced.split())


# Maps lab variables to the JSON property they represent (for input labels only).
_JSON_PROPERTY_BY_VAR: dict[str, str] = {
    "USER_FIRST_NAME_KEY": "firstName",
    "USER_LAST_NAME_KEY": "lastName",
    "USER_EMAIL_KEY": "email",
    "AGENT_PROFILE_ID_KEY": "agentProfileId",
    "MULTIMEDIA_PROFILE_ID_KEY": "multimediaProfileId",
    "USER_PROFILE_ID_KEY": "userProfileId",
    "AGENT_PROFILE_NAME_KEY": "name",
    "USER_PROFILE_NAME_KEY": "name",
    "SKILL_PROFILE_ID_KEY": "id",
    "SKILL_NAME_KEY": "name",
    "TEAM_IDS_KEY": "userIds",
    "TEAM_NAME_KEY": "name",
    "MULTIMEDIA_PROFILE_NAME_KEY": "name",
    "CHANNEL_TELEPHONY_KEY": "telephony",
    "CHANNEL_CHAT_KEY": "chat",
    "CHANNEL_EMAIL_KEY": "email",
    "CHANNEL_SOCIAL_KEY": "social",
    "EP_NAME_KEY": "name",
    "EP_FLOW_ID_KEY": "flowId",
    "EP_ACTIVE_KEY": "active",
    "DIAL_NUMBER_DN_KEY": "dialledNumber",
    "DIAL_NUMBER_EP_ID_KEY": "entryPointId",
    "DIAL_NUMBER_LOCATION_KEY": "location",
    "DIAL_NUMBER_REGION_KEY": "regionId",
    "QUEUE_NAME_KEY": "name",
    "QUEUE_ID_KEY": "id",
    "QUEUE_CONTACT_DIRECTION_KEY": "queueType",
    "QUEUE_TYPE_KEY": "channelType",
    "QUEUE_ROUTING_TYPE_KEY": "queueRoutingType",
    "QUEUE_STATUS_KEY": "active",
    "TEAM_SITE_NAME_KEY": "siteName",
    "TEAM_TYPE_KEY": "teamType",
    "TEAM_DN_KEY": "dialedNumber",
    "TEAM_STATUS_KEY": "teamStatus",
    "AUX_CODE_NAME_KEY": "name",
    "AUX_CODE_ID_KEY": "id",
    "AUX_CODE_TYPE_KEY": "workTypeCode",
    "AUX_CODE_DEFAULT_KEY": "defaultCode",
    "AUX_CODE_STATUS_KEY": "active",
    "GV_NAME_KEY": "name",
    "GV_VALUE_KEY": "defaultValue",
    "GV_TYPE_KEY": "variableType",
    "GV_STATUS_KEY": "active",
    "CSR_TASK_ID_KEY": "id",
    "CSR_CHANNEL_TYPE_KEY": "channelType",
    "CSR_TERMINATION_TYPE_KEY": "terminationType",
    "CSR_CALL_DIRECTION_KEY": "direction",
    "CAR_ACTIVITY_NAME_KEY": "activityName",
    "CAR_QUEUE_NAME_KEY": "queueName",
    "ASR_AGENT_ID_KEY": "agentId",
    "ASR_AGENT_NAME_KEY": "agentName",
    "ASR_TEAM_NAME_KEY": "teamName",
    "AAR_ACTIVITY_TYPE_KEY": "state",
    "AAR_DURATION_KEY": "duration",
    "RT_AGENT_STATE_KEY": "isActive",
    "RT_AGENT_ID_KEY": "agentId",
    "PEOPLE_EMAIL_KEY": "emails",
    "PEOPLE_DISPLAY_NAME_KEY": "displayName",
    "PEOPLE_STATUS_KEY": "status",
    "PEOPLE_ROLES_KEY": "roles",
    "PEOPLE_LICENSES_KEY": "licenses",
    "LOCATION_NAME_KEY": "name",
    "LOCATION_ID_KEY": "id",
    "LOCATION_ADDRESS_KEY": "address",
    "PHONE_NUMBER_KEY": "phoneNumber",
}

FIELD_LABELS: dict[str, str] = {
    var: _label_from_camel(prop) for var, prop in _JSON_PROPERTY_BY_VAR.items()
}
FIELD_LABELS.update(
    {
        "CSR_RECORD_TYPE": "Report Type",
        "CSR_TERMINATION_TYPE_KEY": "Termination Type",
        "CSR_CALL_DIRECTION_KEY": "Call Direction",
        "CAR_RECORD_TYPE": "Report Type",
        "ASR_RECORD_TYPE": "Report Type",
        "AAR_RECORD_TYPE": "Report Type",
        "SETUP_BEARER_TOKEN": "Admin bearer token",
        "SETUP_ORG_ID": "Organization ID",
        "TEAM_IDS_KEY": "User IDs",
    }
)

ENDPOINT_PLACEHOLDERS: dict[str, str] = {
    "USERS_LIST_ENDPOINT": "/{orgId}/v2/resourceName",
    "AGENT_PROFILE_LIST_ENDPOINT": "/{orgId}/v2/resourceName",
    "USER_PROFILE_LIST_ENDPOINT": "/{orgId}/v3/resourceName",
    "SKILL_PROFILE_LIST_ENDPOINT": "/{orgId}/v2/resourceName",
    "TEAM_LIST_ENDPOINT": "/{orgId}/v2/resourceName",
    "MULTIMEDIA_PROFILE_LIST_ENDPOINT": "/{orgId}/v2/resourceName",
    "ENTRY_POINT_LIST_ENDPOINT": "/{orgId}/v2/resourceName",
    "DIAL_NUMBER_LIST_ENDPOINT": "/{orgId}/v3/resourceName",
    "QUEUE_LIST_ENDPOINT": "/{orgId}/v2/resourceName",
    "AUX_CODE_LIST_ENDPOINT": "/{orgId}/v2/resourceName",
    "GLOBAL_VARIABLE_LIST_ENDPOINT": "/{orgId}/v2/resourceName",
    "GV_UPDATE_ENDPOINT": "/{orgId}/resourceName/{resourceId}",
    "WEBEX_PEOPLE_ENDPOINT": "/resourceName",
    "WEBEX_ROLES_ENDPOINT": "/resourceName",
    "WEBEX_LICENSES_ENDPOINT": "/resourceName",
    "WEBEX_LOCATION_ENDPOINT": "/resourceName",
    "PSTN_CONNECTION_ENDPOINT": "/telephony/pstn/locations/{location_id}/connection",
    "WEBEX_PHONE_NUMBERS_ENDPOINT": "/telephony/config/resourceName",
}


STEP_META: dict[tuple[str, str], dict] = {
    ("module0", "0.1"): {
        "instruction": "Connect with an admin profile bearer token, or create a Webex Integration and let the lab exchange the authorization code for a token.",
        "doc_url": "https://developer.webex.com",
        "doc_title": "Access token",
        "doc_guide": [
            "Go to [developer.webex.com](https://developer.webex.com) and sign in with your Webex Contact Center admin account.",
            "Click your profile (avatar or name) in the top-right corner.",
            "Copy the bearer token shown in your profile.",
            "Paste the token string only — do not include the word Bearer.",
        ],
    },
    ("module0", "0.2"): {
        "instruction": "Paste your organization ID and verify lab connectivity.",
        "doc_url": "https://developer.webex.com",
        "doc_title": "Organization ID",
        "doc_guide": [
            "In the [developer portal](https://developer.webex.com), click your profile (avatar or name) in the top-right corner, then copy your organization ID.",
            "The org ID must belong to the same organization as the token from step 0.1 (admin profile or integration).",
            "When you save this step, the lab calls the [WxCC List Users API](https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users) to confirm your bearer token is valid.",
            "Once this step is complete, you can close your developer portal integration page.",
        ],
    },
    ("module1", "1.1"): {
        "instruction": "Navigate to the List Users API. Copy the endpoint and paste it into the lab.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users",
        "doc_title": "List Users",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "doc_guide": [
            "Navigate to the List Users API.",
            "Copy the endpoint and paste it into the lab.",
        ],
        "field_hints": {
            "USERS_LIST_ENDPOINT": "Paste the List Users endpoint.",
        },
    },
    ("module1", "1.2"): {
        "instruction": "From the List Users API, run the request and copy first name, last name, and email keys from one user.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users",
        "doc_title": "List Users",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "doc_guide": [
            "From the List Users API, hit the Run button at the bottom of the page.",
            "From the response, locate the details for one user, then copy and paste the first name, last name, and email response keys into the lab.",
        ],
        "field_hints": {
            "USER_FIRST_NAME_KEY": "On each user object — the first name key.",
            "USER_LAST_NAME_KEY": "On each user object — the last name key.",
            "USER_EMAIL_KEY": "On each user object — the email key.",
        },
    },
    ("module1", "1.3"): {
        "instruction": "Copy profile ID keys from List Users, then list endpoints and name keys from the desktop, user, and multimedia profile APIs.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users",
        "doc_title": "Profile IDs & profile list APIs",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "field_groups": [
            {
                "id": "a",
                "title": "Part A — Profile IDs (List Users)",
                "instruction": "From the same List Users response, copy the agent, multimedia, and user profile ID keys.",
                "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users",
                "doc_title": "List Users",
                "api_method": "GET",
                "doc_guide": [
                    "From the same List Users response generated in the previous step, locate the keys for the agent, multimedia, and user profile IDs.",
                    "Copy and paste those keys into the lab.",
                ],
                "variables": [
                    "AGENT_PROFILE_ID_KEY",
                    "MULTIMEDIA_PROFILE_ID_KEY",
                    "USER_PROFILE_ID_KEY",
                ],
            },
            {
                "id": "b",
                "title": "Part B — List Desktop Profiles",
                "instruction": "Navigate to List Desktop Profiles. Copy the endpoint and the name key.",
                "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/desktop-profile/list-desktop-profiles",
                "doc_title": "List Desktop Profiles",
                "api_method": "GET",
                "doc_guide": [
                    "Navigate to the List Desktop Profiles API.",
                    "Copy the endpoint and paste it into the lab.",
                    "Hit the Run button at the bottom of the API page, then from the response copy the name key and paste it into the lab.",
                ],
                "variables": ["AGENT_PROFILE_LIST_ENDPOINT", "AGENT_PROFILE_NAME_KEY"],
            },
            {
                "id": "c",
                "title": "Part C — List User Profiles",
                "instruction": "Navigate to List User Profiles. Copy the endpoint and the name key.",
                "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/user-profiles/list-user-profiles",
                "doc_title": "List User Profiles",
                "api_method": "GET",
                "doc_guide": [
                    "Navigate to the List User Profiles API.",
                    "Copy the endpoint and paste it into the lab.",
                    "Hit the Run button at the bottom of the API page, then from the response copy the name key and paste it into the lab.",
                ],
                "variables": ["USER_PROFILE_LIST_ENDPOINT", "USER_PROFILE_NAME_KEY"],
            },
            {
                "id": "d",
                "title": "Part D — List Multimedia Profiles",
                "instruction": "Navigate to List Multimedia Profiles. Copy the endpoint and the name key.",
                "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/multimedia-profile/list-multimedia-profiles",
                "doc_title": "List Multimedia Profiles",
                "api_method": "GET",
                "doc_guide": [
                    "Navigate to the List Multimedia Profiles API.",
                    "Copy the endpoint and paste it into the lab.",
                    "Hit the Run button at the bottom of the API page, then from the response copy the name key and paste it into the lab.",
                ],
                "variables": ["MULTIMEDIA_PROFILE_LIST_ENDPOINT", "MULTIMEDIA_PROFILE_NAME_KEY"],
            },
        ],
        "field_hints": {
            "AGENT_PROFILE_ID_KEY": "List Users — agent profile ID key on each user object.",
            "MULTIMEDIA_PROFILE_ID_KEY": "List Users — multimedia profile ID key on each user object.",
            "USER_PROFILE_ID_KEY": "List Users — user profile ID key on each user object.",
            "AGENT_PROFILE_LIST_ENDPOINT": "List Desktop Profiles — list endpoint (no ID at the end).",
            "AGENT_PROFILE_NAME_KEY": "List Desktop Profiles — name key on each profile object.",
            "USER_PROFILE_LIST_ENDPOINT": "List User Profiles — list endpoint.",
            "USER_PROFILE_NAME_KEY": "List User Profiles — name key on each profile object.",
            "MULTIMEDIA_PROFILE_LIST_ENDPOINT": "List Multimedia Profiles — list endpoint.",
            "MULTIMEDIA_PROFILE_NAME_KEY": "List Multimedia Profiles — name key on each profile object.",
        },
    },
    ("module1", "1.4"): {
        "instruction": "From the same List Multimedia Profiles response, copy the telephony, chat, email, and social keys.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/multimedia-profile/list-multimedia-profiles",
        "doc_title": "List Multimedia Profiles",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "doc_guide": [
            "From the same List Multimedia Profiles response generated in the previous step, copy and paste the keys for telephony, chat, email, and social into the lab.",
        ],
        "field_hints": {
            "CHANNEL_TELEPHONY_KEY": "Telephony channel capacity key.",
            "CHANNEL_CHAT_KEY": "Chat channel capacity key.",
            "CHANNEL_EMAIL_KEY": "Email channel capacity key.",
            "CHANNEL_SOCIAL_KEY": "Social channel capacity key.",
        },
    },
    ("module1", "1.5"): {
        "instruction": "Navigate to List Skill Profiles. Copy the endpoint, then the id and name keys from the response.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/skill-profile/list-skill-profiles",
        "doc_title": "List Skill Profiles",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "doc_guide": [
            "Navigate to the List Skill Profiles API.",
            "Copy the endpoint and paste it into the lab.",
            "Hit the Run button at the bottom of the API page, then from the response copy and paste both id and name keys into the lab.",
        ],
        "field_hints": {
            "SKILL_PROFILE_LIST_ENDPOINT": "Paste the List Skill Profiles endpoint.",
            "SKILL_PROFILE_ID_KEY": "On each skill profile — the id key.",
            "SKILL_NAME_KEY": "On each skill profile — the name key.",
        },
    },
    ("module1", "1.6"): {
        "instruction": "Navigate to List Teams. Copy the endpoint and name key, then the user IDs array key from the same response.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams",
        "doc_title": "List Teams",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "field_groups": [
            {
                "id": "a",
                "title": "Part A — List Teams",
                "instruction": "Navigate to List Teams. Copy the endpoint and the name key.",
                "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams",
                "doc_title": "List Teams",
                "api_method": "GET",
                "doc_guide": [
                    "Navigate to the List Teams API.",
                    "Copy the endpoint and paste it into the lab.",
                    "Hit the Run button at the bottom of the API page, then from the response copy and paste the name key into the lab.",
                ],
                "variables": ["TEAM_LIST_ENDPOINT", "TEAM_NAME_KEY"],
            },
            {
                "id": "b",
                "title": "Part B — User IDs",
                "instruction": "From the same List Teams response, copy the key that holds an array of user IDs.",
                "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams",
                "doc_title": "List Teams",
                "api_method": "GET",
                "doc_guide": [
                    "From the same List Teams response generated in the previous step, locate the key that holds an array of user IDs, then copy and paste that key into the lab.",
                ],
                "variables": ["TEAM_IDS_KEY"],
            },
        ],
        "field_hints": {
            "TEAM_LIST_ENDPOINT": "Paste the List Teams endpoint.",
            "TEAM_IDS_KEY": "List Teams — key for the array of user IDs on each team object.",
            "TEAM_NAME_KEY": "List Teams — name key on each team object.",
        },
    },
    ("module2", "2.1"): {
        "instruction": "Copy the List Entry Points endpoint and keys, then the List Dialed Number Mappings endpoint and keys.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/entry-point/list-entry-points",
        "doc_title": "List Entry Points",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "field_groups": [
            {
                "id": "a",
                "title": "Part A — List Entry Points",
                "instruction": "Navigate to List Entry Points. Copy the endpoint and the name, flow id, and active keys.",
                "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/entry-point/list-entry-points",
                "doc_title": "List Entry Points",
                "api_method": "GET",
                "doc_guide": [
                    "Navigate to the List Entry Points API.",
                    "Copy the endpoint and paste it into the lab.",
                    "Hit the Run button at the bottom of the API page, then from the response copy and paste the name, flow id, and active keys into the lab.",
                ],
                "variables": [
                    "ENTRY_POINT_LIST_ENDPOINT",
                    "EP_NAME_KEY",
                    "EP_FLOW_ID_KEY",
                    "EP_ACTIVE_KEY",
                ],
            },
            {
                "id": "b",
                "title": "Part B — List Dialed Number Mappings",
                "instruction": "Navigate to List Dialed Number Mappings. Copy the endpoint and mapping keys.",
                "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/dial-number/list-dialed-number-mappings",
                "doc_title": "List Dialed Number Mappings",
                "api_method": "GET",
                "doc_guide": [
                    "Navigate to the List Dialed Number Mappings API.",
                    "Copy the endpoint and paste it into the lab.",
                    "Hit the Run button at the bottom of the API page, then from the response copy and paste the dialled number, entry point id, location, and region id keys into the lab.",
                ],
                "variables": [
                    "DIAL_NUMBER_LIST_ENDPOINT",
                    "DIAL_NUMBER_DN_KEY",
                    "DIAL_NUMBER_EP_ID_KEY",
                    "DIAL_NUMBER_LOCATION_KEY",
                    "DIAL_NUMBER_REGION_KEY",
                ],
            },
        ],
        "field_hints": {
            "ENTRY_POINT_LIST_ENDPOINT": "Paste the List Entry Points endpoint.",
            "EP_NAME_KEY": "On each entry point object — the name key.",
            "EP_FLOW_ID_KEY": "On each entry point object — the flow id key.",
            "EP_ACTIVE_KEY": "On each entry point object — the active key.",
            "DIAL_NUMBER_LIST_ENDPOINT": "Paste the List Dialed Number Mappings endpoint.",
            "DIAL_NUMBER_DN_KEY": "On each mapping record — the dialled number key.",
            "DIAL_NUMBER_EP_ID_KEY": "On each mapping record — the entry point id key.",
            "DIAL_NUMBER_LOCATION_KEY": "On each mapping record — the location key.",
            "DIAL_NUMBER_REGION_KEY": "On each mapping record — the region id key.",
        },
    },
    ("module2", "2.2"): {
        "instruction": "Navigate to List Contact Service Queues. Copy the v2 endpoint and the queue keys from the response.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/contact-service-queues/list-contact-service-queues",
        "doc_title": "List Contact Service Queues",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "doc_guide": [
            "Navigate to the List Contact Service Queues API.",
            "Copy the v2 endpoint and paste it into the lab. Do not copy a v3 endpoint.",
            "Hit the Run button at the bottom of the API page, then from the response copy and paste the name, id, queue type, channel type, queue routing type, and active keys into the lab.",
        ],
        "field_hints": {
            "QUEUE_LIST_ENDPOINT": "Paste the List Contact Service Queues v2 endpoint. Do not use v3.",
            "QUEUE_NAME_KEY": "On each queue object — the name key.",
            "QUEUE_ID_KEY": "On each queue object — the id key.",
            "QUEUE_CONTACT_DIRECTION_KEY": "On each queue object — the queue type key.",
            "QUEUE_TYPE_KEY": "On each queue object — the channel type key.",
            "QUEUE_ROUTING_TYPE_KEY": "On each queue object — the queue routing type key.",
            "QUEUE_STATUS_KEY": "On each queue object — the active key.",
        },
    },
    ("module2", "2.3"): {
        "instruction": "Navigate to List Teams. Copy the endpoint and the team detail keys from the response.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams",
        "doc_title": "List Teams",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "doc_guide": [
            "Navigate to the List Teams API.",
            "Copy the endpoint and paste it into the lab.",
            "Hit the Run button at the bottom of the API page, then from the response copy and paste the name, site name, team type, dialed number, and team status keys into the lab.",
        ],
        "field_hints": {
            "TEAM_LIST_ENDPOINT": "Paste the List Teams endpoint.",
            "TEAM_NAME_KEY": "On each team object — the name key.",
            "TEAM_SITE_NAME_KEY": "On each team object — the site name key.",
            "TEAM_TYPE_KEY": "On each team object — the team type key.",
            "TEAM_DN_KEY": "On each team object — the dialed number key.",
            "TEAM_STATUS_KEY": "On each team object — the team status key.",
        },
    },
    ("module2", "2.4"): {
        "instruction": "Navigate to List Auxiliary Codes. Copy the endpoint and the code keys from the response.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/auxiliary-code/list-auxiliary-codes",
        "doc_title": "List Auxiliary Codes",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "doc_guide": [
            "Navigate to the List Auxiliary Codes API.",
            "Copy the endpoint and paste it into the lab.",
            "Hit the Run button at the bottom of the API page, then from the response copy and paste the name, id, work type code, default code, and active keys into the lab.",
        ],
        "field_hints": {
            "AUX_CODE_LIST_ENDPOINT": "Paste the List Auxiliary Codes endpoint.",
            "AUX_CODE_NAME_KEY": "On each auxiliary code — the name key.",
            "AUX_CODE_ID_KEY": "On each auxiliary code — the id key.",
            "AUX_CODE_TYPE_KEY": "On each auxiliary code — the work type code key.",
            "AUX_CODE_DEFAULT_KEY": "On each auxiliary code — the default code key.",
            "AUX_CODE_STATUS_KEY": "On each auxiliary code — the active key.",
        },
    },
    ("module2", "2.5"): {
        "instruction": "Navigate to List Global Variables. Copy the endpoint and the variable keys from the response.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/list-global-variables",
        "doc_title": "List Global Variables",
        "api_method": "GET",
        "api_base": "WxCC Organization API",
        "doc_guide": [
            "Navigate to the List Global Variables API.",
            "Copy the endpoint and paste it into the lab.",
            "Hit the Run button at the bottom of the API page, then from the response copy and paste the name, default value, variable type, and active keys into the lab.",
        ],
        "field_hints": {
            "GLOBAL_VARIABLE_LIST_ENDPOINT": "Paste the List Global Variables endpoint.",
            "GV_NAME_KEY": "On each global variable — the name key.",
            "GV_VALUE_KEY": "On each global variable — the default value key.",
            "GV_TYPE_KEY": "On each global variable — the variable type key.",
            "GV_STATUS_KEY": "On each global variable — the active key.",
        },
    },
    ("module2", "2.6"): {
        "instruction": "Navigate to Update specific Global Variable by ID. Copy the endpoint and the request method.",
        "doc_url": "https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/update-specific-global-variable-by-id",
        "doc_title": "Update specific Global Variable by ID",
        "api_base": "WxCC Organization API",
        "doc_guide": [
            "Navigate to the Update specific Global Variable by ID API.",
            "Copy the endpoint and paste it into the lab.",
            "From the API page, copy the request method and paste it into the lab.",
        ],
        "field_hints": {
            "GV_UPDATE_ENDPOINT": "Paste the Update specific Global Variable by ID endpoint.",
            "GV_REQUEST_METHOD": "On the Update specific Global Variable by ID API page — the request method.",
        },
    },

    ("module3", "3.1"): {
        "instruction": "Answer a typical contact-volume question: how many customer sessions occurred, on which channels, with what termination type, and inbound vs outbound?",
        "doc_url": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/CSR.md",
        "doc_title": "CSR Data Dictionary",
        "api_method": "POST (GraphQL)",
        "api_base": "WxCC Search API",
        "doc_guide": [
            "Navigate to the CSR Data Dictionary.",
            "Copy the report type into the lab.",
            "From the dictionary, copy and paste the keys for Id, Channel Type, Termination Type, and Direction into the lab.",
        ],
        "field_hints": {
            "CSR_RECORD_TYPE": "Report Type — three-letter code from the CSR dictionary.",
            "CSR_TASK_ID_KEY": "Id field from the CSR Data Dictionary.",
            "CSR_CHANNEL_TYPE_KEY": "Channel Type field from the CSR Data Dictionary.",
            "CSR_TERMINATION_TYPE_KEY": "Termination Type field from the CSR Data Dictionary.",
            "CSR_CALL_DIRECTION_KEY": "Direction field from the CSR Data Dictionary (inbound / outbound).",
        },
    },
    ("module3", "3.2"): {
        "instruction": "Enter the CAR report type and pick activity fields from the CAR Data Dictionary.",
        "doc_url": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/CAR.md",
        "doc_title": "CAR Data Dictionary",
        "api_method": "POST (GraphQL)",
        "api_base": "WxCC Search API",
        "doc_guide": [
            "Navigate to the CAR Data Dictionary.",
            "Copy the report type into the lab.",
            "From the dictionary, copy and paste the keys for Activity Name and Queue Name into the lab.",
        ],
        "field_hints": {
            "CAR_RECORD_TYPE": "Report Type — three-letter code from the CAR dictionary.",
            "CAR_ACTIVITY_NAME_KEY": "Activity Name from the CAR Data Dictionary.",
            "CAR_QUEUE_NAME_KEY": "Queue Name from the CAR Data Dictionary.",
        },
    },
    ("module3", "3.3"): {
        "instruction": "Answer a typical staffing question: which agents were in session, and which teams do they belong to?",
        "doc_url": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/ASR.md",
        "doc_title": "ASR Data Dictionary",
        "api_method": "POST (GraphQL)",
        "api_base": "WxCC Search API",
        "doc_guide": [
            "Navigate to the ASR Data Dictionary.",
            "Copy the report type into the lab.",
            "From the dictionary, copy and paste the keys for Agent Id, Agent Name, and Team Name into the lab.",
        ],
        "field_hints": {
            "ASR_RECORD_TYPE": "Report Type — three-letter code from the ASR dictionary.",
            "ASR_AGENT_ID_KEY": "Agent Id from the ASR Data Dictionary.",
            "ASR_AGENT_NAME_KEY": "Agent Name from the ASR Data Dictionary.",
            "ASR_TEAM_NAME_KEY": "Team Name from the ASR Data Dictionary.",
        },
    },
    ("module3", "3.4"): {
        "instruction": "Enter the AAR report type and pick telephony activity fields from the AAR Data Dictionary.",
        "doc_url": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/AAR.md",
        "doc_title": "AAR Data Dictionary",
        "api_method": "POST (GraphQL)",
        "api_base": "WxCC Search API",
        "doc_guide": [
            "Navigate to the AAR Data Dictionary.",
            "Copy the report type into the lab.",
            "From the dictionary, copy and paste the keys for State and Duration into the lab.",
        ],
        "field_hints": {
            "AAR_RECORD_TYPE": "Report Type — three-letter code from the AAR dictionary.",
            "AAR_ACTIVITY_TYPE_KEY": "State field from the AAR Data Dictionary.",
            "AAR_DURATION_KEY": "Duration field from the AAR Data Dictionary.",
        },
    },
    ("module3", "3.5"): {
        "instruction": "Pick logged-in agent fields from the ASR Data Dictionary. Live state is refreshed with GET /v1/agents/activities.",
        "doc_url": "https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/ASR.md",
        "doc_title": "ASR Data Dictionary",
        "api_method": "POST (GraphQL) + GET /v1/agents/activities",
        "api_base": "WxCC Search + Agents API",
        "doc_guide": [
            "Navigate to the ASR Data Dictionary.",
            "Copy and paste the keys for Is Active and Agent Id into the lab.",
            "Navigate to the [Get Agent Activities API](https://developer.webex.com/webex-contact-center/docs/api/v1/agents/get-agent-activities).",
            "The lab uses Agent Id to match Search rows to Activities rows.",
        ],
        "field_hints": {
            "RT_AGENT_STATE_KEY": "Is Active from the ASR Data Dictionary.",
            "RT_AGENT_ID_KEY": "Agent Id from the ASR Data Dictionary.",
        },
    },
    ("module4", "4.1"): {
        "instruction": "Use List People for user fields, then List Roles and List Licenses to resolve IDs to names.",
        "doc_url": "https://developer.webex.com/docs/api/v1/people/list-people",
        "doc_title": "Control Hub — People",
        "api_method": "GET",
        "api_base": "Webex Platform API (webexapis.com)",
        "field_groups": [
            {
                "id": "a",
                "title": "Part A — List People",
                "instruction": "Open List People. Copy the endpoint and the JSON keys from one person object.",
                "doc_url": "https://developer.webex.com/docs/api/v1/people/list-people",
                "doc_title": "List People",
                "api_method": "GET",
                "api_base": "Webex Platform API",
                "doc_guide": [
                    "Navigate to the List People API.",
                    "Copy the endpoint and paste it into the lab.",
                    "Hit the Run button at the bottom of the API page, then from the response copy and paste the email, display name, status, roles, and licenses keys into the lab.",
                ],
                "variables": [
                    "WEBEX_PEOPLE_ENDPOINT",
                    "PEOPLE_EMAIL_KEY",
                    "PEOPLE_DISPLAY_NAME_KEY",
                    "PEOPLE_STATUS_KEY",
                    "PEOPLE_ROLES_KEY",
                    "PEOPLE_LICENSES_KEY",
                ],
            },
            {
                "id": "b",
                "title": "Part B — List Roles",
                "instruction": "Open List Roles and copy the endpoint. Role id/name keys are standard and handled by the lab.",
                "doc_url": "https://developer.webex.com/docs/api/v1/roles/list-roles",
                "doc_title": "List Roles",
                "api_method": "GET",
                "api_base": "Webex Platform API",
                "doc_guide": [
                    "Navigate to the List Roles API.",
                    "Copy the endpoint and paste it into the lab.",
                ],
                "variables": ["WEBEX_ROLES_ENDPOINT"],
            },
            {
                "id": "c",
                "title": "Part C — List Licenses",
                "instruction": "Open List Licenses and copy the endpoint.",
                "doc_url": "https://developer.webex.com/docs/api/v1/licenses/list-licenses",
                "doc_title": "List Licenses",
                "api_method": "GET",
                "api_base": "Webex Platform API",
                "doc_guide": [
                    "Navigate to the List Licenses API.",
                    "Copy the endpoint and paste it into the lab.",
                ],
                "variables": ["WEBEX_LICENSES_ENDPOINT"],
            },
        ],
        "field_hints": {
            "WEBEX_PEOPLE_ENDPOINT": "Paste the List People endpoint.",
            "PEOPLE_EMAIL_KEY": "List People — email field on each person.",
            "PEOPLE_DISPLAY_NAME_KEY": "List People — display name field.",
            "PEOPLE_STATUS_KEY": "List People — account status field.",
            "PEOPLE_ROLES_KEY": "List People — roles array on each person.",
            "PEOPLE_LICENSES_KEY": "List People — licenses array on each person.",
            "WEBEX_ROLES_ENDPOINT": "Paste the List Roles endpoint.",
            "WEBEX_LICENSES_ENDPOINT": "Paste the List Licenses endpoint.",
        },
    },
    ("module4", "4.2"): {
        "instruction": "Use List Locations for site data, then List Phone Numbers to count numbers per location.",
        "doc_url": "https://developer.webex.com/calling/docs/api/v1/locations/list-locations",
        "doc_title": "Webex Calling — Locations",
        "api_method": "GET",
        "api_base": "Webex Calling API",
        "field_groups": [
            {
                "id": "a",
                "title": "Part A — List Locations",
                "instruction": "Open List Locations. Copy the endpoint and key location fields from the response.",
                "doc_url": "https://developer.webex.com/calling/docs/api/v1/locations/list-locations",
                "doc_title": "List Locations",
                "api_method": "GET",
                "api_base": "Webex Calling API",
                "doc_guide": [
                    "Navigate to the List Locations API.",
                    "Copy the endpoint and paste it into the lab.",
                    "Hit the Run button at the bottom of the API page, then from the response copy and paste the name, id, and address keys into the lab.",
                ],
                "variables": [
                    "WEBEX_LOCATION_ENDPOINT",
                    "LOCATION_NAME_KEY",
                    "LOCATION_ID_KEY",
                    "LOCATION_ADDRESS_KEY",
                ],
            },
            {
                "id": "b",
                "title": "Part B — List Phone Numbers",
                "instruction": "Open Get Phone Numbers and copy the endpoint plus the phone number key.",
                "doc_url": "https://developer.webex.com/calling/docs/api/v1/numbers/get-phone-numbers-for-an-organization-with-given-criteria",
                "doc_title": "Get Phone Numbers",
                "api_method": "GET",
                "api_base": "Webex Calling API",
                "doc_guide": [
                    "Navigate to the Get Phone Numbers API.",
                    "Copy the endpoint and paste it into the lab.",
                    "Hit the Run button at the bottom of the API page, then from the response copy and paste the phone number key into the lab.",
                ],
                "variables": ["WEBEX_PHONE_NUMBERS_ENDPOINT", "PHONE_NUMBER_KEY"],
            },
        ],
        "field_hints": {
            "WEBEX_LOCATION_ENDPOINT": "Paste the List Locations endpoint.",
            "LOCATION_NAME_KEY": "List Locations — name field on each location.",
            "LOCATION_ID_KEY": "List Locations — id field on each location.",
            "LOCATION_ADDRESS_KEY": "List Locations — nested address object on each location.",
            "WEBEX_PHONE_NUMBERS_ENDPOINT": "Paste the Get Phone Numbers endpoint.",
            "PHONE_NUMBER_KEY": "Get Phone Numbers — phone number field on each record.",
        },
    },
    ("module4", "4.3"): {
        "instruction": "Navigate to Retrieve PSTN Connection. Copy the endpoint and paste it into the lab.",
        "doc_url": "https://developer.webex.com/calling/docs/api/v1/pstn/retrieve-pstn-connection-for-a-location",
        "doc_title": "Retrieve PSTN Connection",
        "api_method": "GET",
        "api_base": "Webex Calling API",
        "doc_guide": [
            "Navigate to the Retrieve PSTN Connection API.",
            "Copy the endpoint and paste it into the lab.",
        ],
        "field_hints": {
            "PSTN_CONNECTION_ENDPOINT": "Retrieve PSTN Connection — endpoint with a location id placeholder.",
        },
    },
}


def get_field_hint(module_id: str, step_id: str, var_name: str) -> str | None:
    meta = STEP_META.get((module_id, step_id), {})
    return meta.get("field_hints", {}).get(var_name)


def get_step_field_groups(module_id: str, step_id: str) -> list[dict]:
    return list(STEP_META.get((module_id, step_id), {}).get("field_groups", []))


def get_part_variables(module_id: str, step_id: str, part_id: str) -> list[str]:
    for group in get_step_field_groups(module_id, step_id):
        if group.get("id") == part_id:
            return list(group.get("variables", []))
    return []


def _value_filled(values: dict[str, str], var: str) -> bool:
    value = values.get(var, "")
    if value is None:
        return False
    text = str(value).strip()
    return bool(text) and text != FILL_IN_PLACEHOLDER


def _build_field_groups(meta: dict, values: dict[str, str], step_meta: dict) -> list[dict]:
    raw_groups = meta.get("field_groups", [])
    field_groups: list[dict] = []
    for index, group in enumerate(raw_groups):
        group_id = group.get("id") or chr(ord("a") + index)
        variables = group.get("variables", [])
        prior_vars = [var for g in raw_groups[:index] for var in g.get("variables", [])]
        complete = all(_value_filled(values, var) for var in variables)
        prior_complete = all(_value_filled(values, var) for var in prior_vars)
        if complete:
            access = "complete"
        elif prior_complete or index == 0:
            access = "active"
        else:
            access = "locked"

        group_fields = []
        for var in variables:
            desc = describe_field(var)
            group_fields.append({**desc, "value": values.get(var, "")})

        field_groups.append(
            {
                "id": group_id,
                "title": group.get("title", ""),
                "instruction": group.get("instruction", ""),
                "doc_url": group.get("doc_url"),
                "doc_title": group.get("doc_title"),
                "api_method": group.get("api_method", step_meta.get("api_method")),
                "api_base": group.get("api_base", step_meta.get("api_base")),
                "doc_guide": group.get("doc_guide", []),
                "variables": variables,
                "fields": group_fields,
                "complete": complete,
                "access": access,
            }
        )
    return field_groups


def _humanize(name: str) -> str:
    return " ".join(part.capitalize() for part in name.lower().split("_"))


def describe_field(var_name: str) -> dict:
    if var_name.endswith("_ENDPOINT"):
        prefix = var_name[: -len("_ENDPOINT")]
        return {
            "var": var_name,
            "kind": "endpoint",
            "label": f"{_humanize(prefix)} endpoint",
            "placeholder": ENDPOINT_PLACEHOLDERS.get(var_name, "/{orgId}/v2/resourceName"),
        }
    if var_name.endswith("_METHOD"):
        return {
            "var": var_name,
            "kind": "key",
            "label": "Request method",
            "placeholder": "httpMethod",
        }
    if var_name == "SETUP_BEARER_TOKEN":
        return {
            "var": var_name,
            "kind": "secret",
            "label": FIELD_LABELS.get(var_name, "Bearer token"),
            "placeholder": "Paste admin bearer token from your Developer Portal profile",
        }
    if var_name == "SETUP_ORG_ID":
        return {
            "var": var_name,
            "kind": "key",
            "label": FIELD_LABELS.get(var_name, "Organization ID"),
            "placeholder": "Paste organization ID from your Developer Portal profile",
        }
    if var_name.endswith("_RECORD_TYPE"):
        return {
            "var": var_name,
            "kind": "key",
            "label": "Report Type",
            "placeholder": "XXX",
        }
    if var_name.endswith("_KEY"):
        return {
            "var": var_name,
            "kind": "key",
            "label": FIELD_LABELS.get(var_name, _humanize(var_name[: -len("_KEY")])),
            "placeholder": "key",
        }
    return {
        "var": var_name,
        "kind": "key",
        "label": FIELD_LABELS.get(var_name, _humanize(var_name)),
        "placeholder": "key",
    }


def enrich_step(module_id: str, step: dict, values: dict[str, str]) -> dict:
    meta = STEP_META.get((module_id, step["id"]), {})
    variables = step.get("variables", [])

    display_values = dict(values)
    if module_id == "module0":
        try:
            from config import org_id_from_token
            from lab_credentials import get_stored_org_id, get_stored_token, get_suggested_org_id, has_token

            if has_token():
                display_values["SETUP_BEARER_TOKEN"] = ""
            org = get_stored_org_id() or get_suggested_org_id() or (org_id_from_token(get_stored_token()) or "")
            if org:
                display_values["SETUP_ORG_ID"] = org
        except ImportError:
            pass

    fields = [describe_field(var) for var in variables]
    endpoints = [f for f in fields if f["kind"] == "endpoint"]
    keys = [f for f in fields if f["kind"] == "key" or f["kind"] == "secret"]
    field_groups = _build_field_groups(meta, display_values, meta)

    token_saved = False
    if module_id == "module0":
        try:
            from lab_credentials import has_token

            token_saved = has_token()
        except ImportError:
            pass

    def field_with_value(f):
        payload = {**f, "value": display_values.get(f["var"], ""), "hide_label": module_id == "module0"}
        if f["var"] == "SETUP_BEARER_TOKEN" and token_saved:
            payload["saved"] = True
            payload["placeholder"] = "Token saved — paste again to replace"
        return payload

    return {
        "id": step["id"],
        "label": step["label"],
        "instruction": meta.get("instruction", f"Complete step {step['id']}: {step['label']}."),
        "doc_url": meta.get("doc_url"),
        "doc_title": meta.get("doc_title"),
        "api_method": meta.get("api_method"),
        "api_base": meta.get("api_base"),
        "doc_link_label": meta.get("doc_link_label"),
        "doc_guide": meta.get("doc_guide", []),
        "field_layout": "plain" if module_id == "module0" else "default",
        "keys_section_title": "Field names" if module_id == "module3" else "Response keys",
        "field_groups": field_groups,
        "endpoints": [field_with_value(f) for f in endpoints],
        "keys": [field_with_value(f) for f in keys],
        "variables": variables,
    }
