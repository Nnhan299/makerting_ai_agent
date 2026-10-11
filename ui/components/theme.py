"""
Theme & Design System cho Marketing AI Campaign Manager.
Áp dụng phong cách Dark Glassmorphism cao cấp, macOS typography và component helpers.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
/* ============================================================
   GOOGLE FONTS & BASE TYPOGRAPHY
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: #0B0F19 !important;
    color: #F1F5F9 !important;
}

/* Subtle ambient glow on background */
.stApp {
    background: 
        radial-gradient(circle at 12% 10%, rgba(99, 102, 241, 0.12) 0%, transparent 45%),
        radial-gradient(circle at 88% 85%, rgba(168, 85, 247, 0.10) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 60%),
        #0B0F19 !important;
}

/* Hide Streamlit Web Chrome for pure Desktop App feel */
#MainMenu { visibility: hidden; display: none !important; }
footer { visibility: hidden; display: none !important; }
header[data-testid="stHeader"] {
    background: transparent !important;
    backdrop-filter: none !important;
}
.stDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}
[data-testid="stStatusWidget"] {
    visibility: hidden !important;
}

/* Modern Dark Scrollbars */
::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}
::-webkit-scrollbar-track {
    background: #0B0F19;
}
::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
    background: #334155;
}

/* ============================================================
   SIDEBAR STYLING
   ============================================================ */
[data-testid="stSidebar"] {
    background-color: #0E1322 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
}
[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
}
[data-testid="stSidebarNav"] {
    padding-top: 0.5rem;
}
[data-testid="stSidebarNav"] a {
    border-radius: 8px;
    margin-bottom: 2px;
    transition: all 0.2s ease;
}
[data-testid="stSidebarNav"] a:hover {
    background-color: rgba(99, 102, 241, 0.12) !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(168, 85, 247, 0.2)) !important;
    border-left: 3px solid #818CF8;
    color: #FFFFFF !important;
}

/* ============================================================
   HEADER GRADIENT & BADGES
   ============================================================ */
.hero-title {
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 45%, #818CF8 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 0.25rem !important;
}

.hero-subtitle {
    font-size: 0.92rem !important;
    color: #94A3B8 !important;
    font-weight: 400 !important;
    margin-bottom: 1.25rem !important;
    line-height: 1.5;
}

.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.73rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    background: rgba(99, 102, 241, 0.15);
    color: #818CF8;
    border: 1px solid rgba(99, 102, 241, 0.3);
    margin-bottom: 0.65rem;
}

.badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #818CF8;
    box-shadow: 0 0 8px #818CF8;
}

/* ============================================================
   GLASSMORPHIC KPI METRIC CARDS
   ============================================================ */
.glass-card {
    background: rgba(17, 24, 39, 0.72) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.25rem !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.35) !important;
    position: relative;
    overflow: hidden;
}

.glass-card:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(99, 102, 241, 0.45) !important;
    box-shadow: 0 12px 30px -4px rgba(99, 102, 241, 0.25) !important;
}

.glass-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}

.glass-card-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.glass-card-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}

.icon-indigo { background: rgba(99, 102, 241, 0.18); color: #818CF8; border: 1px solid rgba(99, 102, 241, 0.3); }
.icon-cyan   { background: rgba(6, 182, 212, 0.18); color: #38BDF8; border: 1px solid rgba(6, 182, 212, 0.3); }
.icon-emerald{ background: rgba(16, 185, 129, 0.18); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
.icon-amber  { background: rgba(245, 158, 11, 0.18); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
.icon-rose   { background: rgba(244, 63, 94, 0.18); color: #FB7185; border: 1px solid rgba(244, 63, 94, 0.3); }

.glass-card-value {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #F8FAFC;
    margin-bottom: 0.25rem;
    line-height: 1.15;
}

.glass-card-sub {
    font-size: 0.78rem;
    color: #64748B;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Hide default Streamlit metric container */
[data-testid="stMetric"] {
    display: none !important;
}

/* ============================================================
   STREAMLIT BUTTONS & CTAs
   ============================================================ */
button[kind="primary"], div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.4) !important;
    transition: all 0.2s ease-in-out !important;
}

button[kind="primary"]:hover, div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.55) !important;
    filter: brightness(1.08) !important;
}

button[kind="secondary"], div.stButton > button[kind="secondary"] {
    background: rgba(30, 41, 59, 0.7) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.2rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

button[kind="secondary"]:hover, div.stButton > button[kind="secondary"]:hover {
    background: rgba(51, 65, 85, 0.85) !important;
    border-color: rgba(99, 102, 241, 0.4) !important;
    color: #FFFFFF !important;
}

/* ============================================================
   FORM INPUTS & SELECTBOXES
   ============================================================ */
input, textarea, select {
    background-color: #131A2B !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    padding: 0.55rem 0.85rem !important;
    transition: all 0.2s ease !important;
}

input:focus, textarea:focus, select:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
    outline: none !important;
}

[data-baseweb="select"] > div {
    background-color: #131A2B !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
}

[data-baseweb="tag"] {
    background: rgba(99, 102, 241, 0.25) !important;
    color: #C7D2FE !important;
    border: 1px solid rgba(99, 102, 241, 0.4) !important;
    border-radius: 6px !important;
}

/* ============================================================
   TABS STYLING
   ============================================================ */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background-color: rgba(17, 24, 39, 0.7) !important;
    padding: 6px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 8px 16px !important;
    color: #94A3B8 !important;
    font-weight: 600 !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(99, 102, 241, 0.45) !important;
}

/* ============================================================
   EXPANDERS & ACCORDIONS
   ============================================================ */
[data-testid="stExpander"] {
    background: rgba(17, 24, 39, 0.55) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    margin-bottom: 0.75rem !important;
    box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.25) !important;
    overflow: hidden !important;
    transition: all 0.2s ease !important;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(99, 102, 241, 0.35) !important;
}

[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #F1F5F9 !important;
    padding: 0.85rem 1.1rem !important;
}

/* ============================================================
   DATAFRAME / TABLE STYLING
   ============================================================ */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ============================================================
   STATUS PILL CHIPS
   ============================================================ */
.chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}

.chip-draft { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
.chip-inprogress { background: rgba(6, 182, 212, 0.15); color: #38BDF8; border: 1px solid rgba(6, 182, 212, 0.3); }
.chip-approved { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
.chip-completed { background: rgba(148, 163, 184, 0.15); color: #94A3B8; border: 1px solid rgba(148, 163, 184, 0.3); }
.chip-rejected { background: rgba(244, 63, 94, 0.15); color: #FB7185; border: 1px solid rgba(244, 63, 94, 0.3); }

.chip-teaser { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
.chip-launch { background: rgba(99, 102, 241, 0.15); color: #818CF8; border: 1px solid rgba(99, 102, 241, 0.3); }
.chip-cta { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }

.chip-facebook { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }
.chip-linkedin { background: rgba(14, 165, 233, 0.15); color: #38BDF8; border: 1px solid rgba(14, 165, 233, 0.3); }
.chip-email { background: rgba(236, 72, 153, 0.15); color: #F472B6; border: 1px solid rgba(236, 72, 153, 0.3); }

/* ============================================================
   STEPPER TIMELINE FOR PIPELINE
   ============================================================ */
.step-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.25rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 1;
}

.step-num {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.9rem;
}

.step-num-active {
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    color: #FFFFFF;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.6);
}

.step-num-done {
    background: #10B981;
    color: #FFFFFF;
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.5);
}

.step-num-pending {
    background: #1E293B;
    color: #64748B;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.step-info-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #F8FAFC;
}

.step-info-desc {
    font-size: 0.75rem;
    color: #94A3B8;
}

/* Subtle Divider */
hr {
    border-color: rgba(255, 255, 255, 0.08) !important;
    margin: 1.5rem 0 !important;
}
</style>
"""


def apply_custom_theme():
    """Áp dụng bộ CSS Dark Glassmorphism tùy chỉnh và tối ưu hiển thị Desktop App."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "", badge: str = ""):
    """Render tiêu đề trang sang trọng với badge gradient và subtitle."""
    badge_html = f'<div class="badge-pill"><span class="badge-dot"></span>{badge}</div>' if badge else ""
    st.markdown(
        f"""
        <div style="margin-bottom: 1.25rem;">
            {badge_html}
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_kpi_card(label: str, value: str, subtext: str = "", icon: str = "📈", theme: str = "indigo"):
    """Render thẻ KPI card kiểu Dark Glassmorphism."""
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="glass-card-top">
                <span class="glass-card-label">{label}</span>
                <div class="glass-card-icon icon-{theme}">{icon}</div>
            </div>
            <div class="glass-card-value">{value}</div>
            <div class="glass-card-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_status_chip(status: str) -> str:
    """Trả về HTML status chip với badge màu."""
    st_val = (status or "Draft").lower()
    if "progress" in st_val:
        return '<span class="chip chip-inprogress">🔄 In-Progress</span>'
    elif "approved" in st_val:
        return '<span class="chip chip-approved">✅ Approved</span>'
    elif "completed" in st_val:
        return '<span class="chip chip-completed">🏁 Completed</span>'
    elif "rejected" in st_val:
        return '<span class="chip chip-rejected">❌ Rejected</span>'
    return f'<span class="chip chip-draft">🟡 {status or "Draft"}</span>'


def get_channel_chip(channel: str) -> str:
    """Trả về HTML chip đại diện cho từng kênh Social Media."""
    ch = (channel or "").lower()
    if "facebook" in ch:
        return '<span class="chip chip-facebook">📘 Facebook</span>'
    elif "linkedin" in ch:
        return '<span class="chip chip-linkedin">💼 LinkedIn</span>'
    elif "email" in ch:
        return '<span class="chip chip-email">✉️ Email</span>'
    return f'<span class="chip chip-completed">🌐 {channel}</span>'


def get_stage_chip(stage: str) -> str:
    """Trả về HTML chip phân loại giai đoạn phễu Marketing."""
    stg = (stage or "Teaser").lower()
    if "launch" in stg:
        return f'<span class="chip chip-launch">🚀 {stage}</span>'
    elif "cta" in stg:
        return f'<span class="chip chip-cta">🎯 {stage}</span>'
    return f'<span class="chip chip-teaser">💡 {stage}</span>'
