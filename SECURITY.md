# Security

This project is **sample lab code**. It is not for production. Use it only against a Webex Contact Center organization you control.

## Do not commit secrets

Never add any of the following to git:

- Bearer tokens, authorization codes, refresh tokens
- Integration Client Secret
- `.env` (copy from `.env.example` only)
- Files under `data/` (`lab_credentials.json`, `lab_answers.json`)

The dashboard stores credentials locally in `data/`, which is gitignored. That folder is for your machine only.

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) on this repository. Do not open a public issue that includes tokens or org data.

If a token was committed or pasted into a ticket, revoke it in the Developer Portal (or GitHub, if it was a PAT) and generate a new one.
