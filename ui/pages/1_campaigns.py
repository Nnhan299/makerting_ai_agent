"""
Trang 1: Quản lý Chiến dịch Marketing (Module 1 - Campaign Management)
Giao diện Dark Glassmorphism cao cấp với Card View và Form nhập liệu hiện đại.
"""

import sys
import os
import streamlit as st
import pandas as pd
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.connection import get_connection
from database.crud import (
    create_campaign,
    get_all_campaigns,
    update_campaign,
    delete_campaign
)
from ui.components.sidebar import render_sidebar
from ui.components.navbar import render_dynamic_dock
from ui.components.theme import (
    apply_custom_theme,
    render_page_header,
    get_status_chip,
    get_channel_chip
)

st.set_page_config(page_title="Chiến dịch Marketing - Marketing AI", page_icon="📋", layout="wide")
apply_custom_theme()
render_sidebar()
render_dynamic_dock("campaigns")

render_page_header(
    title="Quản trị Chiến dịch (Campaign Briefs)",
    subtitle="Khởi tạo hồ sơ chiến dịch, thiết lập đối tượng mục tiêu và kênh phân phối",
    badge="MODULE 1 • CAMPAIGN MANAGEMENT"
)

tab1, tab2 = st.tabs(["📑 Danh sách Chiến dịch", "➕ Khởi tạo Chiến dịch Mới"])

# ============================================================
# TAB 1: DANH SÁCH CHIẾN DỊCH (CARD VIEW)
# ============================================================
with tab1:
    try:
        conn = get_connection()
        campaigns = get_all_campaigns(conn)
        conn.close()
    except Exception as e:
        campaigns = []
        st.error(f"Lỗi khi đọc dữ liệu: {e}")

    if not campaigns:
        st.info("Chưa có chiến dịch nào. Hãy chuyển sang Tab 'Khởi tạo Chiến dịch Mới' bên cạnh.")
    else:
        # Search & Filter bar
        c_filter1, c_filter2 = st.columns([2, 1])
        with c_filter1:
            search_query = st.text_input("🔍 Tìm kiếm chiến dịch hoặc sản phẩm...", placeholder="Nhập từ khóa...")
        with c_filter2:
            status_filter = st.selectbox("Lọc trạng thái", ["Tất cả", "Draft", "In-Progress", "Approved", "Completed"])

        filtered_camps = campaigns
        if search_query:
            q = search_query.lower()
            filtered_camps = [c for c in filtered_camps if q in c["name"].lower() or q in c["product_name"].lower()]
        if status_filter != "Tất cả":
            filtered_camps = [c for c in filtered_camps if c["status"] == status_filter]

        st.caption(f"Tìm thấy {len(filtered_camps)} / {len(campaigns)} chiến dịch")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        for camp in filtered_camps:
            status_html = get_status_chip(camp.get("status"))
            channels_list = [ch.strip() for ch in (camp.get("channels") or "").split(",") if ch.strip()]
            channel_chips = " ".join([get_channel_chip(ch) for ch in channels_list]) if channels_list else "<span>Chưa gán kênh</span>"

            with st.expander(f"🎯 [{camp['status']}] {camp['name']}  •  Sản phẩm: {camp['product_name']}", expanded=False):
                col_left, col_right = st.columns([3, 1], gap="medium")
                
                with col_left:
                    st.markdown(
                        f"""
                        <div style="background: rgba(15, 23, 42, 0.6); padding: 14px 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 12px;">
                            <div style="display: flex; gap: 8px; margin-bottom: 10px;">
                                {status_html}
                                {channel_chips}
                            </div>
                            <div style="font-size: 0.88rem; color: #E2E8F0; margin-bottom: 6px;">
                                <strong>Đối tượng mục tiêu:</strong> <span style="color: #94A3B8;">{camp.get('target_audience') or 'Chưa xác định'}</span>
                            </div>
                            <div style="display: flex; gap: 24px; font-size: 0.82rem; color: #94A3B8;">
                                <span>💰 Ngân sách: <strong style="color: #F8FAFC;">{camp.get('budget') or 'Chưa nhập'}</strong></span>
                                <span>📅 Thời gian: <strong style="color: #F8FAFC;">{camp['start_date']} ➔ {camp['end_date']}</strong></span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col_right:
                    st.markdown("##### Thao tác")
                    new_status = st.selectbox(
                        "Cập nhật trạng thái",
                        options=["Draft", "In-Progress", "Approved", "Completed"],
                        index=["Draft", "In-Progress", "Approved", "Completed"].index(camp["status"]),
                        key=f"status_sel_{camp['id']}"
                    )
                    
                    c_act1, c_act2 = st.columns(2)
                    with c_act1:
                        if st.button("Lưu", key=f"btn_save_{camp['id']}", type="primary", use_container_width=True):
                            conn = get_connection()
                            update_campaign(conn, camp["id"], status=new_status)
                            conn.close()
                            st.success("Đã cập nhật!")
                            st.rerun()
                    with c_act2:
                        if st.button("Xóa", key=f"btn_del_{camp['id']}", type="secondary", use_container_width=True):
                            conn = get_connection()
                            delete_campaign(conn, camp["id"])
                            conn.close()
                            st.success("Đã xóa chiến dịch!")
                            st.rerun()

# ============================================================
# TAB 2: FORM KHỞI TẠO CHIẾN DỊCH
# ============================================================
with tab2:
    st.markdown("### 📝 Điền thông tin Campaign Brief")
    st.caption("Cung cấp chi tiết các trường bên dưới để AI Agent phân tích và sinh nội dung chuẩn xác nhất.")

    with st.form("create_campaign_form", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2, gap="medium")
        
        with col_f1:
            name = st.text_input("Tên chiến dịch Marketing *", placeholder="Vd: Ra mắt Sữa rửa mặt XYZ Tháng 10")
            product_name = st.text_input("Tên Sản phẩm / Dịch vụ *", placeholder="Vd: Sữa rửa mặt XYZ Salicylic Acid 2%")
            budget = st.text_input("Ngân sách dự kiến", placeholder="Vd: 50.000.000 VND")
            
        with col_f2:
            channels_selected = st.multiselect(
                "Kênh xuất bản truyền thông",
                options=["Facebook", "LinkedIn", "Email"],
                default=["Facebook", "Email"]
            )
            c_d1, c_d2 = st.columns(2)
            with c_d1:
                start_date = st.date_input("Ngày bắt đầu", value=date.today())
            with c_d2:
                end_date = st.date_input("Ngày kết thúc", value=date.today())

        target_audience = st.text_area(
            "Mô tả chi tiết Đối tượng mục tiêu (Target Persona & Pain Points)",
            placeholder="Vd: Nữ 18-25 tuổi, da dầu mụn, học sinh sinh viên hoặc nhân viên văn phòng trẻ, có thói quen thức khuya, mong muốn làm sạch sâu không khô da...",
            height=120
        )

        submitted = st.form_submit_button("🚀 Khởi Tạo Campaign Brief Mới", type="primary", use_container_width=True)

        if submitted:
            if not name.strip() or not product_name.strip():
                st.error("Vui lòng điền đầy đủ Tên chiến dịch và Tên sản phẩm!")
            elif end_date < start_date:
                st.error("Ngày kết thúc không được nhỏ hơn ngày bắt đầu!")
            else:
                try:
                    conn = get_connection()
                    channels_str = ", ".join(channels_selected) if channels_selected else "Facebook"
                    camp_id = create_campaign(
                        conn=conn,
                        name=name.strip(),
                        product_name=product_name.strip(),
                        target_audience=target_audience.strip(),
                        budget=budget.strip(),
                        channels=channels_str,
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d")
                    )
                    conn.close()
                    st.success(f"✅ Đã tạo chiến dịch thành công! (ID: {camp_id})")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi khi lưu chiến dịch: {e}")
