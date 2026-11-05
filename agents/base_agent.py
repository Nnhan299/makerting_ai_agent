"""
Lớp trừu tượng BaseAgent cho tất cả các AI Agent trong hệ thống Marketing AI.
"""

import os
import datetime
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

logger = logging.getLogger("BaseAgent")


DEFAULT_PROMPTS = {
    "prompts/agent1_system.txt": (
        "Bạn là chuyên gia phân tích thị trường Marketing với 15 năm kinh nghiệm tại Việt Nam.\n\n"
        "Nhiệm vụ: Đọc Campaign Brief và phân tích sâu sắc thị trường để đưa ra thông tin chiến lược:\n"
        "1. Target Persona: Chân dung khách hàng mục tiêu chi tiết.\n"
        "2. Pain Points: Ít nhất 5 nỗi đau/vấn đề thực tế của khách hàng.\n"
        "3. USP: Điểm bán hàng độc nhất của sản phẩm/dịch vụ.\n"
        "4. Communication Angles: Từ 3 đến 5 góc tiếp cận truyền thông.\n"
        "5. Market Summary: Tóm tắt phân tích thị trường trong 3-5 câu.\n\n"
        "BẮT BUỘC trả về kết quả dưới dạng JSON chuẩn theo các trường: target_persona, pain_points, usp, communication_angles, market_summary."
    ),
    "prompts/agent2_system.txt": (
        "Bạn là Copywriter chuyên nghiệp với 10 năm kinh nghiệm sáng tạo nội dung Marketing tại Việt Nam.\n\n"
        "Nhiệm vụ: Dựa trên phân tích từ Agent 1 và Campaign Brief để tạo danh sách bài viết phân bổ theo phễu 3 giai đoạn:\n"
        "1. Teaser (Nhận thức nỗi đau)\n"
        "2. Launch (Giải pháp sản phẩm)\n"
        "3. CTA (Kêu gọi hành động & chốt sale)\n\n"
        "BẮT BUỘC trả về kết quả dưới dạng JSON chuẩn gồm 'posts' và 'content_strategy_summary'."
    ),
    "prompts/agent3_system.txt": (
        "Bạn là Chuyên gia Kiểm duyệt Thương hiệu (Brand Guardian) tại Việt Nam.\n\n"
        "Nhiệm vụ: Đánh giá bài viết dựa trên Brand Rules (từ cấm, từ bắt buộc, tone of voice, luật quảng cáo).\n"
        "Chấm điểm tuân thủ (0-100) và đưa ra gợi ý sửa đổi cho từng vi phạm.\n\n"
        "BẮT BUỘC trả về kết quả dưới dạng JSON chuẩn gồm: overall_score, total_violations, summary, audited_posts."
    ),
}


class BaseAgent(ABC):
    """
    Lớp cơ sở trừu tượng cho 3 Agent.
    """
    def __init__(self, name: str, llm_client, system_prompt_path: str):
        self.name = name
        self.llm_client = llm_client
        self.system_prompt = self._load_system_prompt(system_prompt_path)
        self.logs = []

    def _load_system_prompt(self, path: str) -> str:
        """
        Đọc file system prompt có cơ chế fallback tự động.
        """
        resolved_path = path
        if not os.path.exists(resolved_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resolved_path = os.path.join(base_dir, path)
            
        if os.path.exists(resolved_path):
            try:
                with open(resolved_path, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception:
                pass
                
        # Fallback vào prompt mặc định nếu không có file trên đĩa
        norm_key = path.replace("\\", "/")
        for k, v in DEFAULT_PROMPTS.items():
            if k in norm_key:
                return v
        return DEFAULT_PROMPTS.get("prompts/agent1_system.txt", "")

    def log(self, message: str):
        """
        Ghi log có timestamp.
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {self.name}: {message}"
        self.logs.append(log_entry)
        logger.info(log_entry)

    @abstractmethod
    def build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        Mỗi Agent tự triển khai việc xây dựng user prompt từ dữ liệu đầu vào.
        """
        pass

    @abstractmethod
    def validate_output(self, output: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Mỗi Agent tự kiểm tra tính hợp lệ của kết quả trả về.
        """
        pass

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Quy trình xử lý chung cho mọi Agent:
        1. Ghi log khởi chạy
        2. Tạo prompt
        3. Gọi LLM trả về JSON
        4. Validate output
        5. Ghi log thành công và trả về kết quả
        """
        self.log("Bắt đầu xử lý...")
        user_prompt = self.build_user_prompt(input_data)
        
        result = self.llm_client.call_json(self.system_prompt, user_prompt)
        
        is_valid, error_msg = self.validate_output(result)
        if not is_valid:
            self.log(f"Lỗi validate kết quả: {error_msg}")
            raise ValueError(f"Agent '{self.name}' sinh ra kết quả không hợp lệ: {error_msg}")
            
        self.log("Xử lý hoàn thành thành công!")
        return result
