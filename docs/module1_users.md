# Module 1 — Users

**Answers:** dashboard step forms (Module 1)  
**Reference:** `modules/module1_users.py` (logic only — do not edit)  
**Estimated time:** 25 minutes

## Objective

Build the Users panel of the dashboard by progressively adding user data — from basic name/email through profiles, channel types, skills, and teams.

Each step uses **list-all** APIs. Copy the **endpoint** and **keys** from the JSON response into the lab.

---

## Step 1.1 — List Users API

1. Navigate to the [List Users API](https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users).
2. Copy the endpoint and paste it into the lab.

**Fill in:** Users List endpoint

**Dashboard unlocks:** Users table with name columns

---

## Step 1.2 — Name & Email Fields

1. From the [List Users API](https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users), hit the Run button at the bottom of the page.
2. From the response, locate the details for one user, then copy and paste the first name, last name, and email response keys into the lab.

**Fill in:** First Name, Last Name, Email

**Dashboard unlocks:** Email column in the users table

---

## Step 1.3 — Profile Information

### Part A — Profile IDs (List Users)

1. From the same List Users response generated in the previous step, locate the keys for the agent, multimedia, and user profile IDs.
2. Copy and paste those keys into the lab.

**Fill in:** Agent Profile Id, Multimedia Profile Id, User Profile Id

### Part B — List Desktop Profiles

1. Navigate to the [List Desktop Profiles API](https://developer.webex.com/webex-contact-center/docs/api/v1/desktop-profile/list-desktop-profiles).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy the name key and paste it into the lab.

**Fill in:** Agent Profile List endpoint, Name

### Part C — List User Profiles

1. Navigate to the [List User Profiles API](https://developer.webex.com/webex-contact-center/docs/api/v1/user-profiles/list-user-profiles).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy the name key and paste it into the lab.

**Fill in:** User Profile List endpoint, Name

### Part D — List Multimedia Profiles

1. Navigate to the [List Multimedia Profiles API](https://developer.webex.com/webex-contact-center/docs/api/v1/multimedia-profile/list-multimedia-profiles).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy the name key and paste it into the lab.

**Fill in:** Multimedia Profile List endpoint, Name

**Dashboard unlocks:** Agent, multimedia, and user profile name columns

---

## Step 1.4 — Contact Channel Types

1. From the same List Multimedia Profiles response generated in the previous step, copy and paste the keys for telephony, chat, email, and social into the lab.

**Fill in:** Telephony, Chat, Email, Social

**Dashboard unlocks:** Channel Types column

---

## Step 1.5 — Skill Information

1. Navigate to the [List Skill Profiles API](https://developer.webex.com/webex-contact-center/docs/api/v1/skill-profile/list-skill-profiles).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste both id and name keys into the lab.

**Fill in:** Skill Profile List endpoint, Id, Name

**Dashboard unlocks:** Skill Profile column in the users table

---

## Step 1.6 — Team Information

List Users does not include team IDs. Join membership from each team's array of user IDs.

### Part A — List Teams

1. Navigate to the [List Teams API](https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the name key into the lab.

**Fill in:** Team List endpoint, Name

### Part B — User IDs

1. From the same List Teams response generated in the previous step, locate the key that holds an array of user IDs, then copy and paste that key into the lab.

**Fill in:** User IDs

**Dashboard unlocks:** Teams column in the users table

---

## Developer Portal Reference

- [List Users](https://developer.webex.com/webex-contact-center/docs/api/v1/users/list-users)
- [List Desktop Profiles](https://developer.webex.com/webex-contact-center/docs/api/v1/desktop-profile/list-desktop-profiles)
- [List User Profiles](https://developer.webex.com/webex-contact-center/docs/api/v1/user-profiles/list-user-profiles)
- [List Multimedia Profiles](https://developer.webex.com/webex-contact-center/docs/api/v1/multimedia-profile/list-multimedia-profiles)
- [List Skill Profiles](https://developer.webex.com/webex-contact-center/docs/api/v1/skill-profile/list-skill-profiles)
- [List Teams](https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams)
