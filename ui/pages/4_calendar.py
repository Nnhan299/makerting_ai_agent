"""
Trang 4: Xem trước bài viết trước khi đăng & Phê duyệt (Module 4 - Live Social Preview & Human-in-the-Loop)
Mô phỏng chân thực bài đăng trên màn hình Điện thoại (Mobile) và Bảng tin MXH (Desktop Feed).
"""

import sys
import os
import time
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
    update_post_media,
    mark_post_as_published,
    get_audits_by_campaign
)
from utils.social_publisher import execute_auto_publish
from utils.media_manager import (
    get_all_available_media,
    save_uploaded_media,
    list_local_media,
    CURATED_PRESETS
)
from ui.components.auth import require_auth
from ui.components.sidebar import render_sidebar, get_role_permissions, get_current_role
from ui.components.navbar import render_dynamic_dock
from ui.components.post_mockup import render_social_mockup, render_mobile_phone_mockup
from ui.components.theme import (
    apply_custom_theme,
    render_page_header,
    render_kpi_card,
    get_stage_chip,
    get_channel_chip,
    get_status_chip
)

st.set_page_config(page_title="Xem trước bài viết - Marketing AI", page_icon="👁️", layout="wide")
apply_custom_theme()
require_auth()
render_sidebar()
render_dynamic_dock("calendar")

render_page_header(
    title="Xem trước bài viết trước khi đăng (Live Social Preview)",
    subtitle="Mô phỏng trực quan 100% giao diện bài đăng trên Điện thoại & Bảng tin MXH trước khi chính thức xuất bản",
    badge="MODULE 4 • LIVE SOCIAL PREVIEW & EDITORIAL"
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
col_c1, col_c2 = st.columns([2, 1], gap="medium")
with col_c1:
    camp_options = {f"{c['name']} (ID: {c['id']})": c['id'] for c in campaigns}
    selected_camp_str = st.selectbox("🎯 Chọn Chiến dịch Marketing cần xem trước bài viết:", options=list(camp_options.keys()))
    selected_camp_id = camp_options[selected_camp_str]
    selected_camp = next((c for c in campaigns if c["id"] == selected_camp_id), None)
    selected_camp_name = selected_camp["name"] if selected_camp else "Thương hiệu"

with col_c2:
    current_role = get_current_role()
    permissions = get_role_permissions()
    st.markdown(
        f"""
        <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 10px 14px; margin-top: 26px;">
            <div style="font-size: 0.75rem; color: #94A3B8;">Quyền phê duyệt:</div>
            <div style="font-size: 0.88rem; font-weight: 700; color: {'#10B981' if permissions.get('can_approve') else '#38BDF8'};">
                {'✅ Có quyền duyệt bài (Lead/Admin)' if permissions.get('can_approve') else '🔒 Chỉ xem & soạn thảo (Cần Lead duyệt)'}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

try:
    conn = get_connection()
    posts = get_posts_by_campaign(conn, selected_camp_id)
    audits = get_audits_by_campaign(conn, selected_camp_id)
    conn.close()
    audit_map = {a.get("post_id"): a for a in audits if a.get("post_id")}
except Exception as e:
    posts = []
    audit_map = {}
    st.error(f"Lỗi lấy bài viết: {e}")

if not posts:
    st.warning("⚠️ Chiến dịch này chưa có bài viết nào do AI tạo. Hãy sang trang **3_run_ai** để chạy AI Pipeline!")
    st.stop()

# KPI METRICS
total_cnt = len(posts)
pending_cnt = sum(1 for p in posts if p["status"] == "Pending")
approved_cnt = sum(1 for p in posts if p["status"] == "Approved")
published_cnt = sum(1 for p in posts if p.get("status") == "Published")
rejected_cnt = sum(1 for p in posts if p["status"] == "Rejected")

k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi_card("Tổng bài viết", str(total_cnt), "📅 Toàn bộ chiến dịch", "📚", "indigo")
with k2:
    render_kpi_card("Chờ duyệt", str(pending_cnt), "⏳ Cần biên tập viên duyệt", "🟡", "amber")
with k3:
    render_kpi_card("Đã duyệt", str(approved_cnt), "✅ Sẵn sàng đăng tải", "🟢", "emerald")
with k4:
    render_kpi_card("Đã xuất bản", str(published_cnt), "🚀 Đã đăng lên MXH", "⚡", "cyan")

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# 3 TABS CHÍNH (Xem trước • Danh sách lịch • Thư viện ảnh)
tab_preview, tab_list, tab_media = st.tabs([
    "📱 MỤC XEM TRƯỚC BÀI VIẾT (LIVE SOCIAL PREVIEW)",
    "📑 DANH SÁCH TẤT CẢ BÀI VIẾT & LỊCH ĐĂNG",
    "🖼️ THƯ VIỆN HÌNH ẢNH (MEDIA ASSETS GALLERY)"
])

# ============================================================
# TAB 1: MỤC XEM TRƯỚC BÀI VIẾT TRƯỚC KHI ĐĂNG
# ============================================================
with tab_preview:
    st.markdown("##### 👁️ Xem trước bài đăng trên các thiết bị trước khi bấm xuất bản")
    
    col_p1, col_p2, col_p3 = st.columns([2, 1, 1], gap="medium")
    
    with col_p1:
        post_options = {
            f"[{p['stage']}] #{p['id']} - {p['title'][:60]}... ({p['status']})": p['id'] 
            for p in posts
        }
        sel_post_str = st.selectbox("Chọn bài viết cần xem trước:", options=list(post_options.keys()))
        sel_post_id = post_options[sel_post_str]
        selected_post = next((p for p in posts if p['id'] == sel_post_id), posts[0])

    with col_p2:
        device_mode = st.radio(
            "Thiết bị mô phỏng:",
            ["📱 Điện thoại (Mobile)", "💻 Bảng tin (Desktop Feed)"],
            horizontal=True
        )

    with col_p3:
        platform_mode = st.selectbox("Kênh mạng xã hội:", ["Facebook", "Instagram", "LinkedIn"])

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    col_view, col_action = st.columns([1.3, 1], gap="large")

    # Cột hiển thị Mockup
    with col_view:
        if device_mode == "📱 Điện thoại (Mobile)":
            st.caption("Mô phỏng hiển thị trên màn hình Smartphone (Facebook Mobile App):")
            render_mobile_phone_mockup(selected_post, brand_name=selected_camp_name, platform=platform_mode)
        else:
            st.caption("Mô phỏng hiển thị trên Bảng tin Mạng xã hội (Desktop Web Feed):")
            render_social_mockup(selected_post, brand_name=selected_camp_name, platform=platform_mode)

    # Cột thao tác duyệt & chỉnh sửa
    with col_action:
        st.markdown(f"#### ⚙️ Kiểm duyệt bài viết #{selected_post['id']}")
        
        # Trạng thái hiện tại
        status_color = "#34D399" if selected_post['status'] == 'Approved' else ("#FBBF24" if selected_post['status'] == 'Pending' else "#FB7185")
        st.markdown(
            f"""
            <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 16px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.82rem; color: #94A3B8;">Trạng thái xuất bản:</span>
                    <span style="font-size: 0.9rem; font-weight: 800; color: {status_color};">● {selected_post['status']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                    <span style="font-size: 0.82rem; color: #94A3B8;">Giai đoạn phễu:</span>
                    <span style="font-size: 0.85rem; font-weight: 700; color: #38BDF8;">{selected_post['stage']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                    <span style="font-size: 0.82rem; color: #94A3B8;">Ngày đăng dự kiến:</span>
                    <span style="font-size: 0.85rem; font-weight: 700; color: #E2E8F0;">{selected_post.get('scheduled_date', 'Chưa đặt')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Audit score
        audit = audit_map.get(selected_post["id"])
        if audit:
            score = audit.get("compliance_score", 100)
            score_color = "#34D399" if score >= 80 else ("#FBBF24" if score >= 60 else "#FB7185")
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                    <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Điểm tuân thủ thương hiệu (Compliance Score)</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: {score_color};">{score}/100</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            violations = audit.get("violations_json", [])
            if violations:
                st.error(f"⚠️ Phát hiện {len(violations)} vi phạm từ cấm/luật quảng cáo:")
                for v in violations:
                    st.caption(f"- **[{v.get('type')}]**: {v.get('detail')} (Cụm: `{v.get('found_text')}`)")
                    st.info(f"💡 Gợi ý: {v.get('suggestion')}")
            else:
                st.success("✅ Đạt chuẩn: Không vi phạm từ cấm và tone giọng!")
        else:
            st.info("Chưa có audit log cho bài viết này.")

        # KHU VỰC PHÊ DUYỆT BÀI VIẾT
        can_approve = permissions.get("can_approve", True)
        post_curr_status = selected_post.get("status", "Pending")

        if post_curr_status == "Published":
            st.success("🚀 **BÀI VIẾT NÀY ĐÃ ĐƯỢC XUẤT BẢN THÀNH CÔNG!**")
            pub_link = selected_post.get("published_url") or "#"
            st.markdown(f"👉 [Nhấn vào đây để xem bài đăng thực tế trên Mạng xã hội]({pub_link})")
        else:
            b1, b2 = st.columns(2)
            with b1:
                btn_app_disabled = not can_approve or post_curr_status == "Approved"
                help_app = "Chỉ Marketing Lead hoặc Admin mới có quyền duyệt bài" if not can_approve else ""
                if st.button("✅ Duyệt bài đăng", key=f"app_single_{selected_post['id']}", type="primary", disabled=btn_app_disabled, help=help_app, use_container_width=True):
                    conn = get_connection()
                    update_post_status(conn, selected_post['id'], "Approved")
                    conn.close()
                    st.success("Đã phê duyệt bài viết!")
                    st.rerun()
            with b2:
                btn_rej_disabled = not can_approve or post_curr_status == "Rejected"
                if st.button("❌ Từ chối bài", key=f"rej_single_{selected_post['id']}", disabled=btn_rej_disabled, use_container_width=True):
                    conn = get_connection()
                    update_post_status(conn, selected_post['id'], "Rejected")
                    conn.close()
                    st.warning("Đã từ chối bài viết!")
                    st.rerun()

        # KHU VỰC XUẤT BẢN TỰ ĐỘNG (AUTO-PUBLISH ENGINE)
        with st.container(border=True):
            st.markdown("###### 🚀 Xuất bản Tự động (Auto-Publish Engine)")
            st.caption("Tự động đăng bài viết kèm hình ảnh và hashtag lên Fanpage Facebook, Telegram hoặc Webhook.")
            
            c_dest, c_btn = st.columns([3, 2], gap="small")
            with c_dest:
                default_ch = selected_post.get("channel", "Facebook")
                target_dest = st.selectbox(
                    "Kênh xuất bản đích:",
                    ["Facebook Fanpage", "Telegram Channel", "Automation Webhook"],
                    index=0 if "face" in default_ch.lower() else (1 if "tele" in default_ch.lower() else 0),
                    key=f"dest_sel_{selected_post['id']}"
                )
            with c_btn:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                btn_auto_pub = st.button("⚡ Đăng bài ngay", key=f"btn_pub_now_{selected_post['id']}", type="primary", use_container_width=True)

            if btn_auto_pub:
                with st.spinner(f"Đang tự động phát hành lên {target_dest}..."):
                    receipt = execute_auto_publish(selected_post, channel=target_dest)
                    if receipt.get("success"):
                        conn = get_connection()
                        mark_post_as_published(conn, selected_post['id'], receipt.get("published_url", ""))
                        conn.close()
                        st.balloons()
                        st.success(f"🎉 {receipt.get('message')}")
                        st.markdown(f"**Mã bài đăng:** `{receipt.get('post_id')}` • **Chế độ:** `{receipt.get('mode')}`")
                        st.markdown(f"🔗 [Mở liên kết bài viết]({receipt.get('published_url')})")
                        time.sleep(1.2)
                        st.rerun()
                    else:
                        st.error(f"❌ Lỗi xuất bản: {receipt.get('message')}")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        with st.expander("✏️ Chỉnh sửa nhanh tiêu đề & nội dung", expanded=False):
            with st.form(f"edit_form_{selected_post['id']}"):
                edit_t = st.text_input("Tiêu đề bài viết:", value=selected_post["title"] or "")
                edit_c = st.text_area("Nội dung bài viết:", value=selected_post["content"], height=160)
                btn_save = st.form_submit_button("💾 Lưu thay đổi", use_container_width=True)
                if btn_save:
                    conn = get_connection()
                    update_post_content(conn, selected_post['id'], edit_t, edit_c)
                    conn.close()
                    st.success("Đã lưu nội dung bài viết!")
                    st.rerun()

        # MỤC ĐỔI HÌNH ẢNH CHO BÀI VIẾT NÀY
        with st.expander("🖼️ Đổi hình ảnh bài viết (Thư viện / Tải lên)", expanded=False):
            st.caption("Chọn hình ảnh từ Thư viện Media hoặc tải ảnh mới từ máy tính để hiển thị trên Mockup điện thoại & Bảng tin.")
            
            media_options = get_all_available_media()
            media_dict = {f"[{m.get('category')}] {m.get('title')}": m for m in media_options}
            
            t_pick, t_upl = st.tabs(["📚 Chọn từ Thư viện", "📤 Tải ảnh từ máy tính"])
            
            with t_pick:
                sel_lbl = st.selectbox("Chọn ảnh phù hợp:", options=list(media_dict.keys()), key=f"sel_img_{selected_post['id']}")
                picked_item = media_dict[sel_lbl]
                st.image(picked_item["url"], caption=picked_item["title"], use_container_width=True)
                
                if st.button("💾 Gán ảnh này cho bài viết", key=f"btn_apply_lib_{selected_post['id']}", type="primary", use_container_width=True):
                    conn = get_connection()
                    update_post_media(conn, selected_post['id'], picked_item["url"])
                    conn.close()
                    st.success("✅ Đã cập nhật hình ảnh thành công!")
                    st.rerun()

            with t_upl:
                up_file = st.file_uploader("Chọn ảnh từ máy tính (JPG, PNG, WebP):", type=["jpg", "jpeg", "png", "webp"], key=f"file_up_{selected_post['id']}")
                if up_file is not None:
                    st.image(up_file, caption="Ảnh xem trước vừa tải lên", use_container_width=True)
                    if st.button("💾 Lưu vào Thư viện & Gán ngay", key=f"btn_apply_up_{selected_post['id']}", type="primary", use_container_width=True):
                        saved = save_uploaded_media(up_file)
                        conn = get_connection()
                        update_post_media(conn, selected_post['id'], saved["url"])
                        conn.close()
                        st.success(f"✅ Đã lưu '{saved['title']}' vào Thư viện và gán vào bài viết!")
                        st.rerun()

# ============================================================
# TAB 2: DANH SÁCH BÀI VIẾT & LỊCH ĐĂNG
# ============================================================
with tab_list:
    st.markdown("##### 📅 Lịch phát hành và kiểm duyệt hàng loạt")
    
    col_f1, col_f2 = st.columns(2, gap="medium")
    with col_f1:
        stg_filter = st.selectbox("Lọc giai đoạn:", ["Tất cả", "Teaser", "Launch", "CTA"], key="list_stg")
    with col_f2:
        sta_filter = st.selectbox("Lọc trạng thái:", ["Tất cả", "Pending", "Approved", "Rejected"], key="list_sta")

    f_posts = posts
    if stg_filter != "Tất cả":
        f_posts = [p for p in f_posts if p["stage"] == stg_filter]
    if sta_filter != "Tất cả":
        f_posts = [p for p in f_posts if p["status"] == sta_filter]

    st.caption(f"Hiển thị {len(f_posts)} / {len(posts)} bài viết")

    for p in f_posts:
        with st.expander(f"📌 [{p['stage']}] [{p['channel']}] #{p['id']} - {p['title'] or 'Không có tiêu đề'}  •  📅 {p.get('scheduled_date')}", expanded=False):
            render_social_mockup(p, brand_name=selected_camp_name)


# ============================================================
# TAB 3: THƯ VIỆN HÌNH ẢNH (MEDIA ASSETS GALLERY)
# ============================================================
with tab_media:
    st.markdown("##### 🖼️ Quản lý Thư viện Ảnh Chiến dịch & Tài nguyên Media")
    st.caption("Tải lên ảnh sản phẩm của bạn hoặc lựa chọn từ kho ảnh chuyên nghiệp chuẩn ngành để gắn vào bài viết marketing.")

    # 1. KHU VỰC TẢI ẢNH MỚI LÊN
    with st.container(border=True):
        st.markdown("###### 📤 Tải ảnh mới lên Thư viện nội bộ")
        st.caption("Các file tải lên sẽ được lưu trữ an toàn trong thư mục `assets/media_library` của dự án và sẵn sàng sử dụng cho mọi bài viết.")
        
        multi_files = st.file_uploader(
            "Kéo thả hoặc chọn các ảnh sản phẩm từ máy tính (Hỗ trợ JPG, PNG, WebP):",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
            key="bulk_media_upload"
        )
        if multi_files:
            c_up_btn, c_up_info = st.columns([1, 2])
            with c_up_btn:
                if st.button("🚀 Lưu tất cả vào Thư viện", type="primary", use_container_width=True):
                    saved_cnt = 0
                    for mf in multi_files:
                        save_uploaded_media(mf)
                        saved_cnt += 1
                    st.success(f"🎉 Đã tải lên và lưu thành công {saved_cnt} hình ảnh vào Thư viện!")
                    st.rerun()
            with c_up_info:
                st.info(f"Đã chọn {len(multi_files)} tệp sẵn sàng nạp vào hệ thống.")

    # 2. BỘ CÔNG CỤ GÁN ẢNH HÀNG LOẠT CHO BÀI VIẾT
    with st.container(border=True):
        st.markdown("###### ⚡ Gán nhanh ảnh cho hàng loạt bài viết theo Giai đoạn phễu")
        st.caption("Tiết kiệm thời gian bằng cách chọn 1 hình ảnh đại diện và áp dụng tự động cho toàn bộ bài viết trong một giai đoạn.")
        
        all_avail = get_all_available_media()
        all_choices = {f"[{m.get('category')}] {m.get('title')}": m["url"] for m in all_avail}
        
        col_g1, col_g2, col_g3 = st.columns([1, 2, 1], gap="medium")
        with col_g1:
            target_stage = st.selectbox("Chọn giai đoạn phễu:", ["Teaser", "Launch", "CTA"], key="batch_stage")
        with col_g2:
            batch_img_lbl = st.selectbox("Chọn ảnh áp dụng:", options=list(all_choices.keys()), key="batch_img_sel")
            chosen_batch_url = all_choices[batch_img_lbl]
        with col_g3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button(f"Áp dụng cho bài {target_stage}", type="secondary", use_container_width=True):
                conn = get_connection()
                cur = conn.cursor()
                is_pg = hasattr(conn, "info")
                ph = "%s" if is_pg else "?"
                cur.execute(
                    f"UPDATE campaign_posts SET media_url = {ph} WHERE campaign_id = {ph} AND stage = {ph}",
                    (chosen_batch_url, selected_camp_id, target_stage)
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success(f"✅ Đã gán ảnh thành công cho tất cả bài viết {target_stage}!")
                st.rerun()

    # 3. GALLERY HIỂN THỊ DANH MỤC ẢNH
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("##### 🎨 Bộ sưu tập Hình ảnh hiện có")
    
    cat_filter = st.radio(
        "Lọc theo danh mục:",
        ["Tất cả", "Ảnh tải lên từ máy tính", "Công nghệ & Smartphone", "Mỹ phẩm & Skincare", "F&B & Ẩm thực", "Thời trang & Lifestyle", "Khuyến mãi & Sự kiện"],
        horizontal=True,
        key="cat_filter_radio"
    )
    
    displayed_media = all_avail
    if cat_filter != "Tất cả":
        displayed_media = [m for m in all_avail if m.get("category") == cat_filter]

    st.caption(f"Đang hiển thị {len(displayed_media)} hình ảnh")

    if not displayed_media:
        st.info("Chưa có hình ảnh nào trong danh mục này. Hãy tải ảnh từ máy tính ở ô bên trên!")
    else:
        # Render grid 3 cột
        cols_per_row = 3
        for i in range(0, len(displayed_media), cols_per_row):
            row_items = displayed_media[i:i + cols_per_row]
            grid_cols = st.columns(cols_per_row)
            for j, item in enumerate(row_items):
                with grid_cols[j]:
                    with st.container(border=True):
                        st.image(item["url"], use_container_width=True)
                        badge_type = "🟢 Máy tính" if item.get("is_local") else "🌐 Mẫu chuẩn"
                        st.markdown(f"**{item.get('title')}**")
                        st.caption(f"📁 {item.get('category')} • {badge_type}")
