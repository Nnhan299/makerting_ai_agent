"""
Component mô phỏng bài đăng mạng xã hội (Social Media Post Mockups).
Hỗ trợ 2 chế độ hiển thị cao cấp:
1. Mobile Phone Mockup (Khung điện thoại thông minh chân thực)
2. Desktop Social Feed Card (Bảng tin mạng xã hội chuẩn Facebook/LinkedIn)
"""

import streamlit as st
import html

STAGE_CONFIGS = {
    "Teaser": {
        "color": "#8B5CF6",
        "badge_text": "GIAI ĐOẠN 1 • TEASER (TÒ MÒ)",
        "icon": "🔮",
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=900&auto=format&fit=crop&q=80",
        "overlay_badge": "SẮP RA MẮT • COMING SOON",
        "tagline": "Một bí mật chăm sóc da đột phá sắp được hé lộ..."
    },
    "Launch": {
        "color": "#3B82F6",
        "badge_text": "GIAI ĐOẠN 2 • LAUNCH (GIẢI PHÁP)",
        "icon": "🚀",
        "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=900&auto=format&fit=crop&q=80",
        "overlay_badge": "CHÍNH THỨC RA MẮT • NEW ARRIVAL",
        "tagline": "Giải pháp làm sạch sâu thế hệ mới từ chuyên gia"
    },
    "CTA": {
        "color": "#10B981",
        "badge_text": "GIAI ĐOẠN 3 • CTA (ƯU ĐÃI ĐẶC BIỆT)",
        "icon": "⚡",
        "image_url": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=900&auto=format&fit=crop&q=80",
        "overlay_badge": "ƯU ĐÃI ĐỘC QUYỀN • LIMITED OFFER",
        "tagline": "Mua 1 tặng 1 + Freeship cho 100 đơn hàng đầu tiên"
    }
}


def _format_content_with_hashtags(content: str) -> str:
    """Format nội dung bài viết và highlight các hashtag."""
    escaped = html.escape(content or "")
    lines = escaped.split("\n")
    formatted_lines = []
    
    for line in lines:
        words = line.split(" ")
        formatted_words = []
        for word in words:
            if word.startswith("#") and len(word) > 1:
                formatted_words.append(f'<span style="color: #38BDF8; font-weight: 600;">{word}</span>')
            else:
                formatted_words.append(word)
        formatted_lines.append(" ".join(formatted_words))
        
    return "<br>".join(formatted_lines)


def _render_clean_html(raw_html: str):
    """
    Loại bỏ khoảng trắng thụt lề đầu dòng để Markdown không hiểu nhầm là khối code (<pre><code>).
    Dùng st.html() để xuất HTML nguyên bản không bị lỗi Markdown.
    """
    clean_lines = [line.strip() for line in raw_html.strip().splitlines() if line.strip()]
    cleaned = "".join(clean_lines)
    if hasattr(st, "html"):
        st.html(cleaned)
    else:
        st.markdown(cleaned, unsafe_allow_html=True)


def render_social_mockup(
    post: dict,
    brand_name: str = "XYZ Cosmetics",
    platform: str = "Facebook",
    compliance_score: float = None,
    violations: list = None
):
    """
    Render giao diện bài đăng xã hội chuẩn Desktop Feed.
    """
    channel = (post.get("channel") or platform).strip()
    stage = (post.get("stage") or "Launch").strip()
    title = post.get("title") or "Bài viết chiến dịch"
    content = post.get("content") or ""
    scheduled_date = post.get("scheduled_date") or "2026-11-10"
    stage_info = STAGE_CONFIGS.get(stage, STAGE_CONFIGS["Launch"])
    img_src = post.get("media_url") or stage_info["image_url"]
    formatted_body = _format_content_with_hashtags(content)
    
    likes = 428 if stage == "CTA" else (295 if stage == "Launch" else 184)
    comments = 52 if stage == "CTA" else (34 if stage == "Launch" else 19)
    shares = 18 if stage == "CTA" else (12 if stage == "Launch" else 7)
    
    mockup_html = f"""
<div style="background: #111827; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5); margin-bottom: 24px; overflow: hidden; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
    <div style="padding: 14px 18px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.06); background: rgba(255, 255, 255, 0.02);">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #6366F1, #EC4899); display: flex; align-items: center; justify-content: center; font-size: 1.15rem; font-weight: 800; color: white;">
                {html.escape(brand_name[:2].upper())}
            </div>
            <div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 0.96rem; font-weight: 700; color: #F9FAFB;">{html.escape(brand_name)}</span>
                    <span style="color: #38BDF8; font-size: 0.9rem;">✓</span>
                    <span style="font-size: 0.68rem; padding: 2px 8px; border-radius: 6px; background: rgba(99, 102, 241, 0.2); color: #A5B4FC; font-weight: 700;">{html.escape(channel.upper())}</span>
                </div>
                <div style="font-size: 0.75rem; color: #9CA3AF; margin-top: 2px;">
                    Được tài trợ • 🌐 Ngày đăng dự kiến: <strong>{scheduled_date}</strong>
                </div>
            </div>
        </div>
        <div style="background: {stage_info['color']}22; border: 1px solid {stage_info['color']}55; color: {stage_info['color']}; font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; display: flex; align-items: center; gap: 6px;">
            <span>{stage_info['icon']}</span>
            <span>{stage_info['badge_text']}</span>
        </div>
    </div>
    <div style="padding: 14px 18px 6px 18px; font-size: 1.05rem; font-weight: 700; color: #F3F4F6; line-height: 1.4;">
        {html.escape(title)}
    </div>
    <div style="padding: 6px 18px 14px 18px; font-size: 0.92rem; line-height: 1.65; color: #E5E7EB;">
        {formatted_body}
    </div>
    <div style="position: relative; width: 100%; background: #0F172A; overflow: hidden;">
        <img src="{img_src}" alt="Marketing Visual Mockup" loading="lazy" decoding="async" style="width: 100%; max-height: 360px; min-height: 180px; object-fit: cover; display: block; background: #1E293B;" onerror="this.style.display='none';" />
        <div style="position: absolute; bottom: 12px; left: 16px; right: 16px; background: rgba(15, 23, 42, 0.88); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 10px 14px; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <div style="font-size: 0.72rem; font-weight: 800; color: {stage_info['color']}; text-transform: uppercase;">{stage_info['overlay_badge']}</div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #FFFFFF; margin-top: 2px;">{stage_info['tagline']}</div>
            </div>
            <div style="background: {stage_info['color']}; color: #FFFFFF; font-size: 0.78rem; font-weight: 700; padding: 6px 14px; border-radius: 6px; white-space: nowrap;">
                { 'MUA NGAY' if stage == 'CTA' else ('TÌM HIỂU THÊM' if stage == 'Launch' else 'KHÁM PHÁ') }
            </div>
        </div>
    </div>
    <div style="padding: 10px 18px; display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #9CA3AF; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="background: #3B82F6; color: white; width: 20px; height: 20px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem;">👍</span>
            <span style="background: #EF4444; color: white; width: 20px; height: 20px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem;">❤️</span>
            <span style="font-weight: 600; color: #D1D5DB;">{likes} lượt thích</span>
        </div>
        <div>
            <span>{comments} bình luận</span> • <span>{shares} lượt chia sẻ</span>
        </div>
    </div>
    <div style="padding: 8px 16px; display: flex; justify-content: space-around; background: rgba(255, 255, 255, 0.02); font-size: 0.88rem; font-weight: 600; color: #9CA3AF;">
        <div>👍 Thích</div>
        <div>💬 Bình luận</div>
        <div>↗️ Chia sẻ</div>
    </div>
</div>
"""
    _render_clean_html(mockup_html)


def render_mobile_phone_mockup(
    post: dict,
    brand_name: str = "XYZ Cosmetics",
    platform: str = "Facebook"
):
    """
    Render giao diện xem trước bài viết mô phỏng trực tiếp trên MÀN HÌNH ĐIỆN THOẠI (Mobile Smartphone Mockup).
    Đem lại cảm giác chân thực 100% như đang lướt mạng xã hội trên di động trước khi bấm xuất bản.
    """
    stage = (post.get("stage") or "Launch").strip()
    title = post.get("title") or "Tiêu đề bài viết"
    content = post.get("content") or ""
    scheduled_date = post.get("scheduled_date") or "2026-11-10"
    stage_info = STAGE_CONFIGS.get(stage, STAGE_CONFIGS["Launch"])
    img_src = post.get("media_url") or stage_info["image_url"]
    formatted_body = _format_content_with_hashtags(content)
    
    phone_html = f"""
<div style="max-width: 380px; margin: 0 auto; background: #000000; border: 11px solid #1F2937; border-radius: 46px; box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.15); overflow: hidden; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
    <div style="background: #000; padding: 10px 16px 6px 16px; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.75rem; font-weight: 700; color: white;">9:41</span>
        <div style="width: 80px; height: 18px; background: #111; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);"></div>
        <span style="font-size: 0.72rem; color: white;">5G 🔋</span>
    </div>
    <div style="background: #18191A; padding: 10px 14px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #2F3031;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #2D88FF; font-weight: 900; font-size: 1.3rem;">facebook</span>
        </div>
        <div style="display: flex; gap: 10px; font-size: 0.95rem; color: #E4E6EB;">
            <span>🔍</span>
            <span>💬</span>
        </div>
    </div>
    <div style="background: #242526; max-height: 520px; overflow-y: auto;">
        <div style="padding: 10px 12px; display: flex; align-items: center; gap: 10px;">
            <div style="width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #6366F1, #EC4899); display: flex; align-items: center; justify-content: center; font-weight: 800; color: white; font-size: 0.95rem;">
                {html.escape(brand_name[:2].upper())}
            </div>
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 4px;">
                    <span style="font-size: 0.88rem; font-weight: 700; color: #E4E6EB;">{html.escape(brand_name)}</span>
                    <span style="color: #2D88FF; font-size: 0.8rem;">✓</span>
                </div>
                <div style="font-size: 0.7rem; color: #B0B3B8;">
                    Được tài trợ • 🌐 Ngày đăng: {scheduled_date}
                </div>
            </div>
            <span style="color: #B0B3B8; font-size: 1.1rem;">•••</span>
        </div>
        <div style="padding: 0 12px 6px 12px; font-size: 0.92rem; font-weight: 700; color: #E4E6EB;">
            {html.escape(title)}
        </div>
        <div style="padding: 0 12px 10px 12px; font-size: 0.84rem; line-height: 1.5; color: #E4E6EB;">
            {formatted_body}
        </div>
        <div style="position: relative; width: 100%; background: #18191A;">
            <img src="{img_src}" alt="Phone Preview" loading="lazy" decoding="async" style="width: 100%; max-height: 260px; object-fit: cover; display: block;" onerror="this.style.display='none';" />
            <div style="background: #3A3B3C; padding: 8px 12px; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.65rem; color: #B0B3B8; text-transform: uppercase;">XYZCOSMETICS.VN</div>
                    <div style="font-size: 0.78rem; font-weight: 700; color: #E4E6EB;">{stage_info['overlay_badge']}</div>
                </div>
                <div style="background: #4E4F50; color: white; font-size: 0.72rem; font-weight: 700; padding: 5px 12px; border-radius: 6px;">
                    { 'MUA NGAY' if stage == 'CTA' else 'TÌM HIỂU' }
                </div>
            </div>
        </div>
        <div style="padding: 8px 12px; display: flex; justify-content: space-between; font-size: 0.75rem; color: #B0B3B8; border-bottom: 1px solid #3A3B3C;">
            <div style="display: flex; align-items: center; gap: 4px;">
                <span>👍❤️</span>
                <span>328</span>
            </div>
            <div>42 bình luận • 15 lượt chia sẻ</div>
        </div>
        <div style="padding: 6px 12px; display: flex; justify-content: space-around; font-size: 0.8rem; font-weight: 600; color: #B0B3B8;">
            <div>👍 Thích</div>
            <div>💬 Bình luận</div>
            <div>↗️ Chia sẻ</div>
        </div>
    </div>
    <div style="background: #000; padding: 10px 0 8px 0; text-align: center;">
        <div style="width: 120px; height: 4px; background: #4B5563; border-radius: 2px; margin: 0 auto;"></div>
    </div>
</div>
"""
    _render_clean_html(phone_html)
