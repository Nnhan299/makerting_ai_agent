"""Native Streamlit navigation for the Marketing AI workspace."""

import streamlit as st


PAGES_CONFIG = [
    ("app.py", "Dashboard", ":material/dashboard:"),
    ("pages/1_campaigns.py", "Campaigns", ":material/folder_open:"),
    ("pages/2_brand_rules.py", "Brand rules", ":material/shield:"),
    ("pages/3_run_ai.py", "Run AI", ":material/auto_awesome:"),
    ("pages/4_calendar.py", "Calendar", ":material/calendar_month:"),
    ("pages/5_export.py", "Reports", ":material/download:"),
]


def render_dynamic_dock(current_page="app"):
    """Compatibility hook; navigation is rendered once by the shared sidebar."""
    return None
