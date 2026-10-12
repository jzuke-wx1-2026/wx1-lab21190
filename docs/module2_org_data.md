# Module 2 — Organizational Data

**Answers:** dashboard step forms (Module 2)  
**Reference:** `modules/module2_org_data.py` (logic only — do not edit)  
**Estimated time:** 25 minutes

## Objective

Add organizational visibility to the dashboard: entry points (channels), queues, teams, auxiliary codes, global variables, and the ability to update a global variable value.

---

## Step 2.1 — Entry Points / Channels

### Part A — List Entry Points

1. Navigate to the [List Entry Points API](https://developer.webex.com/webex-contact-center/docs/api/v1/entry-point/list-entry-points).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the name, flow id, and active keys into the lab.

**Fill in:** Entry Point List endpoint, Name, Flow Id, Active

### Part B — List Dialed Number Mappings

1. Navigate to the [List Dialed Number Mappings API](https://developer.webex.com/webex-contact-center/docs/api/v1/dial-number/list-dialed-number-mappings).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the dialled number, entry point id, location, and region id keys into the lab.

**Fill in:** Dial Number List endpoint, Dialled Number, Entry Point Id, Location, Region Id

**Dashboard unlocks:** Entry Points / Channels table

The dialed number (DN) is not on the entry point object itself — it comes from List Dialed Number Mappings. Flow names resolve automatically; you do not need a List Flows step.

---

## Step 2.2 — Queue Information

1. Navigate to the [List Contact Service Queues API](https://developer.webex.com/webex-contact-center/docs/api/v1/contact-service-queues/list-contact-service-queues).
2. Copy the v2 endpoint and paste it into the lab. Do not copy a v3 endpoint.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the name, id, queue type, channel type, queue routing type, and active keys into the lab.

**Fill in:** Queue List endpoint, Name, Id, Queue Type, Channel Type, Queue Routing Type, Active

**Dashboard unlocks:** Queues table

---

## Step 2.3 — Team Details

1. Navigate to the [List Teams API](https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the name, site name, team type, dialed number, and team status keys into the lab.

**Fill in:** Team List endpoint, Name, Site Name, Team Type, Dialed Number, Team Status

**Dashboard unlocks:** Teams table

Dialed number applies to capacity-based teams. Agent-based teams show `—` for DN.

---

## Step 2.4 — Auxiliary Codes

1. Navigate to the [List Auxiliary Codes API](https://developer.webex.com/webex-contact-center/docs/api/v1/auxiliary-code/list-auxiliary-codes).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the name, id, work type code, default code, and active keys into the lab.

**Fill in:** Aux Code List endpoint, Name, Id, Work Type Code, Default Code, Active

**Dashboard unlocks:** Auxiliary Codes table

---

## Step 2.5 — Global Variables

1. Navigate to the [List Global Variables API](https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/list-global-variables).
2. Copy the endpoint and paste it into the lab.
3. Hit the Run button at the bottom of the API page, then from the response copy and paste the name, default value, variable type, and active keys into the lab.

**Fill in:** Global Variable List endpoint, Name, Default Value, Variable Type, Active

**Dashboard unlocks:** Global Variables table

---

## Step 2.6 — Update Global Variable

1. Navigate to the [Update specific Global Variable by ID API](https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/update-specific-global-variable-by-id).
2. Copy the endpoint and paste it into the lab.
3. From the API page, copy the request method and paste it into the lab.

**Fill in:** Gv Update endpoint, Request method

**Dashboard unlocks:** Edit buttons on global variable rows

Update a test variable you create for the lab. Avoid changing production or system-defined variables unless your instructor directs you to.

---

## Developer Portal Reference

- [List Entry Points](https://developer.webex.com/webex-contact-center/docs/api/v1/entry-point/list-entry-points)
- [List Dialed Number Mappings](https://developer.webex.com/webex-contact-center/docs/api/v1/dial-number/list-dialed-number-mappings)
- [List Contact Service Queues](https://developer.webex.com/webex-contact-center/docs/api/v1/contact-service-queues/list-contact-service-queues)
- [List Teams](https://developer.webex.com/webex-contact-center/docs/api/v1/team/list-teams)
- [List Auxiliary Codes](https://developer.webex.com/webex-contact-center/docs/api/v1/auxiliary-code/list-auxiliary-codes)
- [List Global Variables](https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/list-global-variables)
- [Update specific Global Variable by ID](https://developer.webex.com/webex-contact-center/docs/api/v1/global-variables/update-specific-global-variable-by-id)
