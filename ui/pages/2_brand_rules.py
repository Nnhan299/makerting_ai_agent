"""
Trang 2: Quản lý Quy tắc Thương hiệu (Module 2 - Brand Rules Manager)
Giao diện Dark Glassmorphism với Keyword Chips & Tag Preview.
"""

import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.connection import get_connection
from database.crud import (
    create_brand_rule,
    get_all_brand_rules,
    delete_brand_rule
)
from ui.components.auth import require_auth
from ui.components.sidebar import render_sidebar
from ui.components.navbar import render_dynamic_dock
from ui.components.theme import (
    apply_custom_theme,
    render_page_header
)

st.set_page_config(page_title="Quy tắc Thương hiệu - Marketing AI", page_icon="🛡️", layout="wide")
apply_custom_theme()
require_auth()
render_sidebar()
render_dynamic_dock("brand_rules")

render_page_header(
    title="Bộ Quy tắc Thương hiệu (Brand Rules)",
    subtitle="Thiết lập tiêu chuẩn kiểm duyệt từ cấm, từ bắt buộc và phong cách giọng điệu (Tone of Voice)",
    badge="MODULE 2 • BRAND AUDIT ENGINE"
)

tab1, tab2 = st.tabs(["📜 Danh sách Bộ Quy tắc", "➕ Thêm Bộ Quy tắc Mới"])

# ============================================================
# TAB 1: DANH SÁCH BỘ QUY TẮC
# ============================================================
with tab1:
    col_top1, col_top2 = st.columns([3, 1])
    with col_top1:
        st.caption("Các bộ quy tắc đang được áp dụng trong quá trình Agent 3 kiểm duyệt nội dung.")
    with col_top2:
        if st.button("Nạp nhanh quy tắc mẫu", type="secondary", width="stretch"):
            try:
                conn = get_connection()
                create_brand_rule(
                    conn=conn,
                    rule_name="Quy tắc Quảng cáo & Thương hiệu Việt Nam",
                    forbidden_words="tốt nhất, số 1, cam kết 100%, chữa khỏi, duy nhất, không tác dụng phụ",
                    mandatory_keywords="XYZ Cosmetics",
                    tone_of_voice="Chuyên nghiệp"
                )
                conn.close()
                st.success("✅ Đã nạp thành công bộ quy tắc mẫu!")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi: {e}")

    try:
        conn = get_connection()
        rules = get_all_brand_rules(conn)
        conn.close()
    except Exception as e:
        rules = []
        st.error(f"Lỗi tải danh sách quy tắc: {e}")

    if not rules:
        st.info("Chưa có bộ quy tắc nào. Hãy bấm nút 'Nạp nhanh Quy tắc Mẫu' ở trên hoặc chuyển sang tab 'Thêm Bộ Quy tắc Mới'.")
    else:
        for r in rules:
            forbidden_list = [w.strip() for w in (r.get("forbidden_words") or "").split(",") if w.strip()]
            mandatory_list = [w.strip() for w in (r.get("mandatory_keywords") or "").split(",") if w.strip()]
            
            forbidden_chips = " ".join([f'<span class="chip chip-rejected">🚫 {w}</span>' for w in forbidden_list]) if forbidden_list else "<span style='color:#64748B;'>Không có từ cấm</span>"
            mandatory_chips = " ".join([f'<span class="chip chip-approved">🔑 {w}</span>' for w in mandatory_list]) if mandatory_list else "<span style='color:#64748B;'>Không có từ bắt buộc</span>"

            with st.expander(f"🛡️ {r['rule_name']}  •  Tone: {r.get('tone_of_voice')}", expanded=False):
                st.markdown(
                    f"""
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 14px 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 12px;">
                        <div style="margin-bottom: 10px;">
                            <span class="chip chip-launch">🎭 Tone of Voice: <strong>{r.get('tone_of_voice')}</strong></span>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <div style="font-size: 0.78rem; font-weight: 700; color: #F43F5E; text-transform: uppercase; margin-bottom: 6px;">
                                Danh sách Từ Cấm (Forbidden Words):
                            </div>
                            <div>{forbidden_chips}</div>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <div style="font-size: 0.78rem; font-weight: 700; color: #10B981; text-transform: uppercase; margin-bottom: 6px;">
                                Từ khóa bắt buộc (Mandatory Keywords):
                            </div>
                            <div>{mandatory_chips}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                c_del, _ = st.columns([1, 4])
                with c_del:
                    if st.button("Xóa quy tắc này", key=f"del_rule_{r['id']}", type="secondary", width="stretch"):
                        conn = get_connection()
                        delete_brand_rule(conn, r['id'])
                        conn.close()
                        st.success("Đã xóa!")
                        st.rerun()

# ============================================================
# TAB 2: THÊM BỘ QUY TẮC MỚI
# ============================================================
with tab2:
    st.markdown("### ➕ Khởi tạo Bộ Quy tắc Thương hiệu")
    st.caption("Các điều kiện này sẽ được Agent 3 đối chiếu và phát hiện vi phạm tự động.")

    with st.form("create_rule_form", clear_on_submit=True):
        col_r1, col_r2 = st.columns(2, gap="medium")
        with col_r1:
            rule_name = st.text_input("Tên Bộ quy tắc *", placeholder="Vd: Tiêu chuẩn Dược mỹ phẩm 2026")
        with col_r2:
            tone_of_voice = st.selectbox(
                "Tone of Voice (Phong cách giọng điệu)",
                options=["Chuyên nghiệp", "Trẻ trung", "Trang trọng", "Gần gũi", "Hài hước"]
            )
        
        forbidden_words = st.text_area(
            "Danh sách Từ Cấm (Forbidden Words) - Phân tách bằng dấu phẩy",
            placeholder="Vd: tốt nhất, số 1, cam kết 100%, vĩnh viễn, triệt để, thần dược...",
            height=100
        )
        mandatory_keywords = st.text_area(
            "Danh sách Từ Bắt buộc xuất hiện (Mandatory Keywords) - Phân tách bằng dấu phẩy",
            placeholder="Vd: Tên thương hiệu bắt buộc (XYZ Cosmetics), slogan...",
            height=80
        )

        btn_save_rule = st.form_submit_button("Lưu bộ quy tắc", type="primary", width="stretch")

        if btn_save_rule:
            if not rule_name.strip():
                st.error("Vui lòng nhập tên bộ quy tắc!")
            else:
                try:
                    conn = get_connection()
                    rid = create_brand_rule(
                        conn=conn,
                        rule_name=rule_name.strip(),
                        forbidden_words=forbidden_words.strip(),
                        mandatory_keywords=mandatory_keywords.strip(),
                        tone_of_voice=tone_of_voice
                    )
                    conn.close()
                    st.success(f"✅ Đã lưu bộ quy tắc thành công! (ID: {rid})")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi: {e}")
