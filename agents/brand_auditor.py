"""
Agent 3: Brand Compliance Auditor Agent.
Kiểm duyệt danh sách bài viết từ Agent 2 theo Bộ quy tắc thương hiệu (Brand Rules) từ DB.
"""

from typing import Dict, Any, Tuple
from agents.base_agent import BaseAgent
from utils.json_parser import validate_agent3_output


class BrandComplianceAuditorAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__(
            name="Brand Compliance Auditor Agent",
            llm_client=llm_client,
            system_prompt_path="prompts/agent3_system.txt"
        )

    def build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        posts = input_data.get("posts", [])
        brand_rules = input_data.get("brand_rules", {})

        posts_text = ""
        for idx, post in enumerate(posts):
            posts_text += f"\n--- BÀI {idx + 1} ---\n"
            posts_text += f"Giai đoạn: {post.get('stage')}\n"
            posts_text += f"Kênh: {post.get('channel')}\n"
            posts_text += f"Tiêu đề: {post.get('title')}\n"
            posts_text += f"Nội dung: {post.get('content')}\n"

        return (
            "Hãy kiểm duyệt danh sách bài viết sau theo Bộ quy tắc thương hiệu và Quy định Luật Quảng cáo:\n\n"
            "=== BỘ QUY TẮC THƯƠNG HIỆU ===\n"
            f"- Tên quy tắc: {brand_rules.get('rule_name')}\n"
            f"- Từ cấm xuất hiện: {brand_rules.get('forbidden_words')}\n"
            f"- Từ khóa bắt buộc có: {brand_rules.get('mandatory_keywords')}\n"
            f"- Tone giọng chuẩn: {brand_rules.get('tone_of_voice')}\n\n"
            "=== DANH SÁCH BÀI VIẾT CẦN KIỂM DUYỆT ==="
            f"{posts_text}\n\n"
            "Hãy kiểm tra từng bài tỉ mỉ, chấm điểm compliance_score từ 0-100, liệt kê vi phạm và gợi ý sửa. "
            "BẮT BUỘC trả về kết quả theo đúng định dạng JSON."
        )

    def validate_output(self, output: Dict[str, Any]) -> Tuple[bool, str]:
        return validate_agent3_output(output)
