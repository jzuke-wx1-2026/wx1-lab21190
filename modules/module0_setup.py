"""
Module 0 — Lab Setup

Connect the dashboard to your Webex Contact Center organization using an
admin profile bearer token or a Webex Integration, then your organization ID.
"""

MODULE_ID = "module0"
MODULE_NAME = "Setup"

STEPS = [
    {
        "id": "0.1",
        "label": "Access token",
        "variables": ["SETUP_BEARER_TOKEN"],
    },
    {
        "id": "0.2",
        "label": "Organization ID",
        "variables": ["SETUP_ORG_ID"],
    },
]
