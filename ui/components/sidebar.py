"""Shared native sidebar for the Streamlit app with Authentication & RBAC."""

import streamlit as st
from database.connection import get_active_db_name

ROLE_PERMISSIONS = {
    "Marketing Lead": {
        "badge_color": "#10B981",
        "icon": "🎯",
        "desc": "Toàn quyền Duyệt & Xuất bản chiến dịch",
        "can_approve": True,
        "can_edit": True,
        "can_run_ai": True,
    },
    "Content Creator": {
        "badge_color": "#3B82F6",
        "icon": "✍️",
        "desc": "Chạy AI Pipeline & Soạn thảo nội dung (Cần Lead duyệt)",
        "can_approve": False,
        "can_edit": True,
        "can_run_ai": True,
    },
    "Admin": {
        "badge_color": "#8B5CF6",
        "icon": "👑",
        "desc": "Quản trị toàn bộ dữ liệu, người dùng & phân quyền",
        "can_approve": True,
        "can_edit": True,
        "can_run_ai": True,
    }
}


def get_current_role() -> str:
    """Lấy vai trò hiện tại của người dùng."""
    user = st.session_state.get("user")
    if user and isinstance(user, dict):
        return user.get("role", "Marketing Lead")
    return st.session_state.get("user_role", "Marketing Lead")


def get_role_permissions() -> dict:
    """Lấy quyền hạn của vai trò hiện tại."""
    role = get_current_role()
    return ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS["Marketing Lead"])


def render_sidebar():
    with st.sidebar:
        st.html(
            """
            <style>
                [data-testid="stSidebarNav"] { display: none; }
                [data-testid="stSidebar"] { min-width: 290px; max-width: 290px; }
                [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
                    min-height: 42px;
                    margin: 3px 0;
                    border-radius: 8px;
                    font-weight: 600;
                    display: flex;
                    align-items: center;
                    padding: 8px 14px;
                    text-decoration: none;
                    transition: all 0.15s ease-in-out;
                }
            </style>
            """
        )
        
        user = st.session_state.get("user")
        if user and isinstance(user, dict):
            current_role = user.get("role", "Marketing Lead")
            full_name = user.get("full_name", "Người dùng")
            username = user.get("username", "user")
            initial = full_name[0].upper() if full_name else "U"
            role_meta = ROLE_PERMISSIONS.get(current_role, ROLE_PERMISSIONS["Marketing Lead"])
            
            # User profile card (Non-editable for regular users)
            st.markdown(
                f"""
                <div style="
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 12px;
                    padding: 12px 14px;
                    margin-bottom: 8px;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                ">
                    <div style="
                        width: 40px; height: 40px; border-radius: 50%;
                        background: linear-gradient(135deg, #6366F1, #8B5CF6);
                        display: flex; align-items: center; justify-content: center;
                        font-weight: 800; color: white; font-size: 1.1rem;
                        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
                    ">
                        {initial}
                    </div>
                    <div style="flex: 1; min-width: 0;">
                        <div style="font-weight: 700; color: #F8FAFC; font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            {full_name}
                        </div>
                        <div style="
                            font-size: 0.75rem; color: {role_meta['badge_color']}; font-weight: 700;
                            display: flex; align-items: center; gap: 4px; margin-top: 2px;
                        ">
                            <span>{role_meta['icon']}</span>
                            <span>{current_role}</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Nút đăng xuất
            if st.button("🚪 Đăng xuất", use_container_width=True, type="secondary"):
                from ui.components.auth import logout
                logout()

        st.divider()
        st.caption("WORKSPACE")
        
        pages = [
            ("app.py", "Dashboard", ":material/dashboard:"),
            ("pages/1_campaigns.py", "Campaigns", ":material/folder_open:"),
            ("pages/2_brand_rules.py", "Brand rules", ":material/shield:"),
            ("pages/3_run_ai.py", "Run AI Pipeline", ":material/auto_awesome:"),
            ("pages/4_calendar.py", "Xem trước & Duyệt bài", ":material/visibility:"),
            ("pages/5_export.py", "Reports & Export", ":material/download:"),
        ]
        
        # Nếu là Admin, hiển thị thêm trang Admin Portal
        if user and user.get("role") == "Admin":
            pages.append(("pages/6_admin.py", "Admin Portal", ":material/admin_panel_settings:"))

        for target, label, icon in pages:
            st.page_link(target, label=label, icon=icon)
            
        st.divider()
        st.caption("SYSTEM STATUS")
        active_db = get_active_db_name()
        st.success(f"{active_db} active", icon=":material/database:")
        st.info("3 agents pipeline ready", icon=":material/auto_awesome:")
        st.caption("Version 2.1 • Enterprise RBAC")
