"""
Navbar component - Dynamic Dock điều hướng trang hiện đại.
"""
import streamlit as st
from streamlit_option_menu import option_menu

PAGES_CONFIG = [
    {"id": "app", "name": "Dashboard", "icon": "speedometer2", "target": "app.py"},
    {"id": "campaigns", "name": "Chiến dịch", "icon": "folder2-open", "target": "pages/1_campaigns.py"},
    {"id": "brand_rules", "name": "Brand Rules", "icon": "shield-check", "target": "pages/2_brand_rules.py"},
    {"id": "run_ai", "name": "Chạy AI", "icon": "robot", "target": "pages/3_run_ai.py"},
    {"id": "calendar", "name": "Content Calendar", "icon": "calendar3", "target": "pages/4_calendar.py"},
    {"id": "export", "name": "Xuất bản", "icon": "box-arrow-up-right", "target": "pages/5_export.py"}
]


def render_dynamic_dock(current_page="app"):
    """
    Hiển thị macOS style Floating Dynamic Dock ở đầu mỗi trang để chuyển nhanh giữa các module.
    """
    names = [p["name"] for p in PAGES_CONFIG]
    icons = [p["icon"] for p in PAGES_CONFIG]
    targets = {p["name"]: p["target"] for p in PAGES_CONFIG}
    
    current_idx = 0
    for idx, p in enumerate(PAGES_CONFIG):
        if p["id"] == current_page:
            current_idx = idx
            break
            
    selected = option_menu(
        menu_title=None,
        options=names,
        icons=icons,
        default_index=current_idx,
        orientation="horizontal",
        key=f"dock_menu_{current_page}",
        styles={
            "container": {
                "padding": "6px 12px",
                "background": "rgba(15, 23, 42, 0.90)",
                "backdrop-filter": "blur(20px)",
                "-webkit-backdrop-filter": "blur(20px)",
                "border": "1px solid rgba(255, 255, 255, 0.12)",
                "border-radius": "50px",
                "box-shadow": "0 16px 36px -10px rgba(0, 0, 0, 0.7), 0 0 25px rgba(99, 102, 241, 0.25)",
                "margin": "0 auto 24px auto",
                "max-width": "960px",
            },
            "icon": {
                "color": "#818CF8",
                "font-size": "15px",
                "margin-right": "6px"
            },
            "nav-link": {
                "font-size": "13px",
                "font-weight": "600",
                "font-family": "'Plus Jakarta Sans', sans-serif",
                "text-align": "center",
                "margin": "0 3px",
                "padding": "8px 14px",
                "border-radius": "50px",
                "color": "#94A3B8",
                "--hover-color": "rgba(255, 255, 255, 0.08)",
                "transition": "all 0.2s ease"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)",
                "color": "#FFFFFF",
                "font-weight": "700",
                "box-shadow": "0 4px 15px rgba(99, 102, 241, 0.5)",
                "border": "none"
            }
        }
    )
    
    if selected and targets.get(selected) and PAGES_CONFIG[current_idx]["name"] != selected:
        st.switch_page(targets[selected])
