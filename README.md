# LAB-21190 — Building Custom Webex Contact Center Dashboards

A 120-minute hands-on lab where you build a real-time dashboard by filling in API endpoints and response payload keys across four modules, then review everything in a Full Dashboard.

**Not for production use.** Educational and demonstration only. Use your own Webex Contact Center admin account and organization.

## Quick Start

```powershell
git clone https://github.com/jzuke-wx1-2026/wx1-lab21190.git
cd wx1-lab21190

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python app.py
```

On macOS/Linux, use `python3`, `source venv/bin/activate`, and `cp .env.example .env`.

Open **http://127.0.0.1:5000**. Complete **Setup** first (admin profile token **or** Webex Integration, then organization ID), then Modules 1–4. Use **Open Full Dashboard** to review completed sections.

Do not commit `.env` or anything in `data/`. Those files hold your token and answers.

## Lab Structure

| Module | File | Focus |
|--------|------|-------|
| 0 — Setup | `modules/module0_setup.py` | Admin token or Webex Integration, then org ID |
| 1 — Users | `modules/module1_users.py` | List users, profiles, skills, teams, channel types |
| 2 — Org Data | `modules/module2_org_data.py` | Entry points, queues, teams, aux codes, global variables |
| 3 — GraphQL | `modules/module3_graphql.py` | CSR, CAR, ASR, AAR, real-time agent states |
| 4 — Webex APIs | `modules/module4_webex_apis.py` | Control Hub people, locations, PSTN/trunk |
| 5 — Full Dashboard | `/dashboard` | Combined view of completed modules |

## How It Works

1. Complete **Setup** — paste an admin profile token **or** create a Webex Integration, then save your organization ID.
2. Follow the blue-box steps on each module tab. Paste endpoints and JSON keys from the named APIs.
3. Click **Check & save step**. Answers are stored locally in `data/lab_answers.json` and survive reloads.
4. The progress bar updates and live dashboard sections unlock as you go.

## Required Access

Sign in to the [Webex Developer Portal](https://developer.webex.com) with a **Webex Contact Center admin** account. All API calls run as that admin against **your** organization. Updating a global variable in Module 2 writes to that org — use a test variable.

## Project Layout

```
├── modules/                # API logic (do not edit during the lab)
├── data/                   # Saved answers + credentials (runtime, gitignored)
├── app.py                  # Flask dashboard server
├── config.py               # Environment configuration
├── progress.py             # Step completion tracker
├── lab_*.py                # Dashboard forms, validation, and answer storage
├── api/client.py           # HTTP client helpers
├── templates/              # Dashboard HTML
├── static/                 # CSS and JavaScript
├── docs/                   # Lab guide documentation
├── scripts/check_token.py  # Optional credential troubleshooting
└── solutions/              # Answer key used for local step checking (spoiler)
```

## Documentation

See `docs/` for step-by-step instructions. Start with [Getting Started](docs/getting_started.md). Report security issues as described in [SECURITY.md](SECURITY.md).

## License

This project is licensed under the [MIT License](LICENSE).

**Not for production use.** Use at your own risk.
