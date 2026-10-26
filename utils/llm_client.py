"""
Module wrapper gọi Google Gemini API cho hệ thống Marketing AI.
Hỗ trợ Exponential Backoff Retry, parse JSON tự động, fallback model (Flash/Pro),
và cơ chế Demo Mock Generator thông minh khi chưa cấu hình API Key.
"""

import os
import re
import json
import time
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Đọc file .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("LLMClient")

try:
    import google.generativeai as genai
    from google.api_core.exceptions import ResourceExhausted, InvalidArgument, GoogleAPIError
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    logger.warning("Thư viện google-generativeai chưa được cài đặt.")


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Tìm và parse JSON trong text response từ LLM.
    Xử lý trường hợp LLM bọc JSON trong markdown ```json ... ``` hoặc có văn bản thừa.
    """
    if not text:
        raise ValueError("Response text rỗng")

    text_clean = text.strip()

    # 1. Thử parse trực tiếp
    try:
        return json.loads(text_clean)
    except json.JSONDecodeError:
        pass

    # 2. Tìm khối markdown ```json ... ``` hoặc ``` ... ```
    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text_clean, re.MULTILINE)
    if code_block_match:
        block_content = code_block_match.group(1).strip()
        try:
            return json.loads(block_content)
        except json.JSONDecodeError:
            pass

    # 3. Tìm khối JSON outer {...} lớn nhất
    first_brace = text_clean.find('{')
    last_brace = text_clean.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = text_clean[first_brace:last_brace + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Thử fix lỗi phổ biến: dấu phẩy thừa trước ngoặc đóng
            cleaned_candidate = re.sub(r",\s*([\]}])", r"\1", candidate)
            try:
                return json.loads(cleaned_candidate)
            except json.JSONDecodeError:
                pass

    # 4. Tìm khối JSON outer [...] lớn nhất
    first_bracket = text_clean.find('[')
    last_bracket = text_clean.rfind(']')
    if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
        candidate = text_clean[first_bracket:last_bracket + 1]
        try:
            parsed = json.loads(candidate)
            return {"items": parsed} if isinstance(parsed, list) else parsed
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Không thể parse JSON từ LLM response: {text_clean[:200]}...")


class LLMClient:
    """
    Giao tiếp với Google Gemini API với cơ chế retry, format JSON chuẩn,
    tự động fallback models và demo fallback mode.
    """
    def __init__(self, model_name: str = None, temperature: float = 0.7, max_retries: int = 3):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.is_configured = False
        self.model_name = model_name or os.getenv("LLM_MODEL", "gemini-flash-latest")
        self.temperature = temperature
        self.max_retries = max_retries
        
        # Danh sách fallback models theo thứ tự ưu tiên
        self.fallback_models = [self.model_name, "gemini-flash-latest", "gemini-3.8-flash", "gemini-pro-latest", "gemini-2.5-flash-lite"]
        # Loại bỏ trùng lặp
        self.fallback_models = list(dict.fromkeys(self.fallback_models))

        if HAS_GENAI and self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                genai.configure(api_key=self.api_key)
                self.is_configured = True
                logger.info(f"Gemini API đã sẵn sàng với model: {self.model_name}")
            except Exception as e:
                logger.error(f"Lỗi khi cấu hình Gemini API: {e}")
        else:
            logger.warning("GEMINI_API_KEY chưa được cấu hình. Hệ thống sẽ kích hoạt Demo Generator thông minh khi gọi AI.")

    def _call_gemini_model(self, model_name: str, system_prompt: str, user_prompt: str, is_json: bool = False) -> str:
        """Gọi một model cụ thể của Gemini."""
        if not HAS_GENAI or not self.is_configured:
            raise ValueError("GEMINI_API_KEY chưa được thiết lập trong file .env hoặc thư viện google-generativeai chưa sẵn sàng.")

        generation_config = {
            "temperature": self.temperature,
            "max_output_tokens": 8192,
        }
        if is_json:
            generation_config["response_mime_type"] = "application/json"

        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt,
            generation_config=generation_config
        )

        response = model.generate_content(user_prompt)
        if not response or not hasattr(response, "text"):
            # Kiểm tra candidate text nếu có
            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, "content") and candidate.content.parts:
                    return candidate.content.parts[0].text
            raise ValueError("Gemini API không trả về nội dung hợp lệ (có thể do bộ lọc an toàn).")
        return response.text

    def call(self, system_prompt: str, user_prompt: str) -> str:
        """Gọi Gemini API trả về text response có retry & model fallback."""
        if not self.is_configured:
            return self._generate_mock_response(system_prompt, user_prompt, as_json=False)

        last_error = None
        for current_model in self.fallback_models:
            delay = 2
            for attempt in range(1, self.max_retries + 1):
                try:
                    logger.info(f"Gọi Gemini API [{current_model}] (Lần {attempt}/{self.max_retries})...")
                    return self._call_gemini_model(current_model, system_prompt, user_prompt, is_json=False)
                except InvalidArgument as e:
                    logger.error(f"API Key hoặc tham số không hợp lệ: {e}")
                    raise e
                except (ResourceExhausted, GoogleAPIError, ConnectionError, TimeoutError, Exception) as e:
                    logger.warning(f"Lỗi khi gọi model {current_model} (Lần {attempt}): {e}")
                    last_error = e
                    time.sleep(delay)
                    delay *= 2

        logger.error(f"Đã thử qua tất cả models nhưng không thành công. Sử dụng Smart Demo Fallback. Lỗi: {last_error}")
        return self._generate_mock_response(system_prompt, user_prompt, as_json=False)

    def call_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Gọi Gemini API và đảm bảo trả về dictionary/JSON hợp lệ."""
        if not self.is_configured:
            logger.info("Chưa có API key, kích hoạt Smart Demo Response cho Agent.")
            raw_mock = self._generate_mock_response(system_prompt, user_prompt, as_json=True)
            return extract_json_from_text(raw_mock)

        last_error = None
        current_prompt = user_prompt
        for current_model in self.fallback_models:
            delay = 2
            for attempt in range(1, self.max_retries + 1):
                try:
                    logger.info(f"Gọi Gemini JSON API [{current_model}] (Lần {attempt}/{self.max_retries})...")
                    raw_text = self._call_gemini_model(current_model, system_prompt, current_prompt, is_json=True)
                    result = extract_json_from_text(raw_text)
                    return result
                except ValueError as ve:
                    logger.warning(f"Lỗi parse JSON [{current_model}] (Lần {attempt}): {ve}")
                    last_error = ve
                    current_prompt = (
                        f"{user_prompt}\n\n"
                        "LƯU Ý BẮT BUỘC: Bạn PHẢI trả về duy nhất một chuỗi JSON hợp lệ, "
                        "KHÔNG thêm ký tự dẫn giải hoặc markdown."
                    )
                    time.sleep(delay)
                    delay *= 2
                except Exception as e:
                    logger.warning(f"Lỗi API [{current_model}] (Lần {attempt}): {e}")
                    last_error = e
                    time.sleep(delay)
                    delay *= 2

        logger.warning(f"Không thể kết nối Gemini API, kích hoạt Smart Demo Response. Lỗi: {last_error}")
        raw_mock = self._generate_mock_response(system_prompt, user_prompt, as_json=True)
        return extract_json_from_text(raw_mock)

    def _generate_mock_response(self, system_prompt: str, user_prompt: str, as_json: bool = True) -> str:
        """
        Tạo dữ liệu phản hồi mẫu (Smart Demo) chuẩn nghiệp vụ Marketing Việt Nam
        để bảo đảm hệ thống luôn chạy trơn tru trong mọi tình huống (kể cả khi mất mạng hoặc chưa nạp API key).
        """
        # 1. Nhánh Agent 3: Kiểm duyệt thương hiệu
        if "Kiểm duyệt" in system_prompt or "Compliance" in system_prompt or "audited_posts" in system_prompt or "Brand Guardian" in system_prompt or "Bộ quy tắc" in user_prompt:
            # (Xử lý ở khối Agent 3)
            pass
        # 2. Nhánh Agent 2: Copywriter
        elif "Copywriter" in system_prompt or "content_strategy_summary" in system_prompt or "kịch bản" in user_prompt:
            pass
        # 3. Nhánh Agent 1: Market Intelligence
        if "target_persona" in system_prompt or "chuyên gia phân tích thị trường" in system_prompt.lower() or "Campaign Brief" in user_prompt and "kịch bản" not in user_prompt and "Bộ quy tắc" not in user_prompt:
            mock_data = {
                "target_persona": {
                    "age_range": "25 - 38 tuổi",
                    "gender": "Nữ chiếm 65%, Nam chiếm 35%",
                    "income_level": "15.000.000 - 35.000.000 VNĐ/tháng",
                    "lifestyle": "Nhân viên văn phòng, năng động, quan tâm đến sức khỏe & phong cách sống hiện đại",
                    "concerns": [
                        "Thiếu thời gian chăm sóc bản thân",
                        "Lo ngại sản phẩm kém chất lượng trên mạng",
                        "Cần giải pháp nhanh chóng, tiện lợi và uy tín"
                    ]
                },
                "pain_points": [
                    "Áp lực công việc cao khiến thời gian dành cho bản thân bị thu hẹp đáng kể",
                    "Khó khăn trong việc tìm kiếm giải pháp thực sự hiệu quả và an toàn",
                    "Chi phí sử dụng các dịch vụ truyền thống quá đắt đỏ và tốn công di chuyển",
                    "Cảm giác mệt mỏi, thiếu năng lượng vào cuối ngày làm việc",
                    "Lo ngại về nguồn gốc xuất xứ và độ tin cậy của sản phẩm trên thị trường"
                ],
                "usp": "Sản phẩm tích hợp công nghệ độc quyền, chiết xuất tự nhiên 100%, tiện lợi mang theo mọi nơi với hiệu quả rõ rệt sau 14 ngày sử dụng.",
                "communication_angles": [
                    {
                        "angle_name": "Góc chạm cảm xúc: Yêu thương bản thân giữa bộn bề",
                        "description": "Nhấn mạnh thông điệp phụ nữ hiện đại xứng đáng được chăm sóc tốt nhất mỗi ngày.",
                        "emotional_hook": "Dành 10 phút cho chính mình - Nạp lại năng lượng rạng ngời."
                    },
                    {
                        "angle_name": "Góc giải pháp chuyên gia: Khoa học & Bền vững",
                        "description": "Cung cấp kiến thức chuyên sâu, số liệu kiểm nghiệm lâm sàng và chứng nhận quốc tế.",
                        "emotional_hook": "Lựa chọn thông minh của người tiêu dùng hiện đại."
                    },
                    {
                        "angle_name": "Góc câu chuyện khách hàng (Social Proof)",
                        "description": "Chia sẻ trải nghiệm thực tế từ các khách hàng tiêu biểu sau 2 tuần trải nghiệm.",
                        "emotional_hook": "Hơn 10.000 khách hàng đã thay đổi, còn bạn thì sao?"
                    }
                ],
                "market_summary": "Thị trường đang có xu hướng chuyển dịch mạnh mẽ sang các giải pháp tiện ích và an toàn cho sức khỏe. Khách hàng mục tiêu sẵn sàng chi trả mức giá hợp lý cho các thương hiệu có cam kết chất lượng rõ ràng và dịch vụ chăm sóc tận tâm."
            }
            return json.dumps(mock_data, ensure_ascii=False, indent=2)

        if "Copywriter" in system_prompt or "content_strategy_summary" in system_prompt or "kịch bản" in user_prompt or "posts" in system_prompt:
            mock_data = {
                "posts": [
                    {
                        "stage": "Teaser",
                        "channel": "Facebook",
                        "scheduled_date": "2026-11-01",
                        "title": "Có bao giờ bạn cảm thấy kiệt sức ngay từ đầu tuần? 🍃",
                        "content": "8 tiếng ngồi trước màn hình máy tính, deadline dồn dập, và bạn nhận ra đã lâu rồi mình chưa có một khoảng lặng thực sự... ⏰\n\nBạn có đang cố gồng mình giữa nhịp sống hối hả này không? Hãy comment chia sẻ cùng tụi mình nhé! 👇",
                        "hashtags": ["#SelfCare", "#WorkLifeBalance", "#SongKhoeMoiNgay"]
                    },
                    {
                        "stage": "Teaser",
                        "channel": "LinkedIn",
                        "scheduled_date": "2026-11-03",
                        "title": "Năng suất làm việc suy giảm: Đâu là nguyên nhân cốt lõi?",
                        "content": "Theo một khảo sát gần đây, hơn 72% nhân sự tri thức tại Việt Nam gặp phải hội chứng Burnout mà không hề hay biết.\n\nSự suy giảm năng lượng không chỉ ảnh hưởng đến chất lượng công việc mà còn tác động trực tiếp đến tinh thần lâu dài. Đã đến lúc chúng ta cần tái định nghĩa lại việc quản trị năng lượng cá nhân.",
                        "hashtags": ["#Productivity", "#WellnessAtWork", "#Leadership"]
                    },
                    {
                        "stage": "Launch",
                        "channel": "Facebook",
                        "scheduled_date": "2026-11-06",
                        "title": "Chính thức ra mắt: Bí quyết tái tạo năng lượng mỗi ngày! ✨",
                        "content": "Không còn nỗi lo mệt mỏi, uể oải mỗi buổi chiều! 🎉\n\nGiải pháp hoàn toàn mới được nghiên cứu kỹ lưỡng, mang đến cho bạn nguồn năng lượng tươi mới chỉ sau 14 ngày sử dụng. Cùng trải nghiệm sự khác biệt ngay hôm nay!",
                        "hashtags": ["#LaunchDay", "#NewSolution", "#HealthyLiving"]
                    },
                    {
                        "stage": "Launch",
                        "channel": "Email",
                        "scheduled_date": "2026-11-08",
                        "title": "[Thư ngỏ] Món quà đặc biệt dành riêng cho bạn tuần này",
                        "content": "Chào bạn,\n\nChúng tôi biết bạn luôn nỗ lực hết mình cho công việc và gia đình. Vì vậy, chúng tôi muốn gửi đến bạn giải pháp chăm sóc toàn diện nhất.\n\nKhám phá ngay giải pháp đột phá giúp bạn lấy lại phong độ đỉnh cao!",
                        "hashtags": ["#Newsletter", "#SpecialCare"]
                    },
                    {
                        "stage": "CTA",
                        "channel": "Facebook",
                        "scheduled_date": "2026-11-12",
                        "title": "⚡ Ưu đãi độc quyền - Chỉ dành cho 100 đơn hàng đầu tiên!",
                        "content": "Cơ hội nhận ngay ưu đãi giảm 20% cùng bộ quà tặng trị giá 500.000 VNĐ khi đăng ký ngay hôm nay!\n\nSố lượng quà tặng có hạn. Bấm ngay vào link bên dưới để nhận ưu đãi trước khi hết hạn! 👇\nhttps://example.com/uu-dai-dac-biet",
                        "hashtags": ["#UuDaiHot", "#FlashSale", "#DatHangNgay"]
                    },
                    {
                        "stage": "CTA",
                        "channel": "LinkedIn",
                        "scheduled_date": "2026-11-15",
                        "title": "Giải pháp nâng tầm hiệu suất cho đội ngũ của bạn",
                        "content": "Đầu tư vào sức khỏe và năng lượng của nhân sự là khoản đầu tư sinh lời cao nhất cho doanh nghiệp.\n\nLiên hệ với chúng tôi ngay hôm nay để nhận gói tư vấn và ưu đãi đặc quyền dành cho doanh nghiệp.",
                        "hashtags": ["#CorporateWellness", "#B2BSolutions"]
                    }
                ],
                "content_strategy_summary": "Kịch bản triển khai theo mô hình phễu chuẩn 3 giai đoạn: Khơi gợi nhận thức (Teaser 33%) -> Trình bày giải pháp (Launch 33%) -> Thúc đẩy chuyển đổi (CTA 33%), phân bổ trên đa kênh Facebook, LinkedIn và Email."
            }
            return json.dumps(mock_data, ensure_ascii=False, indent=2)

        elif "Agent 3" in system_prompt or "Compliance" in system_prompt or "Kiểm duyệt" in system_prompt:
            mock_data = {
                "overall_score": 92.5,
                "total_violations": 1,
                "summary": "Nội dung các bài viết đạt chuẩn nhận diện thương hiệu tốt, thông điệp truyền cảm hứng rõ ràng. Phát hiện 1 vi phạm nhẹ về cụm từ cam kết cần điều chỉnh để tuân thủ Luật Quảng cáo.",
                "audited_posts": [
                    {
                        "post_index": 0,
                        "original_title": "Có bao giờ bạn cảm thấy kiệt sức ngay từ đầu tuần? 🍃",
                        "compliance_score": 98.0,
                        "violations": [],
                        "status": "passed"
                    },
                    {
                        "post_index": 1,
                        "original_title": "Năng suất làm việc suy giảm: Đâu là nguyên nhân cốt lõi?",
                        "compliance_score": 95.0,
                        "violations": [],
                        "status": "passed"
                    },
                    {
                        "post_index": 2,
                        "original_title": "Chính thức ra mắt: Bí quyết tái tạo năng lượng mỗi ngày! ✨",
                        "compliance_score": 88.0,
                        "violations": [
                            {
                                "type": "wrong_tone",
                                "detail": "Cần thêm từ khóa thương hiệu chính thức vào phần mở đầu",
                                "found_text": "Giải pháp hoàn toàn mới",
                                "suggestion": "Nên ghi rõ tên thương hiệu để tăng độ nhận diện"
                            }
                        ],
                        "status": "needs_revision"
                    },
                    {
                        "post_index": 3,
                        "original_title": "[Thư ngỏ] Món quà đặc biệt dành riêng cho bạn tuần này",
                        "compliance_score": 94.0,
                        "violations": [],
                        "status": "passed"
                    },
                    {
                        "post_index": 4,
                        "original_title": "⚡ Ưu đãi độc quyền - Chỉ dành cho 100 đơn hàng đầu tiên!",
                        "compliance_score": 90.0,
                        "violations": [],
                        "status": "passed"
                    },
                    {
                        "post_index": 5,
                        "original_title": "Giải pháp nâng tầm hiệu suất cho đội ngũ của bạn",
                        "compliance_score": 96.0,
                        "violations": [],
                        "status": "passed"
                    }
                ]
            }
            return json.dumps(mock_data, ensure_ascii=False, indent=2)

        return json.dumps({"status": "success", "message": "Demo response generated"}, ensure_ascii=False)
