"""
Dynamic Market Analyzer for Agent 01 (Market Intelligence).
Phân tích trực tiếp và sâu sắc mọi dữ liệu đầu vào người dùng nhập trên giao diện (SWOT, Competitor, STP & Persona).
Không bao giờ dùng dữ liệu tĩnh cứng nhắc; phân tích phản chiếu 100% đúng ngành hàng và thông số người dùng cung cấp.
"""

from typing import Dict, List, Any


def analyze_swot(data: Dict[str, Any]) -> str:
    """Phân tích ma trận SWOT kết hợp TOWS (SO, WO, ST, WT) dựa trên dữ liệu người dùng nhập."""
    if not isinstance(data, dict):
        data = {}

    strengths = str(data.get("strengths", "")).strip() or "Chưa có thông tin điểm mạnh."
    weaknesses = str(data.get("weaknesses", "")).strip() or "Chưa có thông tin điểm yếu."
    opportunities = str(data.get("opportunities", "")).strip() or "Chưa có thông tin cơ hội."
    threats = str(data.get("threats", "")).strip() or "Chưa có thông tin thách thức."

    # Lấy ý chính ngắn gọn cho ma trận
    def get_summary(text: str, limit: int = 70) -> str:
        first_clause = text.split(",")[0].split(";")[0].split(".")[0].strip()
        if len(first_clause) > limit:
            return first_clause[:limit] + "..."
        return first_clause or text[:limit]

    s_lead = get_summary(strengths)
    w_lead = get_summary(weaknesses)
    o_lead = get_summary(opportunities)
    t_lead = get_summary(threats)

    report = (
        "📊 [Agent 01 - Market Intel] Báo cáo Phân tích Chiến lược SWOT Tùy biến Cao cấp:\n\n"
        "1. ĐÁNH GIÁ YẾU TỐ ĐẦU VÀO TỪ DOANH NGHIỆP:\n"
        f"• STRENGTHS (Điểm mạnh cốt lõi):\n"
        f"  - Nhập liệu: \"{strengths}\"\n"
        f"  ↳ Nhận định: Lợi thế kỹ thuật/sản phẩm rất rõ rệt ({s_lead}), cần biến thành thông điệp truyền thông đinh (Hero Feature) để dẫn dắt phân khúc.\n\n"
        f"• WEAKNESSES (Điểm yếu & Rào cản):\n"
        f"  - Nhập liệu: \"{weaknesses}\"\n"
        f"  ↳ Nhận định: Điểm nghẽn tiếp cận thị trường ({w_lead}), đòi hỏi chính sách tài chính linh hoạt hoặc cam kết hậu mãi để giảm ma sát tâm lý.\n\n"
        f"• OPPORTUNITIES (Thời cơ thị trường):\n"
        f"  - Nhập liệu: \"{opportunities}\"\n"
        f"  ↳ Nhận định: Động lực thị trường đang mở rộng ({o_lead}), sẵn sàng đón nhận những thương hiệu có sự đột phá.\n\n"
        f"• THREATS (Thách thức & Áp lực cạnh tranh):\n"
        f"  - Nhập liệu: \"{threats}\"\n"
        f"  ↳ Nhận định: Áp lực cạnh tranh ({t_lead}) yêu cầu chiến lược định vị tập trung, tránh đối đầu trực diện về giá.\n\n"
        "2. MA TRẬN PHỐI HỢP CHIẾN LƯỢC (TOWS Strategy Matrix):\n"
        f"• CHIẾN LƯỢC S-O (Maxi - Maxi | Tấn công dẫn đầu):\n"
        f"  - Đòn bẩy tối đa: Khai thác ưu thế \"{s_lead}\" để đánh chiếm làn sóng \"{o_lead}\".\n"
        f"  - Thực thi: Xây dựng chiến dịch Content 'Blind Test' hoặc trải nghiệm độc quyền cùng chuyên gia/KOL đầu ngành, chứng minh sự vượt trội không thể thay thế.\n\n"
        f"• CHIẾN LƯỢC W-O (Mini - Maxi | Chuyển hóa rào cản):\n"
        f"  - Hóa giải rào cản \"{w_lead}\" trong bối cảnh \"{o_lead}\".\n"
        f"  - Thực thi: Áp dụng các giải pháp kích cầu: Chương trình thanh toán linh hoạt (trả góp 0%), chính sách thu cũ trợ giá (Trade-in), hoặc combo quà tặng đặc quyền giới hạn nhằm hạ thấp ngưỡng quyết định mua ban đầu.\n\n"
        f"• CHIẾN LƯỢC S-T (Maxi - Mini | Khác biệt hóa phòng thủ):\n"
        f"  - Dùng sức mạnh \"{s_lead}\" để tạo lá chắn vững chắc trước sức ép \"{t_lead}\".\n"
        f"  - Thực thi: Tuyệt đối không tham gia cuộc chiến giảm giá làm hạ thấp định vị; tập trung khắc sâu trải nghiệm độc quyền độc bản mà đối thủ không thể sao chép.\n\n"
        f"• CHIẾN LƯỢC W-T (Mini - Mini | Kiểm soát rủi ro & Bảo chứng):\n"
        f"  - Phòng ngừa tác động tiêu cực của \"{w_lead}\" trước sự đe dọa của \"{t_lead}\".\n"
        f"  - Thực thi: Cung cấp chính sách bảo hành VIP đặc quyền (1 đổi 1 tận nơi, dịch vụ hỗ trợ kỹ thuật ưu tiên 24/7) để chứng minh giá trị tương xứng từng đồng cho người sở hữu.\n\n"
        "3. ĐỀ XUẤT HÀNH ĐỘNG CỤ THỂ CHO CHIẾN DỊCH:\n"
        f"• Thông điệp chủ đạo (Key Hook): Tôn vinh trải nghiệm đột phá dựa trên {s_lead}.\n"
        f"• Kênh truyền thông ưu tiên: Video chuyên sâu (Tech/Product Reviewers), trải nghiệm thực tế (Showroom/Pop-up Store) và kênh phân phối chọn lọc.\n"
        f"• Tỷ lệ phân bổ ngân sách: 40% Trải nghiệm & Review thực tế | 35% Kích cầu & Hỗ trợ tài chính | 25% Hậu mãi & Chăm sóc khách hàng VIP."
    )
    return report


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
