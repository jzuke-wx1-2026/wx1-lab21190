# Module 3 — GraphQL for Historical and Real-Time Reports

**Answers:** dashboard step forms (Module 3)  
**Reference:** `modules/module3_graphql.py` (logic only — do not edit)  
**Estimated time:** 25 minutes

## Objective

Use the Webex Contact Center GraphQL Search API to answer typical business questions about contacts and agents, then keep a live agent-state table current with the Activities API.

Queries use the **organization ID from Setup**. You may enter the full dictionary path (e.g. `activities.nodes.queueName`) or the leaf name (e.g. `queueName`).

---

## Step 3.1 — CSR Report Query

1. Navigate to the [CSR Data Dictionary](https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/CSR.md).
2. Copy the report type into the lab.
3. From the dictionary, copy and paste the keys for Id, Channel Type, Termination Type, and Direction into the lab.

**Fill in:** Report Type, Id, Channel Type, Termination Type, Call Direction

**Dashboard unlocks:** CSR card with volume, channel mix, termination-type mix, and inbound/outbound mix

---

## Step 3.2 — CAR Report Query

1. Navigate to the [CAR Data Dictionary](https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/CAR.md).
2. Copy the report type into the lab.
3. From the dictionary, copy and paste the keys for Activity Name and Queue Name into the lab.

**Fill in:** Report Type, Activity Name, Queue Name

**Dashboard unlocks:** More customer details (click an Interaction ID to view CAR events)

---

## Step 3.3 — ASR Report Query

1. Navigate to the [ASR Data Dictionary](https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/ASR.md).
2. Copy the report type into the lab.
3. From the dictionary, copy and paste the keys for Agent Id, Agent Name, and Team Name into the lab.

**Fill in:** Report Type, Agent Id, Agent Name, Team Name

**Dashboard unlocks:** ASR card with total logged-in time, unique-agent count, and team breakdown

---

## Step 3.4 — AAR Report Query

1. Navigate to the [AAR Data Dictionary](https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/AAR.md).
2. Copy the report type into the lab.
3. From the dictionary, copy and paste the keys for State and Duration into the lab.

**Fill in:** Report Type, State, Duration

**Dashboard unlocks:** More agent details

---

## Step 3.5 — Real-Time Agent States

1. Navigate to the [ASR Data Dictionary](https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/ASR.md).
2. Copy and paste the keys for Is Active and Agent Id into the lab.
3. Navigate to the [Get Agent Activities API](https://developer.webex.com/webex-contact-center/docs/api/v1/agents/get-agent-activities).
4. The lab uses Agent Id to match Search rows to Activities rows.

**Fill in:** Is Active, Agent Id

**Dashboard unlocks:** Real-time table (polls every 10 seconds)

---

## Developer Portal Reference

- [CSR Data Dictionary](https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/CSR.md)
- [CAR Data Dictionary](https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/CAR.md)
- [ASR Data Dictionary](https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/ASR.md)
- [AAR Data Dictionary](https://github.com/WebexSamples/webex-contact-center-api-samples/blob/main/reporting-samples/graphql-sample/DataDictionary/AAR.md)
- [Get Agent Activities](https://developer.webex.com/webex-contact-center/docs/api/v1/agents/get-agent-activities)
- [Getting Started with Search API](https://developer.webex.com/webex-contact-center/docs/getting-started-with-search-api)
