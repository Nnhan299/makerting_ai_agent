"""
Agent 2: Campaign Copywriter Agent.
Nhận thông tin phân tích từ Agent 1 và Brief chiến dịch để sinh danh sách 20-30 bài đăng theo phễu 3 giai đoạn.
"""

from typing import Dict, Any, Tuple
from agents.base_agent import BaseAgent
from utils.json_parser import validate_agent2_output


class CampaignCopywriterAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__(
            name="Campaign Copywriter Agent",
            llm_client=llm_client,
            system_prompt_path="prompts/agent2_system.txt"
        )

    def build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        brief = input_data.get("brief", {})
        insights = input_data.get("insights", {})

        return (
            "Dựa trên phân tích thị trường từ Chuyên gia Thị trường (Agent 1):\n"
            f"- Target Persona: {insights.get('target_persona')}\n"
            f"- Pain Points: {insights.get('pain_points')}\n"
            f"- USP: {insights.get('usp')}\n"
            f"- Các góc tiếp cận truyền thông: {insights.get('communication_angles')}\n\n"
            "Kết hợp với các thông tin gốc của Chiến dịch:\n"
            f"- Tên chiến dịch: {brief.get('name')}\n"
            f"- Tên sản phẩm: {brief.get('product_name')}\n"
            f"- Kênh xuất bản yêu cầu: {brief.get('channels')}\n"
            f"- Thời gian chạy: {brief.get('start_date')} đến {brief.get('end_date')}\n\n"
            "Hãy sáng tạo kịch bản 20 - 30 bài viết Marketing phân bổ hợp lý theo phễu 3 giai đoạn (Teaser -> Launch -> CTA) "
            "cho các kênh được yêu cầu. Phân bổ ngày đăng (scheduled_date) rải đều trong khoảng thời gian của chiến dịch. "
            "BẮT BUỘC trả về kết quả theo chuẩn JSON."
        )

    def validate_output(self, output: Dict[str, Any]) -> Tuple[bool, str]:
        return validate_agent2_output(output)
