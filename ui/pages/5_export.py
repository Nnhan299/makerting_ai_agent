"""
Trang 5: Xuất bản & Báo cáo (Module 4 - Publishing & Exporting)
Giao diện Xuất file Excel 3 Sheet cao cấp và Gửi Email Báo cáo qua SMTP.
"""

import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.connection import get_connection
from database.crud import (
    get_all_campaigns,
    get_campaign_by_id,
    get_posts_by_campaign,
    get_audits_by_campaign
)
from utils.export_excel import export_campaign_to_excel
from ui.components.auth import require_auth
from ui.components.sidebar import render_sidebar
from ui.components.navbar import render_dynamic_dock
from ui.components.theme import (
    apply_custom_theme,
    render_page_header,
    render_kpi_card
)

st.set_page_config(page_title="Xuất bản & Báo cáo - Marketing AI", page_icon="📤", layout="wide")
apply_custom_theme()
require_auth()
render_sidebar()
render_dynamic_dock("export")

render_page_header(
    title="Xuất bản & Báo cáo Chiến dịch",
    subtitle="Trích xuất bộ dữ liệu lịch bài đăng ra file Excel chuẩn định dạng hoặc gửi email trực tiếp cho các bên liên quan",
    badge="MODULE 4 • PUBLISHING & EXPORT HUB"
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
selected_camp_str = st.selectbox("🎯 Chọn Chiến dịch để trích xuất báo cáo", options=list(camp_options.keys()))
selected_camp_id = camp_options[selected_camp_str]

conn = get_connection()
campaign = get_campaign_by_id(conn, selected_camp_id)
posts = get_posts_by_campaign(conn, selected_camp_id)
audit_logs = get_audits_by_campaign(conn, selected_camp_id)
conn.close()

# KPI TÓM TẮT SẴN SÀNG
approved_posts = [p for p in posts if p.get("status") == "Approved"]
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

e1, e2, e3 = st.columns(3)
with e1:
    render_kpi_card("Tổng số bài viết", str(len(posts)), "📋 Trong kế hoạch", "📝", "indigo")
with e2:
    render_kpi_card("Bài viết đã duyệt", str(len(approved_posts)), "✅ Sẵn sàng đăng tải", "🟢", "emerald")
with e3:
    render_kpi_card("Bản ghi kiểm duyệt", str(len(audit_logs)), "🛡️ Đã đánh giá tuân thủ", "🔍", "cyan")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

col_ex1, col_ex2 = st.columns(2, gap="large")

@st.cache_data(show_spinner="Đang tạo file Excel...", ttl=120)
def get_cached_excel_bytes(camp_id: int, num_posts: int, num_audits: int):
    conn = get_connection()
    c = get_campaign_by_id(conn, camp_id)
    p = get_posts_by_campaign(conn, camp_id)
    a = get_audits_by_campaign(conn, camp_id)
    conn.close()
    return export_campaign_to_excel(c, p, a)


# 2. XUẤT EXCEL CHUYÊN NGHIỆP
with col_ex1:
    st.markdown("### 📥 1. Trích xuất File Excel (.xlsx)")
    st.markdown(
        """
        <div style="background: rgba(17, 24, 39, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 18px; margin-bottom: 16px;">
            <div style="font-weight: 700; color: #F8FAFC; margin-bottom: 8px;">Cấu trúc file Excel 3 Sheet chuyên nghiệp:</div>
            <ul style="color: #94A3B8; font-size: 0.85rem; line-height: 1.6; margin-bottom: 0;">
                <li><strong>Sheet 1 - Tổng quan chiến dịch:</strong> Tên, sản phẩm, đối tượng, ngân sách, thời gian.</li>
                <li><strong>Sheet 2 - Lịch bài đăng:</strong> Bảng phân bổ bài viết theo giai đoạn, kênh và ngày xuất bản.</li>
                <li><strong>Sheet 3 - Báo cáo kiểm duyệt:</strong> Chi tiết vi phạm từ cấm và gợi ý sửa đổi.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if posts:
        excel_bytes = get_cached_excel_bytes(selected_camp_id, len(posts), len(audit_logs))
        st.download_button(
            label="📥 TẢI XUỐNG FILE EXCEL (.XLSX)",
            data=excel_bytes,
            file_name=f"Marketing_Campaign_{selected_camp_id}_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            width="stretch"
        )
    else:
        st.warning("Chiến dịch này chưa có bài viết để xuất Excel.")

# 3. GỬI BÁO CÁO QUA EMAIL SMTP
with col_ex2:
    st.markdown("### 📧 2. Gửi Báo cáo qua Email (SMTP)")
    
    with st.form("email_form"):
        recipient_email = st.text_input("Địa chỉ Email người nhận *", placeholder="marketing.manager@company.com")
        email_subject = st.text_input("Tiêu đề Email", value=f"[Marketing AI Report] Kế hoạch nội dung {campaign['name']}")
        email_notes = st.text_area("Ghi chú bổ sung đính kèm", placeholder="Kính gửi Trưởng phòng, đây là kế hoạch nội dung đã được AI sinh và kiểm duyệt...", height=100)
        
        btn_send_email = st.form_submit_button("Gửi email báo cáo", width="stretch")

        if btn_send_email:
            if not recipient_email.strip():
                st.error("Vui lòng nhập Email người nhận!")
            else:
                smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
                smtp_port = int(os.getenv("SMTP_PORT", 587))
                smtp_user = os.getenv("SMTP_USERNAME", "")
                smtp_pass = os.getenv("SMTP_PASSWORD", "")
                email_from = os.getenv("EMAIL_FROM", smtp_user)

                if not smtp_user or smtp_user == "your_email@gmail.com":
                    st.warning("⚠️ Chưa cấu hình SMTP_USERNAME/SMTP_PASSWORD trong file .env!")
                else:
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = email_from
                        msg['To'] = recipient_email
                        msg['Subject'] = email_subject

                        body_text = f"""Xin chào,\n\nĐây là báo cáo tự động từ Hệ thống Marketing AI Campaign Manager.\n\nTên chiến dịch: {campaign['name']}\nSản phẩm: {campaign['product_name']}\nTổng số bài đăng: {len(posts)}\nSố bài đã duyệt: {len(approved_posts)}\n\nGhi chú: {email_notes}\n\nTrân trọng,\nMarketing AI Team"""
                        msg.attach(MIMEText(body_text, 'plain', 'utf-8'))

                        server = smtplib.SMTP(smtp_host, smtp_port)
                        server.starttls()
                        server.login(smtp_user, smtp_pass)
                        server.sendmail(email_from, recipient_email, msg.as_string())
                        server.quit()

                        st.success(f"✅ Đã gửi email báo cáo thành công tới {recipient_email}!")
                    except Exception as e:
                        st.error(f"❌ Lỗi gửi email: {e}")
