# Answer key — LAB-21190

The dashboard reads this file to check step answers. **Spoiler:** skip this file if you want to complete the lab from the Developer Portal yourself.

Values can vary slightly by API version and region. If a check fails, compare your response to the current Developer Portal.

Participants complete steps in the **dashboard forms** (saved to `data/lab_answers.json`), not in source files under `modules/`.

## Module 1 — Users

```python
USERS_LIST_ENDPOINT = "/{org_id}/v2/user"
USER_FIRST_NAME_KEY = "firstName"
USER_LAST_NAME_KEY = "lastName"
USER_EMAIL_KEY = "email"
AGENT_PROFILE_ID_KEY = "agentProfileId"
MULTIMEDIA_PROFILE_ID_KEY = "multimediaProfileId"
USER_PROFILE_ID_KEY = "userProfileId"
AGENT_PROFILE_LIST_ENDPOINT = "/{org_id}/v2/agent-profile"
AGENT_PROFILE_NAME_KEY = "name"
USER_PROFILE_LIST_ENDPOINT = "/{org_id}/v3/user-profile"
USER_PROFILE_NAME_KEY = "name"
SKILL_PROFILE_LIST_ENDPOINT = "/{org_id}/v2/skill-profile"
SKILL_PROFILE_ID_KEY = "id"
SKILL_NAME_KEY = "name"
TEAM_LIST_ENDPOINT = "/{org_id}/v2/team"
TEAM_IDS_KEY = "userIds"
TEAM_NAME_KEY = "name"
MULTIMEDIA_PROFILE_LIST_ENDPOINT = "/{org_id}/v2/multimedia-profile"
MULTIMEDIA_PROFILE_NAME_KEY = "name"
CHANNEL_TELEPHONY_KEY = "telephony"
CHANNEL_CHAT_KEY = "chat"
CHANNEL_EMAIL_KEY = "email"
CHANNEL_SOCIAL_KEY = "social"
```

## Module 2 — Organizational Data

```python
ENTRY_POINT_LIST_ENDPOINT = "/{org_id}/v2/entry-point"
EP_NAME_KEY = "name"
EP_FLOW_ID_KEY = "flowId"
EP_QUEUE_ID_KEY = "queueId"
DIAL_NUMBER_LIST_ENDPOINT = "/{org_id}/v3/dial-number"
DIAL_NUMBER_DN_KEY = "dialledNumber"
DIAL_NUMBER_EP_ID_KEY = "entryPointId"
DIAL_NUMBER_LOCATION_KEY = "location"
DIAL_NUMBER_REGION_KEY = "regionId"
EP_ACTIVE_KEY = "active"
QUEUE_LIST_ENDPOINT = "/{org_id}/v2/contact-service-queue"
QUEUE_NAME_KEY = "name"
QUEUE_ID_KEY = "id"
QUEUE_CONTACT_DIRECTION_KEY = "queueType"
QUEUE_TYPE_KEY = "channelType"
QUEUE_ROUTING_TYPE_KEY = "queueRoutingType"
QUEUE_STATUS_KEY = "active"
GLOBAL_VARIABLE_LIST_ENDPOINT = "/{org_id}/v2/cad-variable"
GV_NAME_KEY = "name"
GV_VALUE_KEY = "defaultValue"
GV_TYPE_KEY = "variableType"
GV_STATUS_KEY = "active"
AUX_CODE_LIST_ENDPOINT = "/{org_id}/v2/auxiliary-code"
AUX_CODE_NAME_KEY = "name"
AUX_CODE_ID_KEY = "id"
AUX_CODE_TYPE_KEY = "workTypeCode"
AUX_CODE_DEFAULT_KEY = "defaultCode"
AUX_CODE_STATUS_KEY = "active"
TEAM_LIST_ENDPOINT = "/{org_id}/v2/team"
TEAM_NAME_KEY = "name"
TEAM_SITE_NAME_KEY = "siteName"
TEAM_TYPE_KEY = "teamType"
TEAM_DN_KEY = "dialedNumber"
TEAM_STATUS_KEY = "teamStatus"
GV_UPDATE_ENDPOINT = "/{org_id}/cad-variable/{variable_id}"
GV_REQUEST_METHOD = "PUT"
```

## Module 3 — GraphQL Reports

Field keys for steps 3.1–3.5 are validated against `data/report_data_dictionary.json` when present, or against this answer key. Accept full dictionary paths or leaf names. Report Type codes are case-insensitive.

GraphQL query roots and response array keys are hardcoded in `modules/module3_graphql.py` (not lab steps). Search and Activities calls use the Setup org ID so the same queries work across bearer tokens and organizations.

```python
# Hardcoded in module (not student steps):
# SEARCH_QUERY_TYPE_TASK = "taskDetails"
# SEARCH_QUERY_TYPE_AGENT = "agentSession"
# SEARCH_RESPONSE_TASKS_KEY = "tasks"
# SEARCH_RESPONSE_AGENTS_KEY = "agentSessions"
CSR_RECORD_TYPE = "CSR"
CSR_TASK_ID_KEY = "id"
CSR_CHANNEL_TYPE_KEY = "channelType"
CSR_TERMINATION_TYPE_KEY = "terminationType"
CSR_CALL_DIRECTION_KEY = "direction"
CAR_RECORD_TYPE = "CAR"
CAR_ACTIVITY_NAME_KEY = "activityName"
CAR_QUEUE_NAME_KEY = "queueName"
ASR_RECORD_TYPE = "ASR"
ASR_AGENT_ID_KEY = "agentId"
ASR_AGENT_NAME_KEY = "agentName"
ASR_TEAM_NAME_KEY = "teamName"
AAR_RECORD_TYPE = "AAR"
AAR_ACTIVITY_TYPE_KEY = "state"
AAR_DURATION_KEY = "duration"
RT_AGENT_STATE_KEY = "isActive"
RT_AGENT_ID_KEY = "agentId"
```

## Module 4 — Webex APIs

```python
WEBEX_PEOPLE_ENDPOINT = "/people"
PEOPLE_EMAIL_KEY = "emails"
PEOPLE_DISPLAY_NAME_KEY = "displayName"
PEOPLE_STATUS_KEY = "status"
PEOPLE_ROLES_KEY = "roles"
PEOPLE_LICENSES_KEY = "licenses"
WEBEX_ROLES_ENDPOINT = "/roles"
WEBEX_LICENSES_ENDPOINT = "/licenses"
WEBEX_LOCATION_ENDPOINT = "/locations"
LOCATION_NAME_KEY = "name"
LOCATION_ID_KEY = "id"
LOCATION_ADDRESS_KEY = "address"
WEBEX_PHONE_NUMBERS_ENDPOINT = "/telephony/config/numbers"
PHONE_NUMBER_KEY = "phoneNumber"
PSTN_CONNECTION_ENDPOINT = "/telephony/pstn/locations/{location_id}/connection"
```

## Notes for Proctors

- Exact endpoints should be verified in the Developer Portal API endpoint documentation before the event
- **List APIs use versioned paths:** queues → `/v2/contact-service-queue` (v1/v3 deprecated); auxiliary codes → `/v2/auxiliary-code`; entry points → `/v2/entry-point`; dial numbers → `/v3/dial-number`; global variables list → `/v2/cad-variable`; update variable → `/cad-variable/{id}` (v1 PUT)
- GraphQL field names may differ between API versions — use the portal's schema explorer
- Module 4 PSTN data only appears for locations with LOCAL_GATEWAY or similar PSTN types configured
- Region-specific base URLs: US1 = `wxcc-us1`, EU1 = `wxcc-eu1`, APJC = `wxcc-apjc`
