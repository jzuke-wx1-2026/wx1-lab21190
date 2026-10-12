# Module 0 — Lab Setup

Connect the dashboard to your Webex Contact Center organization. Complete step **0.1** with either an **admin profile token** or a **Webex Integration**, then save your **organization ID** in step **0.2**.

Credentials are saved locally in `data/lab_credentials.json` (gitignored). The lab never stores a client secret, authorization code, or refresh token.

## What you will do

1. Sign in to [developer.webex.com](https://developer.webex.com) as a WxCC admin.
2. Provide an access token using one of the options in step 0.1.
3. Copy your **organization ID** and verify connectivity.

## Step 0.1 — Access token

Choose **Admin token** or **Integration (advanced)**. Either option completes this step.

### Admin token

1. Go to [developer.webex.com](https://developer.webex.com) and sign in with your Webex Contact Center admin account.
2. Click your profile (avatar or name) in the top-right corner.
3. Copy the bearer token shown in your profile.
4. Paste the token string only — do not include the word Bearer.

**Fill in:** Admin bearer token

### Integration (advanced)

1. Go to [developer.webex.com/my-apps/new](https://developer.webex.com/my-apps/new) and login as a local admin.
2. Under Integrations, click Create an Integration.
3. Fill out the required fields: Integration Name, Icon, and App Hub Description.
4. Fill in Redirect URI with the one provided below: `http://127.0.0.1:5000/setup/callback`.
5. Add the proper scopes: for each scope chip, click to copy the name, then find and check it off in your integration.
6. Once scopes are added, click Add Integration at the bottom of the page.
7. Your integration will be created and you will now see your client information.
8. Copy the Client ID from your integration, and paste it into the Client ID field in the lab.
9. Copy the Client Secret from your integration, and paste it into the Client Secret field in the lab. The lab does not store the secret.
10. Under OAuth Settings, copy the full OAuth Authorization URL in the black box, and paste it into the OAuth Authorization URL field in the lab.
11. Click the Authorize in Webex button, then login with the admin user who created the integration.
12. Hit the Accept button to authorize the integration.
13. On the pop-up window, click the Copy code button, and paste this into the Authorization code field in the lab.
14. You can close the pop-up window, then click Generate Token.

The Redirect URI must match exactly — `127.0.0.1` and `localhost` are different.

**Fill in:** Client ID, Client Secret, OAuth Authorization URL, Authorization code

Required scopes (click each chip in the lab to copy it):

- `cjp:config` — Contact Center configuration APIs
- `cjp:config_read` — Read users, queues, teams, and other org data
- `cjp:config_write` — Update global variables (Module 2)
- `spark:people_read` — Identify the authorizing admin and organization
- `spark-admin:people_read` — List Control Hub people (Module 4)
- `spark-admin:roles_read` — Resolve role names (Module 4)
- `spark-admin:licenses_read` — Resolve license names (Module 4)
- `spark-admin:telephony_config_read` — Locations and phone numbers (Module 4)
- `spark-admin:telephony_pstn_read` — PSTN connection per location (Module 4 step 4.3)

The lab stores only the resulting access token. If a required scope is missing, step 0.1 does not complete. Edit the integration, check the highlighted chips, copy the new OAuth Authorization URL, authorize again, and generate a new token (the previous code cannot be reused).

## Step 0.2 — Organization ID

1. In the [developer portal](https://developer.webex.com), click your profile (avatar or name) in the top-right corner, then copy your organization ID.
2. The org ID must belong to the same organization as the token from step 0.1 (admin profile or integration).
3. When you save this step, the lab calls the [WxCC List Users API](https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users) to confirm your bearer token is valid.
4. Once this step is complete, you can close your developer portal integration page.

**Fill in:** Organization ID

## After setup

The **Connected** card includes an **i** button that explains whether you used an admin profile token or a Webex Integration.

When both steps are complete, Modules 1–4 unlock and live API data loads as you progress. Use **Continue to Users** or the Users tab to move on.

Use **Reset module** on the Setup tab to clear credentials and start over.

## Developer Portal Reference

- [Developer portal](https://developer.webex.com)
- [Create a Webex Integration](https://developer.webex.com/my-apps/new)
- [List Users](https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users)
