# Module 4 — Webex Control Hub & Webex Calling APIs

**Answers:** dashboard step forms (Module 4)  
**Reference:** `modules/module4_webex_apis.py` (logic only — do not edit)  
**Estimated time:** 20 minutes

## Objective

Extend the dashboard beyond Contact Center by integrating Webex Platform APIs for people, calling locations, and PSTN/carrier/trunk configuration.

---

## Step 4.1 — Control Hub User Info

### Part A — List People

1. Navigate to the [List People API](https://developer.webex.com/docs/api/v1/people/list-people).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the email, display name, status, roles, and licenses keys into the lab.

**Fill in:** Webex People endpoint, Emails, Display Name, Status, Roles, Licenses

### Part B — List Roles

1. Navigate to the [List Roles API](https://developer.webex.com/docs/api/v1/roles/list-roles).
2. Copy the endpoint and paste it into the lab.

**Fill in:** Webex Roles endpoint

### Part C — List Licenses

1. Navigate to the [List Licenses API](https://developer.webex.com/docs/api/v1/licenses/list-licenses).
2. Copy the endpoint and paste it into the lab.

**Fill in:** Webex Licenses endpoint

**Dashboard unlocks:** User Info tab — Control Hub people table

---

## Step 4.2 — Webex Calling Locations

### Part A — List Locations

1. Navigate to the [List Locations API](https://developer.webex.com/calling/docs/api/v1/locations/list-locations).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the name, id, and address keys into the lab.

**Fill in:** Webex Location endpoint, Name, Id, Address

### Part B — List Phone Numbers

1. Navigate to the [Get Phone Numbers API](https://developer.webex.com/calling/docs/api/v1/numbers/get-phone-numbers-for-an-organization-with-given-criteria).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the phone number key into the lab.

**Fill in:** Webex Phone Numbers endpoint, Phone Number

**Dashboard unlocks:** Locations tab

---

## Step 4.3 — PSTN / Carrier / Trunk

1. Navigate to the [Retrieve PSTN Connection API](https://developer.webex.com/calling/docs/api/v1/pstn/retrieve-pstn-connection-for-a-location).
2. Copy the endpoint and paste it into the lab.

**Fill in:** Pstn Connection endpoint

**Dashboard unlocks:** PSTN tab — entry point numbers with location, connection/carrier, and country

Only PSTN telephony numbers that are both mapped to a Module 2 entry point and present in the Webex Calling phone number inventory are listed.

---

## Developer Portal Reference

- [List People](https://developer.webex.com/docs/api/v1/people/list-people)
- [List Roles](https://developer.webex.com/docs/api/v1/roles/list-roles)
- [List Licenses](https://developer.webex.com/docs/api/v1/licenses/list-licenses)
- [List Locations](https://developer.webex.com/calling/docs/api/v1/locations/list-locations)
- [Get Phone Numbers](https://developer.webex.com/calling/docs/api/v1/numbers/get-phone-numbers-for-an-organization-with-given-criteria)
- [Retrieve PSTN Connection](https://developer.webex.com/calling/docs/api/v1/pstn/retrieve-pstn-connection-for-a-location)

## Congratulations!

You have built a custom Webex Contact Center dashboard that integrates:

- User and organizational configuration APIs
- GraphQL historical and real-time reporting
- Webex Control Hub and Webex Calling visibility
