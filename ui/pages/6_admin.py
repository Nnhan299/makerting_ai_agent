"""
Trang 6: Quản trị Hệ thống & Quản lý Người dùng (Admin Control Center)
Chỉ Quản trị viên (Admin) mới có quyền truy cập trang này.
Cho phép tạo người dùng mới, phân quyền (đổi vai trò Role) và theo dõi tình trạng Database.
"""

import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.connection import get_connection, get_active_db_name
from database.crud import (
    get_all_users,
    create_user,
    update_user_role,
    update_user_status,
    delete_user,
    get_all_campaigns,
    get_all_brand_rules,
    get_all_posts,
    get_all_audits
)
from ui.components.auth import require_admin
from ui.components.sidebar import render_sidebar
from ui.components.navbar import render_dynamic_dock
from ui.components.theme import apply_custom_theme, render_page_header

st.set_page_config(page_title="Quản trị Hệ thống - Marketing AI", page_icon="👑", layout="wide")
apply_custom_theme()

# Bảo vệ quyền truy cập: Chỉ Admin mới được vào
current_admin = require_admin()

render_sidebar()
render_dynamic_dock("admin")

render_page_header(
    title="Trung tâm Quản trị Hệ thống (Admin Portal)",
    subtitle="Quản lý tài khoản, phân quyền vai trò (Role-based Access Control) và theo dõi cơ sở dữ liệu",
    badge="ADMINISTRATION • RBAC & SYSTEM"
)

tab_users, tab_db, tab_ai = st.tabs(["👥 Quản lý Người dùng & Phân quyền", "🗄️ Tình trạng Database", "⚙️ Cấu hình AI & API Keys (Admin/Dev)"])

# ============================================================
# TAB 1: QUẢN LÝ NGƯỜI DÙNG
# ============================================================
with tab_users:
    try:
        conn = get_connection()
        users_list = get_all_users(conn)
        conn.close()
    except Exception as e:
        users_list = []
        st.error(f"Lỗi lấy danh sách tài khoản: {e}")

    st.markdown(f"##### 📋 Danh sách tài khoản hệ thống ({len(users_list)} người dùng)")
    
    # Hiển thị bảng người dùng
    user_rows = []
    for u in users_list:
        role_badge = "👑 Admin" if u["role"] == "Admin" else ("🎯 Marketing Lead" if u["role"] == "Marketing Lead" else "✍️ Content Creator")
        status_badge = "🟢 Đang hoạt động" if u.get("is_active") else "🔴 Bị khóa"
        user_rows.append({
            "ID": u["id"],
            "Tên đăng nhập": u["username"],
            "Họ và tên": u["full_name"],
            "Email": u.get("email") or "—",
            "Vai trò (Role)": role_badge,
            "Trạng thái": status_badge,
            "Ngày tạo": str(u.get("created_at", ""))[:19]
        })
    
    st.dataframe(user_rows, use_container_width=True, hide_index=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    col_u1, col_u2 = st.columns(2, gap="large")

    # Form thêm người dùng mới
    with col_u1:
        with st.container(border=True):
            st.subheader("➕ Tạo người dùng mới")
            with st.form("create_user_form", clear_on_submit=True):
                new_username = st.text_input("Tên đăng nhập (Username)*:", placeholder="VD: minhtran")
                new_password = st.text_input("Mật khẩu ban đầu*:", type="password", placeholder="••••••••")
                new_fullname = st.text_input("Họ và tên*:", placeholder="VD: Trần Nhật Minh")
                new_email = st.text_input("Email:", placeholder="VD: minh.tran@marketing.ai")
                new_role = st.selectbox("Phân quyền vai trò (Role):", ["Content Creator", "Marketing Lead", "Admin"])
                
                submit_create = st.form_submit_button("Tạo người dùng", type="primary", use_container_width=True)
                
                if submit_create:
                    if not new_username or not new_password or not new_fullname:
                        st.error("Vui lòng điền đầy đủ các mục bắt buộc (*).")
                    else:
                        try:
                            conn = get_connection()
                            new_id = create_user(
                                conn=conn,
                                username=new_username,
                                password=new_password,
                                full_name=new_fullname,
                                email=new_email,
                                role=new_role
                            )
                            conn.close()
                            st.success(f"Đã tạo thành công người dùng '{new_username}' (ID: {new_id}) với vai trò '{new_role}'!")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Không thể tạo người dùng: {exc}")

    # Form chỉnh sửa quyền & trạng thái
    with col_u2:
        with st.container(border=True):
            st.subheader("⚡ Phân quyền & Quản lý vai trò")
            
            user_options = {f"{u['username']} — {u['full_name']} ({u['role']})": u['id'] for u in users_list}
            if not user_options:
                st.info("Chưa có người dùng để chỉnh sửa.")
            else:
                sel_user_str = st.selectbox("Chọn tài khoản cần điều chỉnh quyền:", options=list(user_options.keys()))
                sel_user_id = user_options[sel_user_str]
                sel_user = next((u for u in users_list if u['id'] == sel_user_id), None)
                
                if sel_user:
                    st.write(f"Đang cấu hình cho: **{sel_user['full_name']}** (`{sel_user['username']}`)")
                    
                    with st.form(f"edit_role_form_{sel_user_id}"):
                        new_assigned_role = st.selectbox(
                            "Gán vai trò mới cho tài khoản:",
                            ["Admin", "Marketing Lead", "Content Creator"],
                            index=["Admin", "Marketing Lead", "Content Creator"].index(sel_user["role"])
                        )
                        is_active_toggle = st.checkbox("Tài khoản đang hoạt động (Active)", value=bool(sel_user.get("is_active", True)))
                        
                        btn_save_role = st.form_submit_button("Cập nhật quyền hạn", type="primary", use_container_width=True)
                        if btn_save_role:
                            try:
                                conn = get_connection()
                                update_user_role(conn, sel_user_id, new_assigned_role)
                                update_user_status(conn, sel_user_id, is_active_toggle)
                                conn.close()
                                st.success("Cập nhật quyền hạn thành công!")
                                st.rerun()
                            except Exception as exc:
                                st.error(f"Lỗi cập nhật: {exc}")

                    # Nút xóa user (ngoại trừ chính admin đang đăng nhập)
                    if sel_user_id != current_admin["id"]:
                        if st.button("🗑️ Xóa tài khoản này", key=f"del_user_{sel_user_id}", type="secondary"):
                            conn = get_connection()
                            delete_user(conn, sel_user_id)
                            conn.close()
                            st.warning("Đã xóa tài khoản.")
                            st.rerun()

# ============================================================
# TAB 2: QUẢN TRỊ CƠ SỞ DỮ LIỆU & HỆ THỐNG
# ============================================================
with tab_db:
    st.markdown("##### 🔍 Kiểm tra tình trạng kết nối & bảng dữ liệu")
    
    active_db = get_active_db_name()
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        st.metric("Hệ thống Database đang dùng", active_db)
    with col_d2:
        st.metric("Số lượng tài khoản", len(users_list))
    with col_d3:
        st.metric("Trạng thái", "Sẵn sàng (Ready)")

    try:
        conn = get_connection()
        camps = get_all_campaigns(conn)
        rules = get_all_brand_rules(conn)
        posts = get_all_posts(conn)
        audits = get_all_audits(conn)
        conn.close()
        
        with st.container(border=True):
            st.markdown("###### 📊 Thống kê các bảng dữ liệu trong PostgreSQL")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Chiến dịch (campaigns)", len(camps))
            with c2:
                st.metric("Quy tắc (brand_rules)", len(rules))
            with c3:
                st.metric("Bài viết (campaign_posts)", len(posts))
            with c4:
                st.metric("Kiểm duyệt (audit_logs)", len(audits))
    except Exception as exc:
        st.error(f"Lỗi kiểm tra dữ liệu: {exc}")



# ============================================================
# TAB 3: CẤU HÌNH AI & API KEYS (DÀNH RIÊNG CHO ADMIN / DEV)
# ============================================================
with tab_ai:
    st.markdown("##### 🔐 Cấu hình Bảo mật Google Gemini API")
    st.caption("Khu vực kỹ thuật dành riêng cho Quản trị viên và Developer. Nhân viên thông thường không thể thấy hoặc chỉnh sửa các tham số này.")
    
    current_key = os.getenv("GEMINI_API_KEY", "")
    is_set = bool(current_key and current_key != "your_gemini_api_key_here")
    
    col_k1, col_k2 = st.columns([2, 1], gap="medium")
    
    with col_k1:
        with st.container(border=True):
            st.markdown("###### 🔑 Trạng thái Gemini API Key")
            if is_set:
                masked = current_key[:6] + "..." + current_key[-4:] if len(current_key) > 10 else "Đã thiết lập"
                st.success(f"✅ Đã kết nối API Key: `{masked}`")
            else:
                st.warning("⚠️ Chưa cấu hình GEMINI_API_KEY: Hệ thống đang chạy ở chế độ **Smart Demo Generator** tự động.")

            new_key = st.text_input("Cập nhật Gemini API Key mới:", type="password", placeholder="AIzaSy...")
            
            if st.button("💾 Lưu và Cập nhật API Key", type="primary"):
                if new_key.strip():
                    os.environ["GEMINI_API_KEY"] = new_key.strip()
                    env_file = os.path.join(BASE_DIR, ".env")
                    if os.path.exists(env_file):
                        try:
                            with open(env_file, "r", encoding="utf-8") as f_env:
                                lines = f_env.readlines()
                            found = False
                            for i, l in enumerate(lines):
                                if l.strip().startswith("GEMINI_API_KEY="):
                                    lines[i] = f"GEMINI_API_KEY={new_key.strip()}\n"
                                    found = True
                                    break
                            if not found:
                                lines.append(f"\nGEMINI_API_KEY={new_key.strip()}\n")
                            with open(env_file, "w", encoding="utf-8") as f_env:
                                f_env.writelines(lines)
                        except Exception as e:
                            st.warning(f"Không thể ghi file .env: {e}")
                    st.success("✅ Đã cập nhật GEMINI_API_KEY thành công vào hệ thống!")
                    st.rerun()
                else:
                    st.error("Vui lòng nhập API Key hợp lệ.")

    with col_k2:
        with st.container(border=True):
            st.markdown("###### ⚡ Kiểm tra kết nối AI")
            st.caption("Thử nghiệm gọi nhanh Google Gemini để xác thực API Key hoạt động bình thường.")
            if st.button("🧪 Kiểm tra API Ping", width="stretch"):
                with st.spinner("Đang kiểm tra kết nối tới Google Gemini..."):
                    try:
                        from utils.llm_client import LLMClient
                        client = LLMClient()
                        if client.is_configured:
                            resp = client.call("Bạn là AI Assistant.", "Trả lời ngắn gọn 1 câu: Hệ thống AI Marketing đã kết nối thành công chưa?")
                            st.success(f"🎉 Kết nối thành công!\n\nAI phản hồi: *\"{resp.strip()}\"*")
                        else:
                            st.info("ℹ️ Đang hoạt động ở chế độ Smart Demo Generator.")
                    except Exception as err:
                        st.error(f"❌ Kết nối thất bại: {err}")

    st.markdown("---")
    st.markdown("##### 🌐 Cấu hình Tự Động Xuất Bản Mạng Xã Hội (Social Publishing API)")
    st.caption("Cấu hình cổng kết nối tự động với Facebook Fanpage, Telegram Channel hoặc Webhook tự động hóa.")
    
    col_s1, col_s2 = st.columns(2, gap="medium")
    
    with col_s1:
        with st.container(border=True):
            st.markdown("###### 📘 Facebook Fanpage (Meta Graph API)")
            curr_fb_token = os.getenv("FB_PAGE_ACCESS_TOKEN", "")
            curr_fb_id = os.getenv("FB_PAGE_ID", "")
            
            fb_pid_in = st.text_input("Facebook Page ID:", value=curr_fb_id, placeholder="Ví dụ: 109827364521...")
            fb_token_in = st.text_input("Facebook Page Access Token:", value=curr_fb_token, type="password", placeholder="EAAG...")
            
            if st.button("💾 Lưu cấu hình Facebook", key="btn_save_fb"):
                os.environ["FB_PAGE_ACCESS_TOKEN"] = fb_token_in.strip()
                os.environ["FB_PAGE_ID"] = fb_pid_in.strip()
                env_file = os.path.join(BASE_DIR, ".env")
                if os.path.exists(env_file):
                    with open(env_file, "r", encoding="utf-8") as f_e:
                        e_lines = f_e.readlines()
                    keys_to_set = {"FB_PAGE_ACCESS_TOKEN": fb_token_in.strip(), "FB_PAGE_ID": fb_pid_in.strip()}
                    for k, v in keys_to_set.items():
                        found = False
                        for i_line, l_text in enumerate(e_lines):
                            if l_text.strip().startswith(f"{k}="):
                                e_lines[i_line] = f"{k}={v}\n"
                                found = True
                                break
                        if not found:
                            e_lines.append(f"{k}={v}\n")
                    with open(env_file, "w", encoding="utf-8") as f_e:
                        f_e.writelines(e_lines)
                st.success("✅ Đã lưu cấu hình Facebook Fanpage!")
                st.rerun()

    with col_s2:
        with st.container(border=True):
            st.markdown("###### ⚡ Webhook Tự Động Hóa (Make.com / Zapier / Telegram)")
            curr_hook = os.getenv("WEBHOOK_PUBLISH_URL", "")
            hook_in = st.text_input("Webhook URL:", value=curr_hook, placeholder="https://hook.eu1.make.com/...")
            curr_tg = os.getenv("TELEGRAM_BOT_TOKEN", "")
            curr_tg_chat = os.getenv("TELEGRAM_CHAT_ID", "")
            tg_in = st.text_input("Telegram Bot Token (Tùy chọn):", value=curr_tg, type="password", placeholder="123456:ABC-DEF...")
            tg_chat_in = st.text_input("Telegram Chat ID / Channel:", value=curr_tg_chat, placeholder="@MyBrandChannel")

            if st.button("💾 Lưu cấu hình Webhook & Telegram", key="btn_save_hook"):
                os.environ["WEBHOOK_PUBLISH_URL"] = hook_in.strip()
                os.environ["TELEGRAM_BOT_TOKEN"] = tg_in.strip()
                os.environ["TELEGRAM_CHAT_ID"] = tg_chat_in.strip()
                st.success("✅ Đã lưu cấu hình Webhook & Telegram thành công!")
                st.rerun()
