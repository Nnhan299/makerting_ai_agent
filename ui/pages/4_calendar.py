"""
Trang 4: Content Calendar & Phê duyệt bài viết (Module 4 - Content Calendar)
Giao diện Social Media Post Cards cao cấp với quy trình Human-in-the-Loop.
"""

import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.connection import get_connection
from database.crud import (
    get_all_campaigns,
    get_posts_by_campaign,
    update_post_status,
    update_post_content,
    get_audit_by_post
)
from ui.components.sidebar import render_sidebar
from ui.components.navbar import render_dynamic_dock
from ui.components.theme import (
    apply_custom_theme,
    render_page_header,
    render_kpi_card,
    get_stage_chip,
    get_channel_chip,
    get_status_chip
)

st.set_page_config(page_title="Content Calendar - Marketing AI", page_icon="📅", layout="wide")
apply_custom_theme()
render_sidebar()
render_dynamic_dock("calendar")

render_page_header(
    title="Content Calendar & Phê duyệt (Human-in-the-Loop)",
    subtitle="Lịch trình phát hành nội dung đa kênh, rà soát vi phạm pháp lý & phê duyệt bài viết trước khi xuất bản",
    badge="MODULE 4 • EDITORIAL & COMPLIANCE"
)

try:
    conn = get_connection()
    campaigns = get_all_campaigns(conn)
    conn.close()
except Exception as e:
    campaigns = []
    st.error(f"Lỗi đọc DB: {e}")

if not campaigns:
    st.info("Chưa có chiến dịch nào.")
    st.stop()

# 1. BỘ CHỌN CHIẾN DỊCH
camp_options = {f"{c['name']} (ID: {c['id']})": c['id'] for c in campaigns}
selected_camp_str = st.selectbox("🎯 Chọn Chiến dịch để xem Content Calendar", options=list(camp_options.keys()))
selected_camp_id = camp_options[selected_camp_str]

try:
    conn = get_connection()
    posts = get_posts_by_campaign(conn, selected_camp_id)
    conn.close()
except Exception as e:
    posts = []
    st.error(f"Lỗi lấy bài viết: {e}")

if not posts:
    st.warning("⚠️ Chiến dịch này chưa có bài viết nào do AI tạo. Hãy sang trang **3_run_ai** để chạy AI Pipeline!")
    st.stop()

# 2. KPI METRICS TRẠNG THÁI BÀI ĐĂNG
total_cnt = len(posts)
pending_cnt = sum(1 for p in posts if p["status"] == "Pending")
approved_cnt = sum(1 for p in posts if p["status"] == "Approved")
rejected_cnt = sum(1 for p in posts if p["status"] == "Rejected")

k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi_card("Tổng bài viết", str(total_cnt), "📅 Phân bổ toàn chiến dịch", "📚", "indigo")
with k2:
    render_kpi_card("Chờ duyệt", str(pending_cnt), "⏳ Cần biên tập viên duyệt", "🟡", "amber")
with k3:
    render_kpi_card("Đã phê duyệt", str(approved_cnt), "✅ Sẵn sàng xuất bản", "🟢", "emerald")
with k4:
    render_kpi_card("Đã từ chối", str(rejected_cnt), "❌ Cần tạo lại nội dung", "🔴", "rose")

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# 3. BỘ LỌC BÀI VIẾT
col_f1, col_f2 = st.columns(2, gap="medium")
with col_f1:
    stage_filter = st.selectbox("Lọc theo Giai đoạn phễu", ["Tất cả", "Teaser", "Launch", "CTA"])
with col_f2:
    status_filter = st.selectbox("Lọc theo Trạng thái duyệt", ["Tất cả", "Pending", "Approved", "Rejected"])

filtered_posts = posts
if stage_filter != "Tất cả":
    filtered_posts = [p for p in filtered_posts if p["stage"] == stage_filter]
if status_filter != "Tất cả":
    filtered_posts = [p for p in filtered_posts if p["status"] == status_filter]

st.caption(f"Đang hiển thị {len(filtered_posts)} / {len(posts)} bài viết")
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# 4. DANH SÁCH POST CARDS
for p in filtered_posts:
    post_id = p["id"]
    stage_chip = get_stage_chip(p.get("stage"))
    channel_chip = get_channel_chip(p.get("channel"))
    status_chip = get_status_chip(p.get("status"))

    with st.expander(f"📌 [{p['stage']}] [{p['channel']}] {p['title'] or 'Không có tiêu đề'}  •  📅 {p.get('scheduled_date')}", expanded=False):
        c_left, c_right = st.columns([3, 2], gap="large")
        
        with c_left:
            st.markdown(
                f"""
                <div style="display: flex; gap: 8px; margin-bottom: 12px; align-items: center;">
                    {stage_chip}
                    {channel_chip}
                    {status_chip}
                    <span style="font-size: 0.8rem; color: #94A3B8; margin-left: auto;">📅 {p.get('scheduled_date')}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(f"**Tiêu đề bài viết:** `{p.get('title')}`")
            st.text_area("Nội dung bài viết (Có thể chỉnh sửa)", value=p["content"], height=160, key=f"txt_{post_id}")
            
        with c_right:
            # Lấy audit log
            try:
                conn = get_connection()
                audit = get_audit_by_post(conn, post_id)
                conn.close()
            except Exception:
                audit = None

            if audit:
                score = audit.get("compliance_score", 100)
                score_color = "#34D399" if score >= 80 else ("#FBBF24" if score >= 60 else "#FB7185")
                
                st.markdown(
                    f"""
                    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Compliance Audit</span>
                            <span style="font-size: 1.15rem; font-weight: 800; color: {score_color};">{score}/100</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                violations = audit.get("violations_json", [])
                if violations:
                    st.error(f"Phát hiện {len(violations)} vi phạm:")
                    for v in violations:
                        st.caption(f"- **[{v.get('type')}]**: {v.get('detail')} (Cụm: `{v.get('found_text')}`) ➔ Gợi ý: {v.get('suggestion')}")
                else:
                    st.success("✅ Đạt chuẩn: Không vi phạm từ cấm và tone giọng!")
            else:
                st.info("Chưa có audit log.")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            # Nút phê duyệt
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("✅ Duyệt", key=f"app_{post_id}", type="primary", use_container_width=True):
                    conn = get_connection()
                    update_post_status(conn, post_id, "Approved")
                    conn.close()
                    st.success("Đã duyệt!")
                    st.rerun()
            with b2:
                if st.button("❌ Từ chối", key=f"rej_{post_id}", type="secondary", use_container_width=True):
                    conn = get_connection()
                    update_post_status(conn, post_id, "Rejected")
                    conn.close()
                    st.warning("Đã từ chối!")
                    st.rerun()
            with b3:
                if st.button("💾 Lưu sửa", key=f"save_{post_id}", use_container_width=True):
                    new_content = st.session_state.get(f"txt_{post_id}", p["content"])
                    conn = get_connection()
                    update_post_content(conn, post_id, p["title"], new_content)
                    conn.close()
                    st.success("Đã lưu nội dung!")
                    st.rerun()
