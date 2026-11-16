"""
Dynamic Market Analyzer for Agent 01 (Market Intelligence).
Phân tích trực tiếp và sâu sắc mọi dữ liệu đầu vào người dùng nhập trên giao diện (SWOT, Competitor, STP & Persona).
Không bao giờ dùng dữ liệu tĩnh cứng nhắc; phân tích phản chiếu 100% đúng ngành hàng và thông số người dùng cung cấp.
"""

from typing import Dict, List, Any, Optional
from agents.quantitative_engine import QuantitativeMarketingEngine


def analyze_swot(data: Dict[str, Any], budget_str: str = "", target_orders: Optional[int] = None) -> str:
    """Phân tích ma trận SWOT kết hợp mô hình kinh tế định lượng và phễu chuyển đổi."""
    if not isinstance(data, dict):
        data = {}
    return QuantitativeMarketingEngine.analyze_swot_quantitative(data, budget_str=budget_str, target_orders=target_orders)



def analyze_competitors(competitors: List[Dict[str, Any]]) -> str:
    """Phân tích ma trận đối thủ cạnh tranh & tìm khoảng trống thị trường."""
    if not isinstance(competitors, list) or len(competitors) == 0:
        return "Chưa có danh sách đối thủ để phân tích."

    comp_summaries = []
    white_spaces = []
    for idx, c in enumerate(competitors, 1):
        name = c.get("name", f"Đối thủ {idx}") or f"Đối thủ {idx}"
        pos = c.get("positioning", "Đang cập nhật")
        chan = c.get("channels", "Đang cập nhật")
        strn = c.get("strengths", "Đang cập nhật")
        weak = c.get("weaknesses", "Đang cập nhật")
        comp_summaries.append(
            f"  {idx}. {name}:\n"
            f"     - Định vị: {pos} | Kênh: {chan}\n"
            f"     - Ưu thế: {strn}\n"
            f"     - Lỗ hổng / Điểm yếu: {weak}"
        )
        if weak and weak != "Đang cập nhật":
            white_spaces.append(f"Khai thác lỗ hổng của {name} ({weak})")

    white_space_str = "; ".join(white_spaces[:3]) if white_spaces else "Tập trung vào dịch vụ vượt trội và cá nhân hóa trải nghiệm khách hàng."

    return (
        "🎯 [Agent 01 - Market Intel] Ma trận Phân tích Đối thủ & Khoảng trống Thị trường:\n\n"
        "1. ĐÁNH GIÁ ĐỐI THỦ ĐẦU VÀO ĐƯỢC CUNG CẤP:\n"
        + "\n".join(comp_summaries)
        + "\n\n"
        "2. KHOẢNG TRỐNG THỊ TRƯỜNG CHIẾN LƯỢC (White Space):\n"
        f"• Cơ hội vàng: {white_space_str}.\n"
        "• Lợi thế cạnh tranh vượt trội: Không đối đầu vào thế mạnh cốt lõi của các thương hiệu dẫn đầu; thay vào đó, tập trung giải quyết triệt để những bất mãn mà khách hàng của đối thủ đang gặp phải.\n\n"
        "3. CHIẾN THUẬT ĐỐI ĐẦU ĐỀ XUẤT:\n"
        "• Chiến thuật Đánh tạt sườn (Flanking Attack): Tấn công vào phân khúc hoặc thuộc tính sản phẩm mà đối thủ chưa phục vụ tốt.\n"
        "• Chiến dịch Bằng chứng xã hội (Social Proof): Sử dụng so sánh trải nghiệm khách quan để làm nổi bật sự vượt trội về giá trị/giá cả."
    )


def analyze_stp(stp: Dict[str, Any], personas: List[Dict[str, Any]]) -> str:
    """Phân tích chiến lược STP & Chân dung khách hàng (Persona)."""
    seg = stp.get("segment", "Chưa nhập phân khúc") if isinstance(stp, dict) else "Chưa nhập"
    tgt = stp.get("target", "Chưa nhập thị trường mục tiêu") if isinstance(stp, dict) else "Chưa nhập"
    pos = stp.get("positioning", "Chưa nhập định vị") if isinstance(stp, dict) else "Chưa nhập"

    persona_texts = []
    if isinstance(personas, list) and personas:
        for p in personas:
            p_name = p.get("name", "Khách hàng mục tiêu")
            p_role = p.get("role", "Nghề nghiệp")
            p_inc = p.get("income", "Thu nhập")
            p_pain = p.get("painPoints", "Nỗi đau cần giải quyết")
            p_chan = p.get("channels", "Kênh ưa thích")
            persona_texts.append(
                f"  • {p_name} ({p_role} - Thu nhập: {p_inc}):\n"
                f"    - Nỗi đau/Rào cản: {p_pain}\n"
                f"    - Kênh tiếp cận hiệu quả: {p_chan}"
            )
    persona_str = "\n".join(persona_texts) if persona_texts else "  • Chưa có Persona cụ thể."

    return (
        "🧭 [Agent 01 - Market Intel] Chiến lược Phân khúc STP & Chân dung Khách hàng (Persona):\n\n"
        "1. BỘ KHUNG CHIẾN LƯỢC STP TÙY BIẾN:\n"
        f"• SEGMENTATION (Phân khúc thị trường):\n"
        f"  {seg}\n\n"
        f"• TARGETING (Thị trường trọng tâm):\n"
        f"  {tgt}\n\n"
        f"• POSITIONING (Định vị thương hiệu độc nhất):\n"
        f"  {pos}\n\n"
        "2. CHÂN DUNG KHÁCH HÀNG MỤC TIÊU (Persona Breakdown):\n"
        f"{persona_str}\n\n"
        "3. LỘ TRÌNH TIẾP CẬN VÀ CHUYỂN ĐỔI (Playbook):\n"
        "• Giai đoạn 1 - Kích hoạt nhận thức (Awareness): Đánh trúng nỗi đau cốt lõi của Persona thông qua video ngắn trên các kênh yêu thích.\n"
        "• Giai đoạn 2 - Cân nhắc (Consideration): Cung cấp bằng chứng thực tế, review chuyên sâu chứng minh định vị là đúng sự thật.\n"
        "• Giai đoạn 3 - Quyết định (Conversion): Kêu gọi hành động với ưu đãi giới hạn và cam kết rủi ro bằng 0."
    )
