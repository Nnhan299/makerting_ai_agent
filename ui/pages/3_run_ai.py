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

from database.connection import get_connection, get_db_type
from database.crud import (
    get_all_campaigns,
    get_all_brand_rules,
    get_campaign_by_id,
    get_brand_rule_by_id
)
from utils.llm_client import LLMClient
from agents.orchestrator import AgentOrchestrator
from ui.components.auth import require_auth
from ui.components.sidebar import render_sidebar
from ui.components.navbar import render_dynamic_dock
from ui.components.post_mockup import render_social_mockup, _render_clean_html
from ui.components.visual_agent_cards import (
    render_agent1_insights_view,
    render_agent3_audit_view
)
from ui.components.theme import (
    apply_custom_theme,
    render_page_header,
    render_kpi_card,
    get_status_chip
)

st.set_page_config(page_title="Chạy AI Pipeline - Marketing AI", page_icon="🤖", layout="wide")
apply_custom_theme()
require_auth()
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

# 2. PREVIEW BRIEF & RULE DẠNG THẺ THÔNG TIN
col_card1, col_card2 = st.columns(2, gap="medium")

with col_card1:
    with st.container(border=True):
        st.caption("📄 CHIẾN DỊCH (CAMPAIGN BRIEF)")
        st.markdown(f"### {selected_camp['name']}")
        st.markdown(f"**Sản phẩm:** {selected_camp['product_name']}")
        st.caption(f"🎯 Đối tượng: {selected_camp.get('target_audience') or 'Chưa nhập'}")

with col_card2:
    with st.container(border=True):
        st.caption("🛡️ BỘ QUY TẮC THƯƠNG HIỆU (BRAND GUIDELINES)")
        st.markdown(f"### {selected_rule['rule_name']}")
        st.markdown(f"**Tone of Voice:** `{selected_rule['tone_of_voice']}`")
        st.caption(f"🚫 Từ cấm kiểm duyệt: {selected_rule.get('forbidden_words') or 'Không có'}")

# 2B. NÚT XEM TRƯỚC BÀI VIẾT NẾU ĐÃ CÓ BÀI
try:
    from database.crud import get_posts_by_campaign
    c_check = get_connection()
    c_posts = get_posts_by_campaign(c_check, selected_camp_id)
    c_check.close()
    if c_posts:
        st.info(f"👁️ **Chiến dịch này đã có {len(c_posts)} bài viết sẵn sàng!** Bạn có thể bấm nút bên dưới để xem trước trên giao diện Điện thoại/Mạng xã hội hoặc chạy lại AI Pipeline bên dưới.")
        st.page_link("pages/4_calendar.py", label="👉 Đi tới mục Xem trước & Duyệt bài (Social Preview)", icon=":material/visibility:")
except Exception:
    pass

# 3. PIPELINE STEPPER DIAGRAM (Tác tử đa luồng)
stepper_html = '''
<div style="background: #ffffff; border: 1px solid #d8d1c8; border-radius: 14px; padding: 18px 24px; margin: 16px 0 24px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
    <div style="display: flex; align-items: center; justify-content: space-between; gap: 14px; flex-wrap: wrap;">
        <!-- Step 1 -->
        <div style="display: flex; align-items: center; gap: 12px; flex: 1; min-width: 210px;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #6366F1, #8B5CF6); color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.05rem; box-shadow: 0 4px 10px rgba(99, 102, 241, 0.35); flex-shrink: 0;">1</div>
            <div>
                <div style="font-size: 0.92rem; font-weight: 700; color: #1e293b;">Agent 1: Market Intelligence</div>
                <div style="font-size: 0.8rem; color: #64748b; margin-top: 2px;">Phân tích Persona, Pain Points, USP</div>
            </div>
        </div>
        
        <!-- Connector 1 -->
        <div style="color: #94a3b8; font-size: 1.3rem; font-weight: bold; flex-shrink: 0; padding: 0 4px;">➔</div>
        
        <!-- Step 2 -->
        <div style="display: flex; align-items: center; gap: 12px; flex: 1; min-width: 210px;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #06B6D4); color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.05rem; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.35); flex-shrink: 0;">2</div>
            <div>
                <div style="font-size: 0.92rem; font-weight: 700; color: #1e293b;">Agent 2: Copywriter</div>
                <div style="font-size: 0.8rem; color: #64748b; margin-top: 2px;">Sinh 20-30 bài theo phễu 3 giai đoạn</div>
            </div>
        </div>
        
        <!-- Connector 2 -->
        <div style="color: #94a3b8; font-size: 1.3rem; font-weight: bold; flex-shrink: 0; padding: 0 4px;">➔</div>
        
        <!-- Step 3 -->
        <div style="display: flex; align-items: center; gap: 12px; flex: 1; min-width: 210px;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #10B981, #059669); color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.05rem; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.35); flex-shrink: 0;">3</div>
            <div>
                <div style="font-size: 0.92rem; font-weight: 700; color: #1e293b;">Agent 3: Brand Auditor</div>
                <div style="font-size: 0.8rem; color: #64748b; margin-top: 2px;">Kiểm duyệt từ cấm & chấm điểm</div>
            </div>
        </div>
    </div>
</div>
'''
_render_clean_html(stepper_html)

# KÍCH HOẠT PIPELINE (API Key được cấu hình bảo mật trong hệ thống)
# 5. KÍCH HOẠT PIPELINE
btn_trigger = st.button("🚀 Kích hoạt AI multi-agent pipeline", type="primary", width="stretch")

if btn_trigger:
    st.markdown("### 🔄 Trạng thái Xử lý Trực tiếp")
    prog_bar = st.progress(0)
    status_box = st.empty()
    log_expander = st.expander("📜 Chi tiết Agent Logs (Thời gian thực)", expanded=True)
    live_log_container = log_expander.empty()
    live_logs = []

    def on_progress(step: int, total: int, msg: str):
        pct = int((step / total) * 100)
        prog_bar.progress(pct)
        status_box.markdown(f"**Bước {step}/{total}:** {msg}")
        live_logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        live_log_container.text_area("Live Logs", value="\n".join(live_logs), height=200, disabled=True)

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
        db_label = "PostgreSQL" if get_db_type(conn) == "postgres" else "SQLite"
        conn.close()

        st.balloons()
        st.success(f"🎉 PIPELINE ĐÃ HOÀN THÀNH XUẤT SẮC TRONG {total_time} GIÂY!")

        # Metric summary
        m1, m2, m3 = st.columns(3)
        with m1:
            render_kpi_card("Bài viết đã tạo", str(pipeline_output["total_posts"]), f"✅ Đã lưu vào {db_label}", "📝", "cyan")
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
            render_agent1_insights_view(pipeline_output.get("insights", {}))

        with t_res2:
            raw_posts = pipeline_output.get("posts", [])
            strat = pipeline_output.get("content_strategy_summary", "")
            
            if isinstance(raw_posts, dict):
                posts_generated = raw_posts.get("posts", [])
                if not strat:
                    strat = raw_posts.get("content_strategy_summary", "")
            elif isinstance(raw_posts, list):
                posts_generated = raw_posts
            else:
                posts_generated = []

            # Chuẩn hóa bảo đảm từng bài viết là dict hợp lệ
            clean_posts = []
            for p in posts_generated:
                if isinstance(p, dict):
                    clean_posts.append(p)
                elif isinstance(p, str):
                    clean_posts.append({
                        "stage": "Launch",
                        "channel": "Facebook",
                        "title": p[:50],
                        "content": p,
                        "hashtags": []
                    })
            posts_generated = clean_posts

            if strat:
                st.info(f"🎯 **Chiến lược kịch bản Agent 2:** {strat}")
            
            if not posts_generated:
                st.info("Chưa có bài viết nào được tạo.")
            else:
                st.markdown(f"##### 📱 Mô phỏng bài đăng mạng xã hội ({len(posts_generated)} bài viết)")
                
                # Tab filter by stage
                stg_tab1, stg_tab2, stg_tab3, stg_tab4 = st.tabs(["Tất cả bài viết", "🔮 Teaser (Nhận thức)", "🚀 Launch (Giải pháp)", "⚡ CTA (Chốt sale)"])
                
                def show_mockups(filtered):
                    for p in filtered:
                        if isinstance(p, dict):
                            render_social_mockup(p, brand_name=selected_camp['name'])

                with stg_tab1:
                    show_mockups(posts_generated)
                with stg_tab2:
                    show_mockups([p for p in posts_generated if isinstance(p, dict) and p.get('stage') == 'Teaser'])
                with stg_tab3:
                    show_mockups([p for p in posts_generated if isinstance(p, dict) and p.get('stage') == 'Launch'])
                with stg_tab4:
                    show_mockups([p for p in posts_generated if isinstance(p, dict) and p.get('stage') == 'CTA'])

        with t_res3:
            render_agent3_audit_view(pipeline_output.get("audit_report", {}))

        with t_res4:
            st.text_area("Agent Execution Logs", value="\n".join(pipeline_output.get("logs", [])), height=250)

    except Exception as err:
        st.error(f"❌ Xảy ra lỗi khi chạy pipeline: {err}")
