"""Shared native sidebar for the Streamlit app."""

import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.html(
            """
            <style>
                [data-testid="stSidebarNav"] { display: none; }
                [data-testid="stSidebar"] { min-width: 286px; max-width: 286px; }
                [data-testid="stSidebar"] button {
                    min-height: 44px;
                    margin: 4px 0;
                    border-radius: 8px;
                    border: 1px solid #d8d1c8;
                    font-weight: 600;
                    text-align: left;
                }
            </style>
            """
        )
        st.markdown("## Marketing AI")
        st.caption("Campaign studio")
        st.divider()
        st.caption("WORKSPACE")
        pages = [
            ("app.py", "Dashboard", ":material/dashboard:"),
            ("pages/1_campaigns.py", "Campaigns", ":material/folder_open:"),
            ("pages/2_brand_rules.py", "Brand rules", ":material/shield:"),
            ("pages/3_run_ai.py", "Run AI", ":material/auto_awesome:"),
            ("pages/4_calendar.py", "Calendar", ":material/calendar_month:"),
            ("pages/5_export.py", "Reports", ":material/download:"),
        ]
        for target, label, icon in pages:
            if st.button(label, icon=icon, key=f"sidebar_{label.lower().replace(' ', '_')}", width="stretch"):
                st.switch_page(target)
        st.divider()
        st.caption("SYSTEM STATUS")
        st.success("Database ready", icon=":material/database:")
        st.info("3 agents available", icon=":material/auto_awesome:")
        st.caption("Version 1.0.0")
