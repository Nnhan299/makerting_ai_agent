"""
Entry point chính của ứng dụng Streamlit - Marketing AI Campaign Manager.
Giao diện Dark Glassmorphism cao cấp với hệ thống KPI Metrics và biểu đồ phân tích thời gian thực.
"""

import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.models import init_database
from database.connection import get_connection
from database.crud import (
    get_all_campaigns,
    get_all_brand_rules,
    get_posts_by_campaign,
    get_audits_by_campaign
)
from ui.components.sidebar import render_sidebar
from ui.components.navbar import render_dynamic_dock
from ui.components.theme import (
    apply_custom_theme,
    render_page_header,
    render_kpi_card,
    get_status_chip
)

# 1. Cấu hình trang
st.set_page_config(
    page_title="Marketing AI Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Áp dụng Design System Dark Glassmorphism & macOS Dynamic Dock
apply_custom_theme()
render_sidebar()
render_dynamic_dock("app")

# 3. Khởi tạo DB nếu cần
try:
    init_database()
except Exception as e:
    st.warning(f"Lưu ý kết nối PostgreSQL: {e}")

# 4. Header trang
render_page_header(
    title="Executive Dashboard",
    subtitle="Trung tâm điều hành và theo dõi hiệu suất chiến dịch Marketing Multi-Agent",
    badge="ORCHESTRATION CONSOLE"
)

# 5. Truy vấn dữ liệu thực tế từ PostgreSQL
try:
    conn = get_connection()
    campaigns = get_all_campaigns(conn)
    brand_rules = get_all_brand_rules(conn)

    total_campaigns = len(campaigns)
    total_rules = len(brand_rules)
    
    total_posts = 0
    total_scores = []
    approved_posts = 0
    
    for camp in campaigns:
        posts = get_posts_by_campaign(conn, camp["id"])
        total_posts += len(posts)
        approved_posts += sum(1 for p in posts if p.get("status") == "Approved")
        
        audits = get_audits_by_campaign(conn, camp["id"])
        for a in audits:
            if a.get("compliance_score") is not None:
                total_scores.append(a["compliance_score"])
                
    avg_score = round(sum(total_scores) / len(total_scores), 1) if total_scores else 0.0
    conn.close()
except Exception as e:
    campaigns = []
    brand_rules = []
    total_campaigns = 0
    total_rules = 0
    total_posts = 0
    avg_score = 0.0
    approved_posts = 0

# 6. Hiển thị 4 Glassmorphic KPI Cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    render_kpi_card(
        label="Chiến dịch Marketing",
        value=str(total_campaigns),
        subtext="📈 Đang quản trị trong hệ thống",
        icon="🎯",
        theme="indigo"
    )

with c2:
    render_kpi_card(
        label="Nội dung AI đã sinh",
        value=str(total_posts),
        subtext=f"✨ {approved_posts} bài đã duyệt hoàn tất",
        icon="✍️",
        theme="cyan"
    )

with c3:
    render_kpi_card(
        label="Điểm Tuân thủ TB",
        value=f"{avg_score}/100" if total_scores else "N/A",
        subtext="🛡️ Brand Compliance Score",
        icon="🏆",
        theme="emerald"
    )

with c4:
    render_kpi_card(
        label="Bộ Quy tắc Thương hiệu",
        value=str(total_rules),
        subtext="📋 Tiêu chuẩn kiểm duyệt",
        icon="📜",
        theme="amber"
    )

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# 7. Quick Actions Banner
st.markdown(
    """
    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.10) 100%); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 14px; padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="font-size: 1.8rem;">🚀</div>
            <div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF;">Khởi chạy Pipeline 3 AI Agent tuần tự</div>
                <div style="font-size: 0.8rem; color: #94A3B8;">Tự động phân tích insight, sinh 20-30 bài viết theo phễu tâm lý và kiểm duyệt vi phạm thương hiệu.</div>
            </div>
        </div>
        <div style="font-size: 0.85rem; font-weight: 600; color: #818CF8;">
            Trang 3_run_ai ➔
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 8. Charts & Recent Campaigns
col_chart, col_list = st.columns([1, 1], gap="medium")

with col_chart:
    st.markdown("### 📊 Phân bổ Trạng thái Chiến dịch")
    if campaigns:
        df_camp = pd.DataFrame(campaigns)
        status_counts = df_camp["status"].value_counts().reset_index()
        status_counts.columns = ["Trạng thái", "Số lượng"]
        
        color_map = {
            "Draft": "#F59E0B",
            "In-Progress": "#06B6D4",
            "Approved": "#10B981",
            "Completed": "#64748B"
        }
        
        fig = px.pie(
            status_counts,
            values="Số lượng",
            names="Trạng thái",
            hole=0.55,
            color="Trạng thái",
            color_discrete_map=color_map
        )
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#CBD5E1"),
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chưa có chiến dịch nào để vẽ biểu đồ.")

with col_list:
    st.markdown("### 📋 Chiến dịch gần đây")
    if campaigns:
        for c in campaigns[:4]:
            status_badge = get_status_chip(c.get("status"))
            channels = c.get("channels") or "Chưa chọn kênh"
            
            st.markdown(
                f"""
                <div style="background: rgba(17, 24, 39, 0.5); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px; padding: 12px 16px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; transition: all 0.2s ease;">
                    <div>
                        <div style="font-weight: 700; font-size: 0.92rem; color: #F1F5F9; margin-bottom: 4px;">{c['name']}</div>
                        <div style="font-size: 0.78rem; color: #94A3B8;">
                            📦 <span style="color: #CBD5E1;">{c['product_name']}</span> &nbsp;•&nbsp; 🌐 {channels}
                        </div>
                    </div>
                    <div>
                        {status_badge}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("Danh sách trống. Hãy tạo chiến dịch mới tại trang 1_campaigns.")
