"""Marketing AI web dashboard."""

import os
import sys

import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.connection import get_connection
from database.crud import get_all_brand_rules, get_all_campaigns, get_audits_by_campaign, get_posts_by_campaign
from database.models import init_database
from ui.components.navbar import render_dynamic_dock
from ui.components.sidebar import render_sidebar
from ui.components.theme import apply_custom_theme, render_page_header


st.set_page_config(
    page_title="Marketing AI",
    page_icon=":material/insights:",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_theme()
render_sidebar()
render_dynamic_dock("app")

try:
    init_database()
except Exception as exc:
    st.warning(f"Database chưa sẵn sàng: {exc}", icon=":material/warning:")

campaigns = []
brand_rules = []
posts = []
audits = []
try:
    conn = get_connection()
    campaigns = get_all_campaigns(conn)
    brand_rules = get_all_brand_rules(conn)
    for campaign in campaigns:
        posts.extend(get_posts_by_campaign(conn, campaign.get("id")))
        audits.extend(get_audits_by_campaign(conn, campaign.get("id")))
    conn.close()
except Exception as exc:
    st.error(f"Không thể tải dữ liệu hệ thống: {exc}", icon=":material/error:")

render_page_header(
    "Marketing AI",
    "Một nơi để lập kế hoạch, tạo nội dung, kiểm duyệt và theo dõi chiến dịch.",
    "WORKSPACE OVERVIEW",
)

with st.container(horizontal=True):
    st.metric("Campaigns", len(campaigns), border=True)
    st.metric("AI posts", len(posts), border=True)
    approved = sum(1 for post in posts if post.get("status") == "Approved")
    st.metric("Approved posts", approved, border=True)
    scores = [audit.get("compliance_score") for audit in audits if audit.get("compliance_score") is not None]
    average_score = round(sum(scores) / len(scores), 1) if scores else 0
    st.metric("Brand score", f"{average_score}/100" if scores else "N/A", border=True)

st.subheader("Start with a workflow")
with st.container(horizontal=True, horizontal_alignment="distribute"):
    st.page_link("pages/1_campaigns.py", label="Plan a campaign", icon=":material/edit_note:")
    st.page_link("pages/3_run_ai.py", label="Run AI pipeline", icon=":material/auto_awesome:")
    st.page_link("pages/5_export.py", label="Export a report", icon=":material/download:")

left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.subheader("Campaign status")
        if campaigns:
            status_counts = pd.Series([item.get("status", "Draft") for item in campaigns]).value_counts()
            st.bar_chart(status_counts, height=260, x_label="Status", y_label="Campaigns")
        else:
            st.info("Chưa có campaign. Hãy tạo campaign đầu tiên.", icon=":material/add_circle:")

with right:
    with st.container(border=True):
        st.subheader("Recent campaigns")
        if campaigns:
            recent = pd.DataFrame(
                [
                    {
                        "Campaign": item.get("name", ""),
                        "Product": item.get("product_name", ""),
                        "Status": item.get("status", "Draft"),
                        "Channels": item.get("channels", "") or "-",
                    }
                    for item in campaigns[:6]
                ]
            )
            st.dataframe(recent, hide_index=True, width="stretch", height=260)
        else:
            st.caption("Danh sách campaign sẽ xuất hiện tại đây.")

with st.container(border=True):
    st.subheader("Next steps")
    st.write("1. Tạo campaign brief và chọn kênh truyền thông.")
    st.write("2. Chọn brand rule để AI kiểm tra nội dung.")
    st.write("3. Chạy pipeline, xem lịch đăng và xuất báo cáo.")
