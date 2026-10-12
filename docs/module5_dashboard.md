# Module 5 — Full Dashboard

**Answers:** none — this is a view-only page  
**Estimated time:** 5 minutes

## Objective

Review every dashboard you unlocked while completing Modules 1–4, on a separate page without the lab forms. After a module is complete, its section becomes available here even if you move on.

## How to use it

1. Complete **Setup**, then finish at least one of Modules 1–4.
2. Click **Open Full Dashboard** in the lab header, or **View in Full Dashboard** after completing a module. The dashboard opens in a new browser tab at `/dashboard`.
3. Inner tabs appear as you complete each module: Users, Org Data, Reports, Webex APIs. Incomplete modules stay visible but locked. Org Data and Webex APIs each have their own inner tabs (entry points / queues / … and user info / locations / PSTN).
4. Click the **i** button on a section to see:
   - HTTP method and endpoint(s)
   - How the lab turns those responses into table rows (ID-to-name matching, GraphQL grouping, and so on)
   - For report cards: the GraphQL query and how the large number and chips are counted

Real-time agents still refresh with **GET `/v1/agents/activities`**.
