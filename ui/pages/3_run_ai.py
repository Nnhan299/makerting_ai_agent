"""
Trang 3: Chạy AI Multi-Agent Pipeline (Module 3 - Multi-Agent Engine)
Giao diện Pipeline Stepper hiện đại, theo dõi tiến trình 3 AI Agent thời gian thực.
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
    get_all_brand_rules,
    get_campaign_by_id,
    get_brand_rule_by_id
)
from utils.llm_client import LLMClient
from agents.orchestrator import AgentOrchestrator
from ui.components.sidebar import render_sidebar
from ui.components.navbar import render_dynamic_dock
from ui.components.theme import (
    apply_custom_theme,
    render_page_header,
    render_kpi_card,
    get_status_chip
)

st.set_page_config(page_title="Chạy AI Pipeline - Marketing AI", page_icon="🤖", layout="wide")
apply_custom_theme()
render_sidebar()
render_dynamic_dock("run_ai")

render_page_header(
    title="AI Multi-Agent Pipeline Console",
    subtitle="Kích hoạt luồng phối hợp tự động giữa 3 tác tử: Phân tích Thị trường ➔ Sáng tạo Nội dung ➔ Kiểm duyệt Thương hiệu",
    badge="MODULE 3 • PIPELINE ORCHESTRATION"
)

try:
    conn = get_connection()
    campaigns = get_all_campaigns(conn)
    rules = get_all_brand_rules(conn)
    conn.close()
except Exception as e:
    campaigns = []
    rules = []
    st.error(f"Lỗi kết nối cơ sở dữ liệu: {e}")

if not campaigns:
    st.warning("⚠️ Chưa có chiến dịch nào! Vui lòng sang trang **1_campaigns** để khởi tạo Brief trước.")
    st.stop()

if not rules:
    st.warning("⚠️ Chưa có bộ quy tắc thương hiệu nào! Vui lòng sang trang **2_brand_rules** để tạo trước.")
    st.stop()

# 1. BỘ CHỌN CHIẾN DỊCH & BỘ QUY TẮC
col_sel1, col_sel2 = st.columns(2, gap="medium")

with col_sel1:
    camp_options = {f"[{c['status']}] {c['name']} (ID: {c['id']})": c['id'] for c in campaigns}
    selected_camp_str = st.selectbox("🎯 Chọn Chiến dịch Marketing để xử lý", options=list(camp_options.keys()))
    selected_camp_id = camp_options[selected_camp_str]

with col_sel2:
    rule_options = {f"{r['rule_name']} (Tone: {r['tone_of_voice']})": r['id'] for r in rules}
    selected_rule_str = st.selectbox("🛡️ Chọn Tiêu chuẩn Quy tắc Thương hiệu", options=list(rule_options.keys()))
    selected_rule_id = rule_options[selected_rule_str]

selected_camp = next((c for c in campaigns if c["id"] == selected_camp_id), None)
selected_rule = next((r for r in rules if r["id"] == selected_rule_id), None)

# 2. PREVIEW BRIEF & RULE DẠNG GLASSMORPHIC CARD
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
col_card1, col_card2 = st.columns(2, gap="medium")

with col_card1:
    st.markdown(
        f"""
        <div style="background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 16px; min-height: 140px;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #818CF8; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;">
                📄 Campaign Brief Preview
            </div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">{selected_camp['name']}</div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 8px;">Sản phẩm: <span style="color: #CBD5E1;">{selected_camp['product_name']}</span></div>
            <div style="font-size: 0.8rem; color: #64748B;">Đối tượng: {selected_camp.get('target_audience') or 'Chưa nhập'}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_card2:
    st.markdown(
        f"""
        <div style="background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 16px; min-height: 140px;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #34D399; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;">
                🛡️ Brand Guidelines Preview
            </div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">{selected_rule['rule_name']}</div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 8px;">Tone of Voice: <span style="color: #818CF8; font-weight: 600;">{selected_rule['tone_of_voice']}</span></div>
            <div style="font-size: 0.8rem; color: #64748B;">Từ cấm kiểm duyệt: {selected_rule.get('forbidden_words') or 'Không có'}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 3. PIPELINE STEPPER DIAGRAM
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="step-container">
        <div class="step-item">
            <div class="step-num step-num-active">1</div>
            <div>
                <div class="step-info-title">Agent 1: Market Intelligence</div>
                <div class="step-info-desc">Phân tích Persona, Pain Points, USP</div>
            </div>
        </div>
        <div style="color: #64748B; font-size: 1.2rem;">➔</div>
        <div class="step-item">
            <div class="step-num step-num-pending">2</div>
            <div>
                <div class="step-info-title">Agent 2: Copywriter</div>
                <div class="step-info-desc">Sinh 20-30 bài theo phễu 3 giai đoạn</div>
            </div>
        </div>
        <div style="color: #64748B; font-size: 1.2rem;">➔</div>
        <div class="step-item">
            <div class="step-num step-num-pending">3</div>
            <div>
                <div class="step-info-title">Agent 3: Brand Auditor</div>
                <div class="step-info-desc">Kiểm duyệt từ cấm & chấm điểm</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 4. KÍCH HOẠT PIPELINE
btn_trigger = st.button("🚀 KÍCH HOẠT AI MULTI-AGENT PIPELINE NGAY", type="primary", use_container_width=True)

if btn_trigger:
    st.markdown("### 🔄 Trạng thái Xử lý Trực tiếp")
    prog_bar = st.progress(0)
    status_box = st.empty()
    log_expander = st.expander("📜 Chi tiết Agent Logs (Thời gian thực)", expanded=True)

    def on_progress(step: int, total: int, msg: str):
        pct = int((step / total) * 100)
        prog_bar.progress(pct)
        status_box.markdown(f"**Bước {step}/{total}:** {msg}")

    try:
        conn = get_connection()
        llm = LLMClient()
        orchestrator = AgentOrchestrator(llm_client=llm, db_connection=conn)
        
        t0 = time.time()
        pipeline_output = orchestrator.run_pipeline(
            campaign_id=selected_camp_id,
            brand_rule_id=selected_rule_id,
            progress_callback=on_progress
        )
        total_time = round(time.time() - t0, 1)
        conn.close()

        st.balloons()
        st.success(f"🎉 PIPELINE ĐÃ HOÀN THÀNH XUẤT SẮC TRONG {total_time} GIÂY!")

        # Metric summary
        m1, m2, m3 = st.columns(3)
        with m1:
            render_kpi_card("Bài viết đã tạo", str(pipeline_output["total_posts"]), "✅ Đã lưu vào PostgreSQL", "📝", "cyan")
        with m2:
            render_kpi_card("Điểm Tuân thủ", f"{pipeline_output['overall_score']}/100", "🛡️ Compliance Score", "🏆", "emerald")
        with m3:
            render_kpi_card("Thời gian xử lý", f"{total_time}s", "⚡ 3 Agents Pipeline", "⏱️", "indigo")

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Tab views
        t_res1, t_res2, t_res3, t_res4 = st.tabs([
            "💡 Market Insights (Agent 1)",
            "✍️ Kịch bản Bài đăng (Agent 2)",
            "🛡️ Báo cáo Kiểm duyệt (Agent 3)",
            "📜 Toàn bộ Logs"
        ])

        with t_res1:
            st.json(pipeline_output["insights"])

        with t_res2:
            st.json(pipeline_output["posts"])

        with t_res3:
            st.json(pipeline_output["audit_report"])

        with t_res4:
            st.text_area("Agent Execution Logs", value="\n".join(pipeline_output["logs"]), height=250)

    except Exception as err:
        st.error(f"❌ Xảy ra lỗi khi chạy pipeline: {err}")
