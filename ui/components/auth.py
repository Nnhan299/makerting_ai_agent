"""
Module xác thực & quản lý phiên đăng nhập (Authentication & Session Guard).
Tích hợp giao diện Đăng nhập bảo mật, phân quyền nghiêm ngặt theo vai trò từ Database.
Người dùng bình thường KHÔNG được tự ý đổi vai trò; chỉ Admin mới có quyền quản lý.
"""

import streamlit as st
from database.connection import get_connection
from database.crud import authenticate_user


def get_current_user() -> dict:
    """Lấy thông tin người dùng đang đăng nhập."""
    return st.session_state.get("user")


def is_authenticated() -> bool:
    """Kiểm tra xem người dùng đã đăng nhập chưa."""
    return st.session_state.get("authenticated", False) and st.session_state.get("user") is not None


def logout():
    """Đăng xuất khỏi hệ thống."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    if "user_role" in st.session_state:
        del st.session_state["user_role"]
    st.rerun()


def render_login_screen():
    """
    Render giao diện đăng nhập cao cấp (Modern Glassmorphic Login Card).
    Bảo vệ ứng dụng và cung cấp các nút Demo 1-Click tiện lợi cho hội đồng chấm / báo cáo.
    """
    # Ẩn hoàn toàn thanh menu (sidebar) và nút toggle khi chưa đăng nhập
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"],
            section[data-testid="stSidebar"],
            [data-testid="collapsedControl"],
            button[kind="header"] {
                display: none !important;
            }
            .main .block-container {
                max-width: 880px !important;
                padding-top: 2.5rem !important;
                margin: 0 auto !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center; margin-top: 10px; margin-bottom: 25px;">
            <div style="
                display: inline-flex; align-items: center; justify-content: center;
                width: 64px; height: 64px; border-radius: 16px;
                background: linear-gradient(135deg, #6366F1, #8B5CF6);
                box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
                font-size: 2rem; margin-bottom: 12px;
            ">
                🤖
            </div>
            <h1 style="
                font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em;
                background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 50%, #818CF8 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                margin: 0;
            ">
                Marketing AI Campaign Manager
            </h1>
            <p style="color: #94A3B8; font-size: 1rem; margin-top: 6px;">
                Hệ thống Multi-Agent Tự động hóa Chiến dịch Marketing Đa kênh
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_left, c_center, c_right = st.columns([1, 1.4, 1])
    
    with c_center:
        st.markdown(
            """
            <div style="
                background: #111827; 
                border: 1px solid rgba(255, 255, 255, 0.12); 
                border-radius: 18px; 
                padding: 28px 24px 20px 24px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
            ">
                <div style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">
                    Đăng nhập hệ thống
                </div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 18px;">
                    Vui lòng nhập tài khoản được cấp quyền để truy cập Workspace
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("login_form", clear_on_submit=False):
            username_input = st.text_input("Tên đăng nhập (Username):", placeholder="Ví dụ: nhan, admin, creator")
            password_input = st.text_input("Mật khẩu (Password):", type="password", placeholder="••••••••")
            submit_btn = st.form_submit_button("🚀 Đăng nhập Workspace", type="primary", use_container_width=True)

            if submit_btn:
                if not username_input or not password_input:
                    st.error("Vui lòng điền đầy đủ tên đăng nhập và mật khẩu!")
                else:
                    try:
                        conn = get_connection()
                        user = authenticate_user(conn, username_input, password_input)
                        conn.close()

                        if user:
                            st.session_state["authenticated"] = True
                            st.session_state["user"] = user
                            st.session_state["user_role"] = user["role"]
                            st.success(f"Xin chào {user['full_name']}! Đang chuyển hướng...")
                            st.rerun()
                        else:
                            st.error("Tên đăng nhập hoặc mật khẩu không chính xác, hoặc tài khoản đã bị vô hiệu hóa.")
                    except Exception as exc:
                        st.error(f"Lỗi kết nối xác thực: {exc}")

        # Quick Demo Buttons for Evaluators
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 0.78rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 8px; text-align: center;">
                ⚡ Đăng nhập nhanh để trải nghiệm (Demo 1-Click)
            </div>
            """,
            unsafe_allow_html=True
        )

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            if st.button("👑 Admin", help="Tài khoản Quản trị viên (Toàn quyền)", use_container_width=True):
                conn = get_connection()
                user = authenticate_user(conn, "admin", "admin123")
                conn.close()
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = user
                    st.session_state["user_role"] = user["role"]
                    st.rerun()

        with col_d2:
            if st.button("🎯 Lead", help="Tài khoản Marketing Lead (Duyệt bài)", use_container_width=True):
                conn = get_connection()
                user = authenticate_user(conn, "nhan", "nhan1903")
                conn.close()
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = user
                    st.session_state["user_role"] = user["role"]
                    st.rerun()

        with col_d3:
            if st.button("✍️ Creator", help="Tài khoản Content Creator (Tạo nội dung)", use_container_width=True):
                conn = get_connection()
                user = authenticate_user(conn, "creator", "creator123")
                conn.close()
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = user
                    st.session_state["user_role"] = user["role"]
                    st.rerun()


def require_auth() -> dict:
    """
    Bảo vệ trang yêu cầu đăng nhập.
    Nếu chưa đăng nhập: hiển thị màn hình đăng nhập và ngắt luồng thực thi (st.stop()).
    """
    if not is_authenticated():
        render_login_screen()
        st.stop()
    return get_current_user()


def require_admin() -> dict:
    """
    Bảo vệ trang Quản trị (Admin-only).
    Chỉ cho phép tài khoản có role == 'Admin' truy cập.
    """
    user = require_auth()
    if user.get("role") != "Admin":
        st.markdown(
            f"""
            <div style="
                background: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 14px;
                padding: 24px;
                text-align: center;
                margin-top: 40px;
            ">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">⛔</div>
                <h3 style="color: #F87171; margin-bottom: 6px;">Quyền truy cập bị từ chối</h3>
                <p style="color: #CBD5E1; font-size: 0.95rem;">
                    Trang này dành riêng cho <strong>Quản trị viên (Admin)</strong>.<br>
                    Tài khoản của bạn hiện tại là <strong>{user.get('full_name')}</strong> với vai trò: 
                    <span style="color: #38BDF8; font-weight: 700;">{user.get('role')}</span>.
                </p>
                <p style="color: #94A3B8; font-size: 0.82rem; margin-top: 12px;">
                    Người dùng thông thường không được quyền tự thay đổi vai trò. Vui lòng liên hệ Admin để được phân quyền.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.stop()
    return user

