"""
Lớp trừu tượng BaseAgent cho tất cả các AI Agent trong hệ thống Marketing AI.
"""

import os
import datetime
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

logger = logging.getLogger("BaseAgent")


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
        Đọc file system prompt.
        """
        if not os.path.exists(path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(base_dir, path)
            
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

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
