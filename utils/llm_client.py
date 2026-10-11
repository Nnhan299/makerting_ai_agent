"""
Module wrapper gọi Google Gemini API cho hệ thống Marketing AI.
Hỗ trợ Exponential Backoff Retry, parse JSON tự động, và xử lý lỗi chuyên sâu.
"""

import os
import re
import json
import time
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, InvalidArgument, GoogleAPIError

# Đọc file .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("LLMClient")


def extract_json_from_text(text: str) -> dict:
    """
    Tìm và parse JSON trong text response từ LLM.
    Xử lý trường hợp LLM bọc JSON trong markdown ```json ... ``` hoặc có văn bản thừa.
    
    Args:
        text: Văn bản trả về từ LLM
        
    Returns:
        dict: Dữ liệu JSON đã parse
    
    Raises:
        ValueError: Nếu không tìm thấy JSON hợp lệ
    """
    if not text:
        raise ValueError("Response text rong")
    
    # 1. Thử parse trực tiếp
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    
    # 2. Xóa markdown code block ```json ... ```
    cleaned_text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned_text = re.sub(r"\s*```$", "", cleaned_text, flags=re.MULTILINE)
    try:
        return json.loads(cleaned_text.strip())
    except json.JSONDecodeError:
        pass
    
    # 3. Tìm khối JSON trong cặp {...} hoặc [...]
    match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
            
    raise ValueError("Khong the parse JSON tu LLM response")


class LLMClient:
    """
    Class giao tiếp với Google Gemini API với cơ chế retry và format JSON.
    """
    def __init__(self, model_name: str = None, temperature: float = 0.7, max_retries: int = 3):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            logger.warning("GEMINI_API_KEY chua duoc cau hinh hop le trong file .env!")
        else:
            genai.configure(api_key=api_key)
            
        self.model_name = model_name or os.getenv("LLM_MODEL", "gemini-1.5-pro")
        self.temperature = temperature
        self.max_retries = max_retries
        
    def call(self, system_prompt: str, user_prompt: str) -> str:
        """
        Gọi Gemini API, trả về text response.
        Thực hiện Exponential Backoff Retry nếu gặp lỗi mạng/rate limit.
        """
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature
            )
        )
        
        delay = 2
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Goi Gemini API (Lan {attempt}/{self.max_retries})...")
                response = model.generate_content(user_prompt)
                return response.text
            except InvalidArgument as e:
                logger.error(f"API Key hoac tham so khong hop le: {e}")
                raise e
            except (ResourceExhausted, GoogleAPIError, ConnectionError, TimeoutError) as e:
                logger.warning(f"Loi API/Mang khi goi Gemini (Lan {attempt}): {e}")
                if attempt == self.max_retries:
                    logger.error("Da het so lan retry phep. Ném exception.")
                    raise e
                time.sleep(delay)
                delay *= 2
            except Exception as e:
                logger.error(f"Loi khong xac dinh khi goi Gemini: {e}")
                if attempt == self.max_retries:
                    raise e
                time.sleep(delay)
                delay *= 2

    def call_json(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Gọi Gemini API và đảm bảo trả về dictionary/JSON hợp lệ.
        Nếu response không phải JSON hợp lệ, tự động retry kèm prompt sửa định dạng.
        """
        current_prompt = user_prompt
        delay = 2
        
        for attempt in range(1, self.max_retries + 1):
            try:
                raw_text = self.call(system_prompt, current_prompt)
                result = extract_json_from_text(raw_text)
                return result
            except ValueError as ve:
                logger.warning(f"Loi parse JSON (Lan {attempt}/{self.max_retries}): {ve}")
                if attempt == self.max_retries:
                    raise ve
                # Thêm hướng dẫn sửa lỗi JSON cho lần thử tiếp theo
                current_prompt = (
                    f"{user_prompt}\n\n"
                    "LƯU Ý QUAN TRỌNG: Kết quả trước đó của bạn không thể parse thành JSON. "
                    "Hãy trả về CHÍNH XÁC một đối tượng JSON duy nhất, KHÔNG thêm bất kỳ văn bản giải thích hay đoạn mã markdown nào khác."
                )
                time.sleep(delay)
                delay *= 2
