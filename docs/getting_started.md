# Getting Started

## Lab Overview

**Duration:** 120 minutes  
**Session ID:** LAB-21190  
**Title:** Building Custom Webex Contact Center Dashboards: Organization Visibility and Control with APIs

In this hands-on lab you will build a custom, real-time dashboard that provides full visibility and control over your Webex Contact Center environment. The dashboard code and logic are pre-built — your job is to connect it to the APIs by filling in endpoints and response payload keys.

## Learning Objectives

By the end of this lab you will be able to:

- Authenticate with your admin bearer token from the Developer Portal profile
- Use the Users API to retrieve agent configuration (profiles, skills, teams)
- Pull organizational data (entry points, queues, global variables)
- Query historical and real-time reports using the GraphQL Search API
- Extend visibility with Webex Control Hub and Webex Calling APIs
- Review completed modules together in a Full Dashboard, with info buttons explaining each API call

## Prerequisites

- A Webex Contact Center organization with admin access
- Python 3.10+ installed locally
- A Webex Developer Portal account (https://developer.webex.com)
- Basic familiarity with REST APIs and JSON

## Step 1 — Get Your Admin Bearer Token & Org ID

Use an admin profile bearer token, **or** create a Webex Integration in Setup (advanced). You need a Contact Center admin on **your** organization.

1. Go to [developer.webex.com](https://developer.webex.com) and sign in with your **Webex Contact Center admin** account.
2. Click your **profile** (avatar or name) in the top-right corner.
3. Copy your **bearer token** and **organization ID** from the profile menu (or create the Integration from the Setup tab instead).
4. You will paste these into the dashboard **Setup** module after starting the lab server.

!!! tip "Admin account required"
    The token must belong to an admin who can access WxCC configuration APIs. If API calls fail with 403, confirm you are signed in with the correct admin account.

## Step 2 — Set Up the Lab Environment

```powershell
git clone https://github.com/jzuke-wx1-2026/wx1-lab21190.git
cd wx1-lab21190
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

The `.env` file is optional for local API base URLs. **Access token and org ID are configured in the dashboard Setup module** (recommended). Do not commit `.env` or files under `data/`.

## Step 3 — Start the Dashboard

```powershell
python app.py
```

Open **http://127.0.0.1:5000**. You should see the dashboard with a progress bar at the top showing 0% complete.

## Step 4 — Complete Setup, Then Begin the Lab

1. Open the **Setup** module tab (selected by default).
2. In step **0.1**, paste an **admin profile bearer token**, or use **Integration (advanced)**: create the integration, paste **Client ID** and **Client Secret**, paste the **OAuth Authorization URL**, click **Authorize in Webex**, then paste the **authorization code** from the pop-up and **Generate Token**.
3. Copy your **organization ID** from the Developer Portal profile menu and save (step **0.2**).
4. When setup is complete, continue with the **Users** module and the remaining tabs.

See [Module 0 — Lab Setup](module0_setup.md) for detailed instructions.

For each lab module step, follow the numbered instructions in the blue box:

1. Navigate to the named API (the API name is a hyperlink in the lab).
2. Copy the **endpoint** (when shown) and paste it into the form.
3. Hit **Run** on the API page, then copy the **JSON keys** from the response into the lab.
4. Click **Check & save step**. When a step is complete, the lab moves to the next step. When a module is complete, use **Continue to …** to open the next module.

Your answers are saved to `data/lab_answers.json` on disk, so progress is kept if you reload the page or restart the lab server.

See the matching guide in `docs/` for step-by-step hints.

## Lab Modules

| # | Module | Est. Time | File |
|---|--------|-----------|------|
| 0 | Setup | 5 min | `modules/module0_setup.py` |
| 1 | Users | 25 min | `modules/module1_users.py` |
| 2 | Organizational Data | 25 min | `modules/module2_org_data.py` |
| 3 | GraphQL Reports | 30 min | `modules/module3_graphql.py` |
| 4 | Control Hub & Webex Calling | 25 min | `modules/module4_webex_apis.py` |
| 5 | Full Dashboard | 5 min | `/dashboard` (opens in a new tab) |
| — | Wrap-up & Q&A | 10 min | — |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Verify the access token is valid and not expired. Re-run **Setup** steps 0.1–0.2 (admin token or a new integration authorization code), or update `.env`. Copy a fresh token from your Developer Portal profile (paste the token only, not `Bearer`). Run `python scripts/check_token.py` to probe the users API. |
| 403 Forbidden (other) | Check integration scopes match the required list |
| Empty data returned | Confirm org ID is correct for your region |
| Progress not updating | Click **Save step** after filling in fields, or hard-refresh the browser |
| Region mismatch | Update `WXCC_ORG_BASE_URL` in `.env` (e.g., `wxcc-eu1` for EU) |
