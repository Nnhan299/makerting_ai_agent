# 📋 HƯỚNG DẪN PROMPT XÂY DỰNG TỪNG CHỨC NĂNG
# Hệ thống Quản trị Chiến dịch Marketing tích hợp AI Multi-Agent

> **Mục đích:** File này chứa các prompt chi tiết để đưa cho AI (ChatGPT/Gemini/Claude) xây dựng từng chức năng của phần mềm.
> **Cách dùng:** Copy từng prompt bên dưới, paste vào AI, và yêu cầu AI viết code cho bạn.
> **Thứ tự thực hiện:** Làm theo đúng thứ tự từ Bước 0 → Bước 8. Mỗi bước phụ thuộc vào bước trước đó.

---

## 📌 TỔNG QUAN DỰ ÁN

- **Tên đề tài:** Xây dựng Hệ thống Quản trị Chiến dịch Marketing tích hợp AI Multi-Agent
- **Công nghệ:** Python 3.10+, Streamlit (Localhost Web App), SQLite, Google Gemini API
- **Kiến trúc:** Desktop Local App – 3 lớp (Presentation → Business Logic → Data Access)
- **AI Engine:** 3 Agent tuần tự (Market Intelligence → Copywriter → Brand Auditor)

---

## 🗂️ CẤU TRÚC THƯ MỤC DỰ ÁN MỤC TIÊU

```
marketing-ai/
├── .env                          # API keys, cấu hình bí mật
├── .env.example                  # Mẫu file .env
├── requirements.txt              # Dependencies
├── config.yaml                   # Cấu hình ứng dụng
├── README.md                     # Hướng dẫn sử dụng
│
├── database/
│   ├── __init__.py
│   ├── connection.py             # Kết nối SQLite
│   ├── models.py                 # Định nghĩa schema các bảng
│   └── crud.py                   # Các hàm CRUD (Create/Read/Update/Delete)
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py             # Lớp trừu tượng BaseAgent
│   ├── market_intelligence.py    # Agent 1: Phân tích thị trường
│   ├── campaign_copywriter.py    # Agent 2: Viết nội dung
│   ├── brand_auditor.py          # Agent 3: Kiểm duyệt thương hiệu
│   └── orchestrator.py           # Bộ điều phối pipeline 3 Agent
│
├── prompts/
│   ├── agent1_system.txt         # System prompt cho Agent 1
│   ├── agent2_system.txt         # System prompt cho Agent 2
│   └── agent3_system.txt         # System prompt cho Agent 3
│
├── ui/
│   ├── app.py                    # Entry point Streamlit (trang chính)
│   ├── pages/
│   │   ├── 1_campaigns.py        # Trang quản lý chiến dịch
│   │   ├── 2_brand_rules.py      # Trang quản lý Brand Rules
│   │   ├── 3_run_ai.py           # Trang chạy AI Pipeline
│   │   ├── 4_calendar.py         # Trang Content Calendar
│   │   └── 5_export.py           # Trang xuất file / gửi email
│   └── components/
│       ├── sidebar.py            # Sidebar navigation
│       └── post_card.py          # Component hiển thị bài viết
│
├── utils/
│   ├── __init__.py
│   ├── llm_client.py             # Wrapper gọi Gemini/OpenAI API
│   ├── json_parser.py            # Parse & validate JSON output từ LLM
│   └── export_excel.py           # Xuất file Excel
│
└── data/
    └── marketing.db              # File SQLite database (tự tạo)
```

---

## ⚡ BƯỚC 0: KHỞI TẠO DỰ ÁN & CÀI ĐẶT

### Prompt 0.1 – Tạo file requirements.txt

```
Tạo file requirements.txt cho dự án Python với các thư viện sau:
- streamlit (giao diện web localhost)
- google-generativeai (gọi Gemini API)
- python-dotenv (đọc file .env)
- pyyaml (đọc config.yaml)
- openpyxl (xuất file Excel)
- pandas (xử lý dữ liệu bảng)
- plotly (biểu đồ cho Streamlit)

Ghi rõ phiên bản tương thích với Python 3.10+.
```

### Prompt 0.2 – Tạo file .env.example và config.yaml

```
Tạo 2 file cấu hình cho dự án Marketing AI Desktop App:

1. File `.env.example` chứa:
   - GEMINI_API_KEY=your_gemini_api_key_here
   - LLM_MODEL=gemini-1.5-pro
   - DATABASE_PATH=data/marketing.db
   - SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM, EMAIL_TO (cho chức năng gửi email)

2. File `config.yaml` chứa:
   - app_name: "Marketing AI Campaign Manager"
   - version: "1.0.0"
   - llm:
       model: "gemini-1.5-pro"
       temperature: 0.7
       max_retries: 3
       retry_delay_seconds: 2
   - pipeline:
       max_posts_per_campaign: 30
       default_stages: ["Teaser", "Launch", "CTA"]
       supported_channels: ["Facebook", "LinkedIn", "Email"]
   - export:
       excel_template: true
       include_audit_report: true
```

---

## ⚡ BƯỚC 1: XÂY DỰNG CƠ SỞ DỮ LIỆU (DATABASE)

### Prompt 1.1 – Kết nối SQLite & tạo bảng

```
Viết module Python cho cơ sở dữ liệu SQLite của hệ thống Marketing AI.

Yêu cầu:
1. File `database/connection.py`: Hàm kết nối SQLite, tự tạo file DB nếu chưa có.
2. File `database/models.py`: Tạo 4 bảng sau bằng lệnh SQL CREATE TABLE IF NOT EXISTS:

BẢNG 1 – campaigns:
| Cột              | Kiểu          | Ràng buộc                              |
|-------------------|---------------|----------------------------------------|
| id               | INTEGER        | PRIMARY KEY AUTOINCREMENT              |
| name             | TEXT           | NOT NULL                               |
| product_name     | TEXT           | NOT NULL                               |
| target_audience  | TEXT           |                                        |
| budget           | TEXT           |                                        |
| channels         | TEXT           | (lưu dạng JSON string: ["Facebook","LinkedIn"]) |
| start_date       | TEXT           | NOT NULL (format: YYYY-MM-DD)          |
| end_date         | TEXT           | NOT NULL                               |
| status           | TEXT           | DEFAULT 'Draft' (Draft/In-Progress/Approved/Completed) |
| created_at       | TEXT           | DEFAULT CURRENT_TIMESTAMP              |
| updated_at       | TEXT           |                                        |

BẢNG 2 – campaign_posts:
| Cột              | Kiểu          | Ràng buộc                              |
|-------------------|---------------|----------------------------------------|
| id               | INTEGER        | PRIMARY KEY AUTOINCREMENT              |
| campaign_id      | INTEGER        | FK → campaigns(id) ON DELETE CASCADE   |
| stage            | TEXT           | NOT NULL (Teaser/Launch/CTA)           |
| channel          | TEXT           | NOT NULL (Facebook/LinkedIn/Email)     |
| title            | TEXT           |                                        |
| content          | TEXT           | NOT NULL                               |
| hashtags         | TEXT           |                                        |
| scheduled_date   | TEXT           |                                        |
| status           | TEXT           | DEFAULT 'Pending' (Pending/Approved/Rejected) |
| created_at       | TEXT           | DEFAULT CURRENT_TIMESTAMP              |

BẢNG 3 – brand_rules:
| Cột               | Kiểu          | Ràng buộc                             |
|---------------------|---------------|---------------------------------------|
| id                | INTEGER        | PRIMARY KEY AUTOINCREMENT             |
| rule_name         | TEXT           | NOT NULL                              |
| forbidden_words   | TEXT           | (lưu dạng JSON array string)          |
| mandatory_keywords| TEXT           | (lưu dạng JSON array string)          |
| tone_of_voice     | TEXT           |                                       |
| industry          | TEXT           |                                       |
| created_at        | TEXT           | DEFAULT CURRENT_TIMESTAMP             |

BẢNG 4 – audit_logs:
| Cột               | Kiểu          | Ràng buộc                             |
|---------------------|---------------|---------------------------------------|
| id                | INTEGER        | PRIMARY KEY AUTOINCREMENT             |
| post_id           | INTEGER        | FK → campaign_posts(id)               |
| rule_id           | INTEGER        | FK → brand_rules(id)                  |
| compliance_score  | REAL           | CHECK(compliance_score >= 0 AND compliance_score <= 100) |
| violations_json   | TEXT           | NOT NULL (lưu JSON string)            |
| suggestions       | TEXT           |                                       |
| audited_at        | TEXT           | DEFAULT CURRENT_TIMESTAMP             |

Lưu ý:
- Bật PRAGMA foreign_keys = ON khi kết nối.
- Hàm init_database() gọi tạo tất cả bảng.
- Sử dụng context manager cho connection.
```

### Prompt 1.2 – Các hàm CRUD

```
Viết file `database/crud.py` chứa các hàm CRUD cho 4 bảng của hệ thống Marketing AI.
Sử dụng module sqlite3 thuần Python, nhận connection làm tham số.

=== CAMPAIGNS ===
- create_campaign(conn, name, product_name, target_audience, budget, channels: list, start_date, end_date) → int (trả về id)
- get_all_campaigns(conn) → list[dict]
- get_campaign_by_id(conn, campaign_id) → dict | None
- update_campaign(conn, campaign_id, **kwargs) → bool
- update_campaign_status(conn, campaign_id, new_status: str) → bool
- delete_campaign(conn, campaign_id) → bool

=== CAMPAIGN_POSTS ===
- create_post(conn, campaign_id, stage, channel, title, content, hashtags, scheduled_date) → int
- create_posts_bulk(conn, posts: list[dict]) → list[int]  (insert nhiều bài 1 lần)
- get_posts_by_campaign(conn, campaign_id) → list[dict]
- get_post_by_id(conn, post_id) → dict | None
- update_post_content(conn, post_id, title, content, hashtags) → bool
- update_post_status(conn, post_id, new_status: str) → bool  (Approve/Reject)
- delete_posts_by_campaign(conn, campaign_id) → bool

=== BRAND_RULES ===
- create_brand_rule(conn, rule_name, forbidden_words: list, mandatory_keywords: list, tone_of_voice, industry) → int
- get_all_brand_rules(conn) → list[dict]
- get_brand_rule_by_id(conn, rule_id) → dict | None
- update_brand_rule(conn, rule_id, **kwargs) → bool
- delete_brand_rule(conn, rule_id) → bool

=== AUDIT_LOGS ===
- create_audit_log(conn, post_id, rule_id, compliance_score, violations_json: list, suggestions) → int
- create_audit_logs_bulk(conn, logs: list[dict]) → list[int]
- get_audit_by_post(conn, post_id) → dict | None
- get_audits_by_campaign(conn, campaign_id) → list[dict]

Lưu ý:
- Tất cả hàm cần có docstring tiếng Việt.
- Khi lưu list vào DB, dùng json.dumps(). Khi đọc ra, dùng json.loads().
- Xử lý lỗi IntegrityError khi FK vi phạm.
- Hàm get trả về dict (dùng conn.row_factory = sqlite3.Row).
```

---

## ⚡ BƯỚC 2: XÂY DỰNG LLM CLIENT (GỌI GEMINI API)

### Prompt 2.1 – LLM Client wrapper

```
Viết file `utils/llm_client.py` – module wrapper gọi Google Gemini API cho hệ thống Marketing AI.

Yêu cầu:
1. Đọc GEMINI_API_KEY từ file .env bằng python-dotenv.
2. Sử dụng thư viện `google-generativeai` (import google.generativeai as genai).
3. Class LLMClient với các method:

class LLMClient:
    def __init__(self, model_name="gemini-1.5-pro", temperature=0.7, max_retries=3):
        # Khởi tạo Gemini client
        
    def call(self, system_prompt: str, user_prompt: str) -> str:
        # Gọi API, trả về text response
        # Retry logic: nếu lỗi mạng/rate-limit, retry tối đa max_retries lần
        # Exponential backoff: lần 1 chờ 2s, lần 2 chờ 4s, lần 3 chờ 8s
        # Log mỗi lần retry
        
    def call_json(self, system_prompt: str, user_prompt: str) -> dict:
        # Gọi API và parse response thành JSON
        # Nếu response không phải JSON hợp lệ → retry kèm prompt bổ sung:
        #   "Hãy trả về kết quả ĐÚNG định dạng JSON. Không thêm markdown hay text nào khác."
        # Trả về dict đã parse

4. Xử lý các loại lỗi:
   - google.api_core.exceptions.ResourceExhausted (rate limit) → retry
   - google.api_core.exceptions.InvalidArgument (API key sai) → raise ngay, không retry
   - ConnectionError / Timeout → retry
   - JSON parse error → retry kèm prompt sửa

5. Hàm helper:
   def extract_json_from_text(text: str) -> dict:
       # Tìm và parse JSON trong text (LLM đôi khi trả về JSON bọc trong ```json ... ```)
       # Thử parse trực tiếp, nếu lỗi thì tìm pattern {...} hoặc [...] trong text
```

### Prompt 2.2 – JSON Parser & Validator

```
Viết file `utils/json_parser.py` – module validate JSON output từ LLM cho hệ thống Marketing AI.

Yêu cầu:
1. Validate output của Agent 1 (Market Intelligence):
   def validate_agent1_output(data: dict) -> tuple[bool, str]:
       # Kiểm tra có đủ các key: target_persona, pain_points, usp, communication_angles
       # pain_points phải là list có ≥ 3 phần tử
       # communication_angles phải là list có ≥ 2 phần tử
       # Trả về (True, "") nếu hợp lệ, (False, "lý do lỗi") nếu không

2. Validate output của Agent 2 (Campaign Copywriter):
   def validate_agent2_output(data: dict, expected_channels: list) -> tuple[bool, str]:
       # Kiểm tra có key "posts" là list
       # Mỗi post phải có: stage, channel, title, content, scheduled_date
       # stage phải thuộc ["Teaser", "Launch", "CTA"]
       # channel phải thuộc expected_channels
       # Tổng số bài ≥ 10
       # Trả về (True, "") hoặc (False, "lý do")

3. Validate output của Agent 3 (Brand Auditor):
   def validate_agent3_output(data: dict) -> tuple[bool, str]:
       # Kiểm tra có key: audited_posts, overall_score, violations
       # overall_score phải là số từ 0-100
       # audited_posts phải là list
       # Trả về (True, "") hoặc (False, "lý do")
```

---

## ⚡ BƯỚC 3: XÂY DỰNG 3 AI AGENT

### Prompt 3.1 – BaseAgent (Lớp trừu tượng)

```
Viết file `agents/base_agent.py` – lớp trừu tượng cho tất cả AI Agent trong hệ thống Marketing AI.

Yêu cầu:
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str, llm_client, system_prompt_path: str):
        """
        name: tên Agent (vd: "Market Intelligence Agent")
        llm_client: instance của LLMClient
        system_prompt_path: đường dẫn file .txt chứa system prompt
        """
        self.name = name
        self.llm_client = llm_client
        self.system_prompt = self._load_system_prompt(system_prompt_path)
        self.logs = []  # Lưu log quá trình xử lý
    
    def _load_system_prompt(self, path: str) -> str:
        # Đọc file system prompt
    
    def log(self, message: str):
        # Thêm log với timestamp: "[HH:MM:SS] Agent_Name: message"
        # Cũng print ra console
    
    @abstractmethod
    def build_user_prompt(self, input_data: dict) -> str:
        # Mỗi Agent tự xây dựng user prompt từ dữ liệu đầu vào
        pass
    
    @abstractmethod
    def validate_output(self, output: dict) -> tuple[bool, str]:
        # Mỗi Agent tự validate output
        pass
    
    def execute(self, input_data: dict) -> dict:
        """
        Luồng thực thi chung cho mọi Agent:
        1. Log "Bắt đầu xử lý..."
        2. Gọi build_user_prompt(input_data) để tạo prompt
        3. Gọi llm_client.call_json(system_prompt, user_prompt)
        4. Gọi validate_output(result)
        5. Nếu không hợp lệ → raise ValueError
        6. Log "Hoàn thành!"
        7. Trả về result (dict)
        """
```

### Prompt 3.2 – Agent 1: Market & Competitor Intelligence

```
Viết 2 file cho Agent 1 của hệ thống Marketing AI:

=== FILE 1: prompts/agent1_system.txt ===
Viết system prompt bằng tiếng Việt, nội dung:
- Gán vai trò: "Bạn là chuyên gia phân tích thị trường Marketing với 15 năm kinh nghiệm tại Việt Nam."
- Nhiệm vụ: Đọc Campaign Brief, phân tích sâu để xác định:
  1. Target Persona (chân dung khách hàng chi tiết: độ tuổi, giới tính, thu nhập, thói quen, nỗi lo)
  2. Pain Points (≥ 5 nỗi đau/vấn đề của khách hàng mục tiêu)
  3. USP – Unique Selling Proposition (điểm bán hàng độc nhất của sản phẩm)
  4. Communication Angles (3-5 góc tiếp cận truyền thông hấp dẫn)
- Yêu cầu suy luận theo Chain-of-Thought: phân tích từng bước trước khi kết luận
- BẮT BUỘC trả về kết quả ĐÚNG JSON format sau (không thêm text hay markdown):
{
  "target_persona": {
    "age_range": "...",
    "gender": "...",
    "income_level": "...",
    "lifestyle": "...",
    "concerns": ["...", "..."]
  },
  "pain_points": ["nỗi đau 1", "nỗi đau 2", "nỗi đau 3", "nỗi đau 4", "nỗi đau 5"],
  "usp": "điểm độc nhất của sản phẩm",
  "communication_angles": [
    {"angle_name": "tên góc", "description": "mô tả cách tiếp cận", "emotional_hook": "điểm chạm cảm xúc"},
    ...
  ],
  "market_summary": "tóm tắt phân tích thị trường 3-5 câu"
}

=== FILE 2: agents/market_intelligence.py ===
Viết class MarketIntelligenceAgent kế thừa BaseAgent:

class MarketIntelligenceAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__(
            name="Market Intelligence Agent",
            llm_client=llm_client,
            system_prompt_path="prompts/agent1_system.txt"
        )
    
    def build_user_prompt(self, input_data: dict) -> str:
        """
        input_data chứa Campaign Brief:
        - campaign_name, product_name, target_audience, budget, channels, start_date, end_date
        
        Xây dựng user prompt dạng:
        "Hãy phân tích Campaign Brief sau đây:
         - Tên chiến dịch: {campaign_name}
         - Sản phẩm: {product_name}
         - Đối tượng mục tiêu: {target_audience}
         - Ngân sách: {budget}
         - Kênh truyền thông: {channels}
         - Thời gian: {start_date} đến {end_date}
         
         Hãy phân tích chi tiết và trả về JSON theo format đã quy định."
        """
    
    def validate_output(self, output: dict) -> tuple[bool, str]:
        # Dùng validate_agent1_output từ json_parser.py
```

### Prompt 3.3 – Agent 2: Campaign Copywriter

```
Viết 2 file cho Agent 2 của hệ thống Marketing AI:

=== FILE 1: prompts/agent2_system.txt ===
Viết system prompt bằng tiếng Việt, nội dung:
- Gán vai trò: "Bạn là Copywriter chuyên nghiệp với 10 năm kinh nghiệm viết content Marketing cho thị trường Việt Nam."
- Nhiệm vụ: Nhận dữ liệu phân tích từ chuyên gia thị trường (Agent 1), kết hợp với Campaign Brief để sinh ra kịch bản bài đăng theo 3 giai đoạn phễu tâm lý:

  **Giai đoạn 1 – Teaser (Gây tò mò):** 
  - Mục đích: Tạo nhận thức vấn đề, KHÔNG bán hàng, KHÔNG nhắc tên sản phẩm
  - Nội dung: Chia sẻ nỗi đau, đặt câu hỏi tương tác, số liệu gây sốc
  - Chiếm khoảng 30% tổng số bài
  
  **Giai đoạn 2 – Launch (Giải pháp):**
  - Mục đích: Giới thiệu sản phẩm là lời giải cho vấn đề ở GĐ1
  - Nội dung: Demo tính năng, so sánh before/after, testimonial, bằng chứng
  - Chiếm khoảng 40% tổng số bài
  
  **Giai đoạn 3 – CTA (Chốt sale):**
  - Mục đích: Thúc đẩy mua hàng
  - Nội dung: Ưu đãi giới hạn, countdown, link đăng ký, lời kêu gọi hành động
  - Chiếm khoảng 30% tổng số bài

- Tối ưu nội dung cho từng kênh:
  - Facebook: emoji nhiều, ngắn gọn, có CTA cuối bài, hashtag
  - LinkedIn: chuyên nghiệp, insight, dài hơn, ít emoji
  - Email: subject line hấp dẫn, cấu trúc rõ ràng, có nút CTA

- BẮT BUỘC trả về JSON:
{
  "posts": [
    {
      "stage": "Teaser|Launch|CTA",
      "channel": "Facebook|LinkedIn|Email",
      "scheduled_date": "YYYY-MM-DD",
      "title": "tiêu đề bài viết",
      "content": "nội dung bài viết đầy đủ",
      "hashtags": ["hashtag1", "hashtag2"]
    },
    ...
  ],
  "content_strategy_summary": "tóm tắt chiến lược nội dung 3-5 câu"
}

- Phân bổ scheduled_date đều trong khoảng start_date → end_date
- Tổng số bài: 20-30 bài tùy theo thời lượng chiến dịch

=== FILE 2: agents/campaign_copywriter.py ===
Viết class CampaignCopywriterAgent kế thừa BaseAgent:

class CampaignCopywriterAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__(
            name="Campaign Copywriter Agent",
            llm_client=llm_client,
            system_prompt_path="prompts/agent2_system.txt"
        )
    
    def build_user_prompt(self, input_data: dict) -> str:
        """
        input_data chứa:
        - brief: dict (Campaign Brief gốc từ DB)
        - insights: dict (output từ Agent 1)
        
        Xây dựng user prompt kết hợp cả Brief + Insight:
        "Dựa trên phân tích thị trường sau đây:
         - Target Persona: {insights.target_persona}
         - Pain Points: {insights.pain_points}
         - USP: {insights.usp}
         - Góc truyền thông: {insights.communication_angles}
         
         Kết hợp với Campaign Brief:
         - Sản phẩm: {brief.product_name}
         - Kênh: {brief.channels}
         - Thời gian: {brief.start_date} đến {brief.end_date}
         
         Hãy tạo kịch bản nội dung 20-30 bài đăng theo phễu 3 giai đoạn."
        """
    
    def validate_output(self, output: dict) -> tuple[bool, str]:
        # Dùng validate_agent2_output từ json_parser.py
```

### Prompt 3.4 – Agent 3: Brand Compliance Auditor

```
Viết 2 file cho Agent 3 của hệ thống Marketing AI:

=== FILE 1: prompts/agent3_system.txt ===
Viết system prompt bằng tiếng Việt, nội dung:
- Gán vai trò: "Bạn là Chuyên gia Kiểm duyệt Thương hiệu (Brand Guardian) với kinh nghiệm 12 năm trong ngành truyền thông Việt Nam."
- Nhiệm vụ: Nhận danh sách bài đăng từ Copywriter + Bộ quy tắc thương hiệu (Brand Rules) để:

  1. **Kiểm tra từ cấm (Forbidden Words):** Quét mỗi bài viết, phát hiện mọi từ/cụm từ nằm trong danh sách cấm.
  2. **Kiểm tra từ bắt buộc (Mandatory Keywords):** Đảm bảo mỗi bài viết có chứa ít nhất 1 từ khóa bắt buộc.
  3. **Kiểm tra Tone of Voice:** Đánh giá xem tone giọng bài viết có phù hợp với tone quy định không (Chuyên nghiệp / Trẻ trung / Trang trọng / Gần gũi).
  4. **Kiểm tra Luật Quảng cáo Việt Nam:** Phát hiện các cụm từ vi phạm pháp luật như "tốt nhất", "số 1", "cam kết 100%", "không có tác dụng phụ"...
  5. **Chấm điểm tuân thủ (Compliance Score):** Mỗi bài viết được chấm điểm 0-100:
     - 90-100: Xuất sắc, không vi phạm
     - 70-89: Tốt, vi phạm nhẹ
     - 50-69: Trung bình, cần sửa
     - Dưới 50: Không đạt, cần viết lại
  6. **Đề xuất sửa đổi:** Với mỗi vi phạm, đưa ra gợi ý sửa cụ thể.

- BẮT BUỘC trả về JSON:
{
  "overall_score": 85,
  "total_violations": 3,
  "summary": "tóm tắt kết quả kiểm duyệt",
  "audited_posts": [
    {
      "post_index": 0,
      "original_title": "...",
      "compliance_score": 90,
      "violations": [
        {
          "type": "forbidden_word|missing_keyword|wrong_tone|legal_violation",
          "detail": "mô tả vi phạm cụ thể",
          "found_text": "đoạn text vi phạm",
          "suggestion": "gợi ý sửa"
        }
      ],
      "status": "passed|needs_revision|failed"
    },
    ...
  ]
}

=== FILE 2: agents/brand_auditor.py ===
Viết class BrandComplianceAuditorAgent kế thừa BaseAgent:

class BrandComplianceAuditorAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__(
            name="Brand Compliance Auditor Agent",
            llm_client=llm_client,
            system_prompt_path="prompts/agent3_system.txt"
        )
    
    def build_user_prompt(self, input_data: dict) -> str:
        """
        input_data chứa:
        - posts: list[dict] (output từ Agent 2, danh sách bài viết)
        - brand_rules: dict (Brand Rules từ DB)
          - forbidden_words: list
          - mandatory_keywords: list
          - tone_of_voice: str
        
        Xây dựng user prompt:
        "Hãy kiểm duyệt danh sách bài viết sau theo Bộ quy tắc thương hiệu:
         
         === BỘ QUY TẮC THƯƠNG HIỆU ===
         - Từ cấm: {brand_rules.forbidden_words}
         - Từ bắt buộc: {brand_rules.mandatory_keywords}
         - Tone giọng: {brand_rules.tone_of_voice}
         
         === DANH SÁCH BÀI VIẾT CẦN KIỂM DUYỆT ===
         Bài 1: {title} - {content}
         Bài 2: ...
         
         Hãy kiểm duyệt từng bài và trả về JSON."
        """
    
    def validate_output(self, output: dict) -> tuple[bool, str]:
        # Dùng validate_agent3_output từ json_parser.py
```

### Prompt 3.5 – Agent Orchestrator (Bộ điều phối)

```
Viết file `agents/orchestrator.py` – bộ điều phối pipeline 3 AI Agent.

Yêu cầu:
class AgentOrchestrator:
    def __init__(self, llm_client, db_connection):
        self.llm_client = llm_client
        self.db = db_connection
        self.agent1 = MarketIntelligenceAgent(llm_client)
        self.agent2 = CampaignCopywriterAgent(llm_client)
        self.agent3 = BrandComplianceAuditorAgent(llm_client)
        self.logs = []           # Tổng hợp log từ cả 3 Agent
        self.current_step = 0    # 0: chưa bắt đầu, 1/2/3: đang chạy Agent nào
        self.checkpoint = {}     # Lưu kết quả trung gian để resume nếu lỗi
    
    def run_pipeline(self, campaign_id: int, brand_rule_id: int, 
                     progress_callback=None) -> dict:
        """
        Chạy pipeline đầy đủ 3 Agent tuần tự.
        
        progress_callback: hàm callback(step, total_steps, message) 
                          để UI cập nhật tiến trình real-time
        
        Luồng xử lý:
        1. Đọc Campaign Brief từ DB (bảng campaigns, theo campaign_id)
        2. Đọc Brand Rules từ DB (bảng brand_rules, theo brand_rule_id)
        3. Cập nhật campaign status → "In-Progress"
        4. callback(1, 3, "🔍 Agent 1 đang phân tích thị trường...")
        
        5. === CHẠY AGENT 1 ===
           input1 = brief_data
           output1 = agent1.execute(input1)  → insights
           Lưu checkpoint["agent1_output"] = output1
           callback(1, 3, "✅ Agent 1 hoàn thành! Đã phân tích insight.")
        
        6. === CHẠY AGENT 2 ===
           input2 = {"brief": brief_data, "insights": output1}
           output2 = agent2.execute(input2)  → posts
           Lưu checkpoint["agent2_output"] = output2
           callback(2, 3, "✅ Agent 2 hoàn thành! Đã tạo {len(posts)} bài viết.")
        
        7. === CHẠY AGENT 3 ===
           input3 = {"posts": output2["posts"], "brand_rules": brand_rules_data}
           output3 = agent3.execute(input3)  → audit_report
           Lưu checkpoint["agent3_output"] = output3
           callback(3, 3, "✅ Agent 3 hoàn thành! Điểm tuân thủ: {score}/100")
        
        8. === LƯU KẾT QUẢ VÀO DATABASE ===
           - INSERT vào bảng campaign_posts (tất cả bài viết)
           - INSERT vào bảng audit_logs (kết quả kiểm duyệt)
           - UPDATE campaign status phù hợp
        
        9. Trả về dict chứa toàn bộ kết quả:
           {
             "insights": output1,
             "posts": output2,
             "audit_report": output3,
             "total_posts": ...,
             "overall_score": ...,
             "logs": self.logs
           }
        
        Xử lý lỗi:
        - Nếu Agent nào lỗi → log lỗi, lưu checkpoint, raise exception
        - Campaign status → "Draft" (rollback nếu lỗi)
        - Không xóa checkpoint để có thể resume
        """
    
    def get_logs(self) -> list[str]:
        """Trả về tất cả log từ cả 3 Agent, sắp xếp theo thời gian."""
        return self.agent1.logs + self.agent2.logs + self.agent3.logs
```

---

## ⚡ BƯỚC 4: XÂY DỰNG GIAO DIỆN STREAMLIT – TRANG CHÍNH & SIDEBAR

### Prompt 4.1 – Entry point & Sidebar

```
Viết file `ui/app.py` – trang chính của ứng dụng Streamlit cho hệ thống Marketing AI.

Yêu cầu:
1. Cấu hình trang:
   st.set_page_config(
       page_title="Marketing AI Campaign Manager",
       page_icon="🚀",
       layout="wide",
       initial_sidebar_state="expanded"
   )

2. Sidebar gồm:
   - Logo/tiêu đề app: "🚀 Marketing AI"
   - Subtitle: "Quản trị Chiến dịch Marketing tích hợp AI Multi-Agent"
   - Divider
   - Menu navigation (dùng st.radio hoặc option_menu):
     📋 Quản lý Chiến dịch
     🛡️ Quy tắc Thương hiệu  
     🤖 Chạy AI Pipeline
     📅 Content Calendar
     📤 Xuất bản & Báo cáo
   - Divider
   - Thông tin phiên bản, trạng thái DB (Connected/Disconnected)

3. Trang chính (Dashboard):
   - Hiển thị thống kê tổng quan:
     - Số chiến dịch (theo từng status)
     - Số bài viết đã tạo
     - Số bộ Brand Rules
     - Điểm tuân thủ trung bình
   - Dùng st.metric() cho 4 KPI card
   - Biểu đồ phân bổ chiến dịch theo status (plotly pie chart)
   - Danh sách 5 chiến dịch gần nhất (st.dataframe)

4. Thiết kế UI đẹp:
   - Custom CSS cho sidebar (màu gradient xanh dương - tím)
   - Card style cho KPI metrics
   - Font đẹp, spacing thoáng
   - Responsive layout (dùng st.columns)

5. Kết nối database: gọi init_database() khi app khởi động.
```

---

## ⚡ BƯỚC 5: TRANG QUẢN LÝ CHIẾN DỊCH

### Prompt 5.1 – CRUD Chiến dịch

```
Viết file `ui/pages/1_campaigns.py` – trang Quản lý Chiến dịch cho Streamlit.

Yêu cầu chức năng:
1. **FORM TẠO MỚI CHIẾN DỊCH** (có thể dùng st.form hoặc st.expander):
   - Tên chiến dịch (text_input, required)
   - Tên sản phẩm/dịch vụ (text_input, required)
   - Đối tượng mục tiêu (text_area – mô tả chi tiết)
   - Ngân sách dự kiến (text_input)
   - Kênh xuất bản (multiselect: Facebook, LinkedIn, Email)
   - Ngày bắt đầu (date_input)
   - Ngày kết thúc (date_input, validate ≥ ngày bắt đầu)
   - Nút "Tạo chiến dịch" → gọi create_campaign() → st.success()

2. **DANH SÁCH CHIẾN DỊCH** (st.dataframe hoặc custom cards):
   - Hiển thị: Tên, Sản phẩm, Status (badge màu), Ngày tạo
   - Status badge:
     - Draft → 🟡 màu vàng
     - In-Progress → 🔵 màu xanh dương
     - Approved → 🟢 màu xanh lá
     - Completed → ⚪ màu xám
   - Mỗi dòng có nút: [Xem chi tiết] [Sửa] [Xóa]

3. **FORM CHỈNH SỬA** (hiện khi bấm Sửa):
   - Điền sẵn dữ liệu hiện tại
   - Chỉ cho sửa khi status = "Draft"
   - Nút "Lưu thay đổi" → gọi update_campaign()

4. **XÓA CHIẾN DỊCH:**
   - Confirm dialog: "Bạn có chắc muốn xóa chiến dịch '{name}'? Tất cả bài viết liên quan sẽ bị xóa."
   - Chỉ cho xóa khi status = "Draft"
   - Gọi delete_campaign() → st.success()

5. **XEM CHI TIẾT:** (st.expander hoặc dialog)
   - Hiển thị đầy đủ Brief
   - Nếu đã chạy AI: hiển thị số bài viết, điểm tuân thủ
   - Nút "Chạy AI" → chuyển sang trang Run AI Pipeline

Thiết kế UI:
- Dùng st.columns để chia layout 2 cột (form bên trái, danh sách bên phải)
- Tab: "Tạo mới" | "Danh sách" 
- Search/filter theo tên hoặc status
```

---

## ⚡ BƯỚC 6: TRANG QUẢN LÝ BRAND RULES

### Prompt 6.1 – CRUD Brand Rules

```
Viết file `ui/pages/2_brand_rules.py` – trang Quản lý Quy tắc Thương hiệu.

Yêu cầu:
1. **FORM TẠO BỘ QUY TẮC MỚI:**
   - Tên bộ quy tắc (text_input, vd: "Quy tắc ngành Dược phẩm")
   - Ngành hàng (selectbox: Dược phẩm, Tài chính, Công nghệ, Thực phẩm, Mỹ phẩm, Khác)
   - Từ cấm – Forbidden Words (text_area, mỗi từ 1 dòng hoặc phân tách bằng dấu phẩy)
     - Ví dụ mặc định: "tốt nhất, số 1, cam kết 100%, không tác dụng phụ, hoàn tiền nếu không hiệu quả"
   - Từ bắt buộc – Mandatory Keywords (text_area)
     - Ví dụ: tên thương hiệu, slogan bắt buộc
   - Tone of Voice (selectbox: Chuyên nghiệp, Trẻ trung, Trang trọng, Gần gũi, Hài hước)
   - Nút "Lưu quy tắc"

2. **DANH SÁCH BỘ QUY TẮC:**
   - Card hiển thị: Tên, Ngành, Tone, Số từ cấm, Ngày tạo
   - Nút [Sửa] [Xóa] [Xem chi tiết]
   - Khi Xem chi tiết: hiển thị đầy đủ danh sách từ cấm, từ bắt buộc dạng tag/chip

3. **DỮ LIỆU MẪU:** Nút "Tạo bộ quy tắc mẫu" tự điền sẵn 1 bộ quy tắc demo:
   - Tên: "Quy tắc Quảng cáo Việt Nam"
   - Từ cấm: ["tốt nhất", "số 1", "cam kết 100%", "duy nhất", "không tác dụng phụ", "chữa khỏi", "triệt để"]
   - Từ bắt buộc: ["[Tên thương hiệu]"]
   - Tone: "Chuyên nghiệp"
```

---

## ⚡ BƯỚC 7: TRANG CHẠY AI PIPELINE

### Prompt 7.1 – Giao diện chạy 3 Agent

```
Viết file `ui/pages/3_run_ai.py` – trang Chạy AI Multi-Agent Pipeline.

Đây là trang QUAN TRỌNG NHẤT của phần mềm, cần thiết kế đẹp và trực quan.

Yêu cầu:
1. **CHỌN CHIẾN DỊCH & BRAND RULES:**
   - Dropdown chọn chiến dịch (chỉ hiện campaign có status = "Draft")
   - Dropdown chọn bộ Brand Rules để áp dụng
   - Hiển thị tóm tắt Brief của campaign đã chọn
   - Nút lớn "🚀 Chạy AI Pipeline" (disabled nếu chưa chọn đủ)

2. **HIỂN THỊ TIẾN TRÌNH REAL-TIME:**
   Khi bấm "Chạy AI Pipeline", hiển thị:
   
   a. Progress bar tổng (0% → 33% → 66% → 100%)
   
   b. 3 khối Agent hiển thị theo dạng timeline/stepper:
   
   ┌─────────────────────────────────────────┐
   │ ✅ AGENT 1: Market Intelligence         │ 
   │ Trạng thái: Hoàn thành (45 giây)       │
   │ Kết quả: 5 pain points, 4 angles       │
   └─────────────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ 🔄 AGENT 2: Campaign Copywriter        │ ← đang chạy (spinner)
   │ Trạng thái: Đang tạo nội dung...       │
   │ ...                                     │
   └─────────────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ ⏳ AGENT 3: Brand Auditor              │ ← chưa chạy (mờ)
   │ Trạng thái: Đang chờ...                │
   └─────────────────────────────────────────┘

   c. Vùng Agent Logs (st.expander hoặc st.text_area readonly):
      - Hiển thị log real-time theo timestamp
      - Scroll tự động xuống dòng mới nhất

3. **KẾT QUẢ SAU KHI HOÀN THÀNH:**
   - st.balloons() celebration
   - Metric cards: Tổng bài viết | Điểm tuân thủ | Số vi phạm | Thời gian xử lý
   - Bảng tóm tắt bài viết theo giai đoạn:
     | Giai đoạn | Facebook | LinkedIn | Email | Tổng |
   - Nút "📅 Xem Content Calendar" → chuyển trang
   - Nút "🔄 Chạy lại" → reset và chạy lại pipeline

4. **XỬ LÝ LỖI:**
   - Nếu lỗi: hiển thị st.error() với thông báo rõ ràng
   - Nút "Thử lại" 
   - Hiển thị log lỗi chi tiết trong expander

Lưu ý kỹ thuật Streamlit:
- Dùng st.status() hoặc st.empty() + placeholder để cập nhật UI
- Dùng threading hoặc st.spinner() cho loading
- Lưu kết quả vào st.session_state để không mất khi rerun
```

---

## ⚡ BƯỚC 8: TRANG CONTENT CALENDAR & XUẤT BẢN

### Prompt 8.1 – Content Calendar

```
Viết file `ui/pages/4_calendar.py` – trang Content Calendar cho hệ thống Marketing AI.

Yêu cầu:
1. **CHỌN CHIẾN DỊCH:** Dropdown chọn campaign (chỉ hiện campaign có bài viết)

2. **CALENDAR VIEW:**
   - Hiển thị lịch bài đăng theo dạng bảng/grid theo ngày
   - Mỗi ô ngày hiển thị số bài viết trong ngày đó
   - Color code theo giai đoạn:
     - Teaser → 🟡 Vàng
     - Launch → 🔵 Xanh dương  
     - CTA → 🟢 Xanh lá
   - Color code theo status:
     - Pending → viền cam
     - Approved → viền xanh
     - Rejected → viền đỏ

3. **DANH SÁCH BÀI VIẾT** (bên dưới calendar):
   - Filter theo: Giai đoạn (All/Teaser/Launch/CTA), Kênh, Status
   - Mỗi bài viết hiển thị dạng card:
     ┌───────────────────────────────────────────────┐
     │ [Teaser] [Facebook]              📅 2026-10-05│
     │ Tiêu đề: Bạn có biết 80% phụ nữ...          │
     │ ──────────────────────────────────────────────│
     │ Nội dung bài viết hiển thị tóm tắt 3 dòng...│
     │ ──────────────────────────────────────────────│
     │ 🏆 Compliance: 92/100  │  Vi phạm: 0        │
     │ [✅ Duyệt] [❌ Từ chối] [✏️ Sửa] [📋 Copy] │
     └───────────────────────────────────────────────┘

4. **XEM CHI TIẾT BÀI VIẾT** (khi click vào card):
   - Hiển thị đầy đủ nội dung
   - Hiển thị kết quả kiểm duyệt:
     - Compliance Score (gauge chart)
     - Danh sách vi phạm (nếu có)
     - Gợi ý sửa đổi
   - Hashtags

5. **CHỨC NĂNG PHÊ DUYỆT (Human-in-the-loop):**
   - Nút "✅ Duyệt" → update_post_status(post_id, "Approved")
   - Nút "❌ Từ chối" → hiện text_input nhập lý do → update_post_status(post_id, "Rejected")
   - Nút "✏️ Chỉnh sửa nội dung" → mở text_area chỉnh sửa → update_post_content()
   - Nút "🔄 Regenerate" → gọi lại Agent 2 chỉ cho bài này
   - Nút "📋 Copy" → copy nội dung vào clipboard (dùng JS injection)
   - Nút "Duyệt tất cả" → duyệt tất cả bài đang Pending

6. **THỐNG KÊ:**
   - Pie chart phân bổ theo status (Pending/Approved/Rejected)
   - Bar chart phân bổ theo stage
   - Điểm tuân thủ trung bình
```

### Prompt 8.2 – Xuất file Excel & Gửi Email

```
Viết 2 file cho chức năng Xuất bản:

=== FILE 1: utils/export_excel.py ===
Viết module xuất Content Calendar ra file Excel (.xlsx):

def export_campaign_to_excel(campaign: dict, posts: list[dict], audit_logs: list[dict]) -> bytes:
    """
    Tạo file Excel với 3 sheet:
    
    Sheet 1 – "Tổng quan chiến dịch":
    - Tên chiến dịch, sản phẩm, đối tượng, ngân sách
    - Thời gian, kênh, status
    - Thống kê: tổng bài, điểm tuân thủ TB
    
    Sheet 2 – "Lịch bài đăng":
    - Bảng gồm: STT, Ngày đăng, Giai đoạn, Kênh, Tiêu đề, Nội dung, Hashtags, Status, Điểm
    - Định dạng: header đậm, zebra striping, auto-width columns
    - Conditional formatting: 
      - Score ≥ 90 → nền xanh
      - Score 70-89 → nền vàng
      - Score < 70 → nền đỏ
    
    Sheet 3 – "Báo cáo kiểm duyệt":
    - Bảng gồm: STT, Tiêu đề bài, Điểm, Số vi phạm, Chi tiết vi phạm, Gợi ý sửa
    
    Trả về bytes (để Streamlit download).
    """

Sử dụng openpyxl để tạo file, có format đẹp chuyên nghiệp.

=== FILE 2: ui/pages/5_export.py ===
Viết trang Streamlit cho chức năng Xuất bản & Báo cáo:

1. **Chọn chiến dịch** (dropdown, chỉ hiện campaign có bài đã Approved)

2. **Xuất file Excel:**
   - Nút "📥 Tải xuống Excel" → gọi export_campaign_to_excel() 
   - Dùng st.download_button() để tải file

3. **Gửi Email (SMTP):**
   - Form nhập: email người nhận, tiêu đề email
   - Preview nội dung email trước khi gửi
   - Nút "📧 Gửi Email" → gọi module gửi email qua SMTP
   - Hiển thị kết quả: thành công/thất bại

4. **1-Click Copy:**
   - Chọn bài viết từ dropdown
   - Hiển thị preview nội dung
   - Nút "📋 Copy nội dung" → copy vào clipboard

5. **Báo cáo tổng hợp:**
   - Biểu đồ phân bổ bài viết theo giai đoạn & kênh
   - Biểu đồ điểm tuân thủ
   - Timeline lịch đăng bài
```

---

## ⚡ BƯỚC BỔ SUNG: CHẠY ỨNG DỤNG & TEST

### Prompt 9.1 – File chạy chính

```
Viết file `run.py` ở thư mục gốc – script chạy ứng dụng:

import subprocess
import sys
import os

def main():
    # 1. Kiểm tra file .env tồn tại, nếu không → copy từ .env.example
    # 2. Kiểm tra GEMINI_API_KEY đã được cấu hình chưa
    # 3. Tự động tạo database nếu chưa có
    # 4. Chạy lệnh: streamlit run ui/app.py --server.port 8501
    # 5. Tự mở browser tại http://localhost:8501

if __name__ == "__main__":
    main()
```

### Prompt 9.2 – Dữ liệu Demo

```
Viết file `seed_demo_data.py` – tạo dữ liệu demo để test ứng dụng:

1. Tạo 2 chiến dịch mẫu:
   - Chiến dịch 1: "Ra mắt Sữa rửa mặt XYZ" (status: Draft)
     - Sản phẩm: Sữa rửa mặt XYZ Salicylic Acid 2%
     - Đối tượng: Nữ 18-25 tuổi, da dầu mụn, sinh viên
     - Kênh: Facebook, Email
     - Thời gian: 01/10 – 21/10/2026
   
   - Chiến dịch 2: "Khuyến mãi Black Friday" (status: Draft)
     - Sản phẩm: Combo chăm sóc da 3 bước
     - Đối tượng: Nữ 20-35 tuổi, quan tâm skincare
     - Kênh: Facebook, LinkedIn
     - Thời gian: 15/11 – 30/11/2026

2. Tạo 2 bộ Brand Rules mẫu:
   - Bộ 1: "Quy tắc ngành Mỹ phẩm"
     - Từ cấm: ["tốt nhất", "số 1", "cam kết 100%", "không tác dụng phụ", "chữa khỏi", "triệt để", "vĩnh viễn"]
     - Từ bắt buộc: ["XYZ Cosmetics"]
     - Tone: "Trẻ trung"
   
   - Bộ 2: "Quy tắc Quảng cáo chung Việt Nam"
     - Từ cấm: ["tốt nhất", "số 1", "duy nhất", "cam kết", "đảm bảo 100%"]
     - Từ bắt buộc: []
     - Tone: "Chuyên nghiệp"

3. In ra "✅ Đã tạo dữ liệu demo thành công!"
```

---

## 📋 CHECKLIST KIỂM TRA SAU KHI LÀM XONG

| STT | Chức năng | Kiểm tra | ✅ |
|-----|-----------|----------|-----|
| 1 | Database | 4 bảng được tạo, CRUD hoạt động | ☐ |
| 2 | Gemini API | Gọi API thành công, retry khi lỗi | ☐ |
| 3 | Agent 1 | Phân tích Brief → trả về JSON insight | ☐ |
| 4 | Agent 2 | Nhận insight → sinh 20-30 bài viết JSON | ☐ |
| 5 | Agent 3 | Kiểm duyệt bài → chấm điểm Compliance | ☐ |
| 6 | Orchestrator | Pipeline 3 Agent chạy tuần tự, lưu DB | ☐ |
| 7 | UI - Dashboard | Thống kê KPI, biểu đồ | ☐ |
| 8 | UI - Campaigns | CRUD chiến dịch đầy đủ | ☐ |
| 9 | UI - Brand Rules | CRUD bộ quy tắc | ☐ |
| 10 | UI - Run AI | Chạy pipeline, hiển thị log real-time | ☐ |
| 11 | UI - Calendar | Lịch bài đăng, duyệt/từ chối | ☐ |
| 12 | Xuất Excel | File Excel 3 sheet, format đẹp | ☐ |
| 13 | Copy bài | 1-Click Copy hoạt động | ☐ |
| 14 | Demo | Chạy demo 2 chiến dịch mẫu thành công | ☐ |

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **Thứ tự bắt buộc:** Luôn làm theo thứ tự Bước 0 → 8. Không nhảy bước.
2. **Test từng bước:** Sau mỗi bước, chạy thử và kiểm tra trước khi sang bước tiếp.
3. **API Key:** Cần có Google Gemini API key (miễn phí tại https://aistudio.google.com).
4. **Bảo mật:** KHÔNG commit file `.env` lên Git. Đã có `.gitignore`.
5. **Ngôn ngữ:** Giao diện và nội dung AI sinh ra đều bằng **tiếng Việt**.
6. **Khi đưa prompt cho AI:** Copy NGUYÊN VĂN prompt ở trên, KHÔNG sửa đổi. Nếu AI hỏi thêm thì trả lời theo ngữ cảnh dự án.

---

*File này được tạo tự động dựa trên tài liệu thiết kế đề tài.*
*Cập nhật lần cuối: 2026-10-09*
