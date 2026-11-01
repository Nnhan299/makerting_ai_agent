"""
Component hiển thị trực quan kết quả phân tích của 3 AI Agent.
Loại bỏ hoàn toàn các khối JSON raw và text-wall nhàm chán.
Hoàn toàn tương thích và đẹp mắt với giao diện ứng dụng.
"""

import streamlit as st
import html

def _render_clean_html(raw_html: str):
    """Render HTML an toàn, không bị markdown thụt lề ép thành code block."""
    clean_lines = [line.strip() for line in raw_html.strip().splitlines() if line.strip()]
    cleaned = "".join(clean_lines)
    if hasattr(st, "html"):
        st.html(cleaned)
    else:
        st.markdown(cleaned, unsafe_allow_html=True)


def render_agent1_insights_view(insights: dict):
    """
    Render kết quả phân tích thị trường của Agent 1 thành các Card đồ họa chuyên nghiệp.
    """
    if not isinstance(insights, dict):
        st.info("Chưa có dữ liệu phân tích thị trường hợp lệ.")
        return

    persona = insights.get("target_persona", {})
    if isinstance(persona, str):
        persona = {"age_range": "Đa dạng", "gender": "Tất cả", "income_level": "Trung bình - Khá", "lifestyle": persona, "concerns": []}
    elif not isinstance(persona, dict):
        persona = {}

    pain_points = insights.get("pain_points", [])
    if not isinstance(pain_points, list):
        pain_points = [pain_points] if pain_points else []

    usp = insights.get("usp", "")
    angles = insights.get("communication_angles", [])
    if not isinstance(angles, list):
        angles = [angles] if angles else []

    market_summary = insights.get("market_summary", "")

    # 1. USP BANNER
    if usp:
        _render_clean_html(
            f"""
            <div style="
                background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                border: 1px solid #F59E0B;
                border-radius: 14px;
                padding: 16px 20px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 16px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                <div style="font-size: 2.2rem;">💎</div>
                <div>
                    <div style="font-size: 0.75rem; font-weight: 800; color: #B45309; text-transform: uppercase; letter-spacing: 0.08em;">
                        USP - Điểm bán hàng độc nhất (Unique Selling Proposition)
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #78350F; margin-top: 3px;">
                        {html.escape(str(usp))}
                    </div>
                </div>
            </div>
            """
        )

    col1, col2 = st.columns([1, 1], gap="medium")

    # 2. TARGET PERSONA CARD
    with col1:
        concerns = persona.get("concerns", [])
        concerns_html = ""
        if isinstance(concerns, list) and concerns:
            chips = "".join([f'<span style="background: rgba(239, 68, 68, 0.1); color: #DC2626; border: 1px solid rgba(239, 68, 68, 0.25); font-size: 0.75rem; padding: 3px 8px; border-radius: 6px;">⚠️ {html.escape(c)}</span>' for c in concerns])
            concerns_html = f'''
            <div style="font-size: 0.8rem; font-weight: 700; color: #475569; margin: 10px 0 6px 0;">Mối lo ngại chính (Concerns):</div>
            <div style="display: flex; flex-wrap: wrap; gap: 6px;">{chips}</div>
            '''

        persona_html = f"""
        <div style="background: #ffffff; border: 1px solid #d8d1c8; border-radius: 14px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); min-height: 250px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px;">
                <div style="background: #3B82F6; width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #fff;">👤</div>
                <div>
                    <div style="font-size: 0.92rem; font-weight: 800; color: #1E293B;">CHÂN DUNG KHÁCH HÀNG (PERSONA)</div>
                    <div style="font-size: 0.75rem; color: #64748B;">Hồ sơ nhân khẩu học & lối sống</div>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px;">
                <div style="background: #f8fafc; padding: 8px 10px; border-radius: 8px; border: 1px solid #f1f5f9;">
                    <span style="font-size: 0.72rem; color: #64748B;">Độ tuổi:</span>
                    <div style="font-weight: 700; color: #1E293B; font-size: 0.88rem;">{persona.get('age_range', 'N/A')}</div>
                </div>
                <div style="background: #f8fafc; padding: 8px 10px; border-radius: 8px; border: 1px solid #f1f5f9;">
                    <span style="font-size: 0.72rem; color: #64748B;">Giới tính:</span>
                    <div style="font-weight: 700; color: #1E293B; font-size: 0.88rem;">{persona.get('gender', 'N/A')}</div>
                </div>
                <div style="background: #f8fafc; padding: 8px 10px; border-radius: 8px; border: 1px solid #f1f5f9;">
                    <span style="font-size: 0.72rem; color: #64748B;">Thu nhập:</span>
                    <div style="font-weight: 700; color: #1E293B; font-size: 0.88rem;">{persona.get('income_level', 'N/A')}</div>
                </div>
                <div style="background: #f8fafc; padding: 8px 10px; border-radius: 8px; border: 1px solid #f1f5f9;">
                    <span style="font-size: 0.72rem; color: #64748B;">Lối sống:</span>
                    <div style="font-weight: 700; color: #1E293B; font-size: 0.88rem;">{persona.get('lifestyle', 'N/A')}</div>
                </div>
            </div>
            {concerns_html}
        </div>
        """
        _render_clean_html(persona_html)

    # 3. PAIN POINTS CARD
    with col2:
        pp_items = ""
        for i, pp in enumerate(pain_points[:5], 1):
            pp_items += f"""
            <div style="background: #fef2f2; border-left: 3px solid #EF4444; padding: 7px 10px; border-radius: 6px; margin-bottom: 6px; font-size: 0.82rem; color: #7f1d1d;">
                <span style="font-weight: 800; color: #DC2626; margin-right: 4px;">#{i}</span> {html.escape(str(pp))}
            </div>
            """
        pain_html = f"""
        <div style="background: #ffffff; border: 1px solid #d8d1c8; border-radius: 14px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); min-height: 250px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px;">
                <div style="background: #EF4444; width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #fff;">🎯</div>
                <div>
                    <div style="font-size: 0.92rem; font-weight: 800; color: #1E293B;">5 NỖI ĐAU THỰC TẾ (PAIN POINTS)</div>
                    <div style="font-size: 0.75rem; color: #64748B;">Vấn đề nhức nhối khách hàng cần giải quyết</div>
                </div>
            </div>
            {pp_items}
        </div>
        """
        _render_clean_html(pain_html)

    # 4. COMMUNICATION ANGLES
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("##### 💡 Các góc tiếp cận truyền thông (Communication Angles)")
    
    if angles and isinstance(angles, list):
        angle_cols = st.columns(len(angles)) if len(angles) <= 4 else st.columns(3)
        for idx, ang in enumerate(angles):
            if isinstance(ang, str):
                ang = {"angle_name": f"Góc #{idx+1}", "description": ang, "emotional_hook": "Tương tác"}
            elif not isinstance(ang, dict):
                continue
            col_target = angle_cols[idx % len(angle_cols)]
            with col_target:
                _render_clean_html(
                    f"""
                    <div style="
                        background: #ffffff;
                        border: 1px solid #d8d1c8;
                        border-radius: 12px;
                        padding: 14px;
                        margin-bottom: 12px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
                    ">
                        <div style="font-size: 0.72rem; font-weight: 800; color: #4F46E5; text-transform: uppercase;">GÓC TIẾP CẬN #{idx+1}</div>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #1E293B; margin: 4px 0 6px 0;">{html.escape(ang.get('angle_name', ''))}</div>
                        <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 8px; line-height: 1.4;">{html.escape(ang.get('description', ''))}</div>
                        <div style="
                            background: #EEF2FF;
                            border-radius: 6px;
                            padding: 6px 10px;
                            font-size: 0.78rem;
                            color: #3730A3;
                            border: 1px dashed #A5B4FC;
                        ">
                            ❤️ <strong>Điểm chạm:</strong> {html.escape(ang.get('emotional_hook', ''))}
                        </div>
                    </div>
                    """
                )

    # 5. MARKET SUMMARY
    if market_summary:
        st.info(f"📊 **Tóm tắt chiến lược thị trường:** {market_summary}")


def render_agent3_audit_view(audit_report: dict):
    """
    Render báo cáo kiểm duyệt thương hiệu của Agent 3 thành bảng chỉ số và thẻ vi phạm trực quan.
    """
    if not isinstance(audit_report, dict):
        st.info("Chưa có báo cáo kiểm duyệt hợp lệ.")
        return

    score = audit_report.get("overall_score", 100)
    total_violations = audit_report.get("total_violations", 0)
    summary = audit_report.get("summary", "Không có vi phạm nghiêm trọng.")
    audited_posts = audit_report.get("audited_posts", [])

    # Color code according to score
    if score >= 85:
        score_color = "#10B981"
        status_text = "ĐẠT CHUẨN XUẤT SẮC"
        badge_bg = "rgba(16, 185, 129, 0.15)"
    elif score >= 70:
        score_color = "#F59E0B"
        status_text = "CẦN CHỈNH SỬA NHẸ"
        badge_bg = "rgba(245, 158, 11, 0.15)"
    else:
        score_color = "#EF4444"
        status_text = "KHÔNG ĐẠT TIÊU CHUẨN"
        badge_bg = "rgba(239, 68, 68, 0.15)"

    # Top KPI Banner
    _render_clean_html(
        f"""
        <div style="
            background: #ffffff;
            border: 1px solid #d8d1c8;
            border-radius: 14px;
            padding: 18px 22px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        ">
            <div>
                <div style="font-size: 0.75rem; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em;">
                    KẾT QUẢ KIỂM DUYỆT THƯƠNG HIỆU & PHÁP LÝ (AGENT 3)
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #1E293B; margin-top: 4px;">
                    {html.escape(summary)}
                </div>
                <div style="margin-top: 8px;">
                    <span style="
                        background: {badge_bg}; color: {score_color}; 
                        font-weight: 800; font-size: 0.75rem; padding: 4px 10px; border-radius: 20px;
                        border: 1px solid {score_color}44;
                    ">
                        ● {status_text}
                    </span>
                    <span style="color: #64748B; font-size: 0.8rem; margin-left: 12px;">
                        Phát hiện: <strong style="color: {'#EF4444' if total_violations > 0 else '#10B981'};">{total_violations} lỗi vi phạm</strong>
                    </span>
                </div>
            </div>

            <!-- Score Circular Display -->
            <div style="
                width: 82px; height: 82px; border-radius: 50%;
                background: #ffffff;
                border: 4px solid {score_color};
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                box-shadow: 0 2px 10px {score_color}33;
                flex-shrink: 0;
            ">
                <div style="font-size: 1.5rem; font-weight: 900; color: {score_color}; line-height: 1;">
                    {int(score)}
                </div>
                <div style="font-size: 0.62rem; color: #64748B; font-weight: 700;">/ 100 ĐIỂM</div>
            </div>
        </div>
        """
    )

    # Detailed Violations List
    st.markdown("##### 📋 Chi tiết rà soát từng bài viết")
    
    if not audited_posts:
        st.success("✅ Toàn bộ bài viết hoàn toàn sạch, tuân thủ 100% Brand Guidelines và Luật Quảng cáo!")
        return

    for idx_item, item in enumerate(audited_posts):
        if isinstance(item, str):
            item = {"post_index": idx_item, "original_title": item, "compliance_score": 100, "violations": []}
        elif not isinstance(item, dict):
            continue
        p_idx = item.get("post_index", idx_item) + 1
        p_title = item.get("original_title", f"Bài viết #{p_idx}")
        p_score = item.get("compliance_score", 100)
        p_violations = item.get("violations", [])
        if not isinstance(p_violations, list):
            p_violations = [p_violations] if p_violations else []
        
        has_viol = len(p_violations) > 0
        status_icon = "⚠️" if has_viol else "✅"

        with st.expander(f"{status_icon} Bài #{p_idx}: {p_title} — Điểm: {p_score}/100", expanded=has_viol):
            if not p_violations:
                st.success("Bài viết này đạt chuẩn tuyệt đối, sẵn sàng xuất bản.")
            else:
                for v in p_violations:
                    if isinstance(v, str):
                        v = {"type": "Cảnh báo", "detail": v, "found_text": "", "suggestion": ""}
                    elif not isinstance(v, dict):
                        continue
                    v_type = v.get("type", "violation")
                    v_detail = v.get("detail", "")
                    v_found = v.get("found_text", "")
                    v_sugg = v.get("suggestion", "")

                    _render_clean_html(
                        f"""
                        <div style="
                            background: rgba(239, 68, 68, 0.05);
                            border: 1px solid rgba(239, 68, 68, 0.2);
                            border-radius: 10px;
                            padding: 12px 16px;
                            margin-bottom: 8px;
                        ">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                                <span style="
                                    background: #EF4444; color: white; font-weight: 800; font-size: 0.7rem; 
                                    padding: 2px 8px; border-radius: 4px; text-transform: uppercase;
                                ">
                                    {html.escape(v_type)}
                                </span>
                                <span style="font-size: 0.8rem; color: #DC2626;">
                                    Phát hiện cụm từ: <code style="color: #991B1B; background: #FEE2E2; padding: 2px 6px; border-radius: 4px;">{html.escape(v_found)}</code>
                                </span>
                            </div>
                            <div style="font-size: 0.85rem; color: #1E293B; margin-top: 6px;">
                                <strong>Vấn đề:</strong> {html.escape(v_detail)}
                            </div>
                            <div style="
                                font-size: 0.85rem; color: #065F46; margin-top: 6px; 
                                background: rgba(16, 185, 129, 0.1); padding: 6px 10px; border-radius: 6px;
                            ">
                                💡 <strong>Gợi ý sửa đổi:</strong> {html.escape(v_sugg)}
                            </div>
                        </div>
                        """
                    )
