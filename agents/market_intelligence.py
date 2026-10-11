"""
Agent 1: Market & Competitor Intelligence Agent.
Phân tích Campaign Brief để tìm ra Target Persona, Pain Points, USP và các góc truyền thông.
"""

from typing import Dict, Any, Tuple
from agents.base_agent import BaseAgent
from utils.json_parser import validate_agent1_output


class MarketIntelligenceAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__(
            name="Market Intelligence Agent",
            llm_client=llm_client,
            system_prompt_path="prompts/agent1_system.txt"
        )

    def build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        campaign_name = input_data.get("name", "")
        product_name = input_data.get("product_name", "")
        target_audience = input_data.get("target_audience", "")
        budget = input_data.get("budget", "")
        channels = input_data.get("channels", "")
        start_date = input_data.get("start_date", "")
        end_date = input_data.get("end_date", "")

        return (
            "Hãy phân tích kĩ lưỡng Campaign Brief sau đây:\n"
            f"- Tên chiến dịch: {campaign_name}\n"
            f"- Tên sản phẩm/dịch vụ: {product_name}\n"
            f"- Đối tượng mục tiêu: {target_audience}\n"
            f"- Ngân sách: {budget}\n"
            f"- Kênh xuất bản: {channels}\n"
            f"- Thời gian thực hiện: Từ {start_date} đến {end_date}\n\n"
            "Hãy phân tích chi tiết và trả về JSON chuẩn theo đúng format đã quy định trong System Prompt."
        )

    def validate_output(self, output: Dict[str, Any]) -> Tuple[bool, str]:
        return validate_agent1_output(output)
