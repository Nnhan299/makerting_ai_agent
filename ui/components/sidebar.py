"""
Sidebar component cao cấp cho giao diện Streamlit.
"""

import streamlit as st


def render_sidebar():
    """
    Hiển thị sidebar navigation sang trọng và bảng điều khiển trạng thái hệ thống.
    """
    with st.sidebar:
        # App Logo & Branding Header
        st.markdown(
            """
            <div style="padding: 12px 4px 18px 4px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                    <div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #6366F1, #A855F7); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);">
                        ⚡
                    </div>
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: -0.02em; color: #FFFFFF;">Marketing AI</div>
                        <div style="font-size: 0.72rem; color: #818CF8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em;">Multi-Agent Suite</div>
                    </div>
                </div>
                <div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.4; margin-top: 6px;">
                    Nền tảng Quản trị & Tự động hóa Chiến dịch Marketing đa tác tử.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); margin-bottom: 16px;"></div>
            """,
            unsafe_allow_html=True
        )

        # System Health Card
        st.markdown(
            """
            <div style="background: rgba(17, 24, 39, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 12px; margin-bottom: 20px;">
                <div style="font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px;">
                    System Infrastructure
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem;">
                        <span style="color: #CBD5E1;">🐘 PostgreSQL DB</span>
                        <span style="display: inline-flex; align-items: center; gap: 5px; color: #34D399; font-weight: 600; font-size: 0.75rem;">
                            <span style="width: 6px; height: 6px; border-radius: 50%; background-color: #34D399; box-shadow: 0 0 6px #34D399;"></span>
                            Connected
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem;">
                        <span style="color: #CBD5E1;">✨ Gemini 1.5 Pro</span>
                        <span style="display: inline-flex; align-items: center; gap: 5px; color: #38BDF8; font-weight: 600; font-size: 0.75rem;">
                            <span style="width: 6px; height: 6px; border-radius: 50%; background-color: #38BDF8; box-shadow: 0 0 6px #38BDF8;"></span>
                            Ready
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem;">
                        <span style="color: #CBD5E1;">🚀 Multi-Agent</span>
                        <span style="color: #818CF8; font-weight: 600; font-size: 0.75rem;">3 Agents</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("Trang tính năng nằm ở menu trên của Sidebar.")
        
        st.markdown(
            """
            <div style="position: fixed; bottom: 12px; left: 16px; font-size: 0.7rem; color: #475569;">
                Marketing AI Platform v1.0.0
            </div>
            """,
            unsafe_allow_html=True
        )
