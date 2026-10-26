"""
Bộ điều phối AgentOrchestrator – quản lý và thực thi Pipeline 3 AI Agent tuần tự.
Cập nhật trạng thái database, phát tiến trình real-time cho UI, lưu checkpoint và xử lý lỗi.
"""

import logging
from typing import Dict, Any, Callable
from agents.market_intelligence import MarketIntelligenceAgent
from agents.campaign_copywriter import CampaignCopywriterAgent
from agents.brand_auditor import BrandComplianceAuditorAgent
from database.crud import (
    get_campaign_by_id,
    get_brand_rule_by_id,
    update_campaign_status,
    create_posts_bulk,
    create_audit_logs_bulk,
    delete_posts_by_campaign
)

logger = logging.getLogger("AgentOrchestrator")


class AgentOrchestrator:
    def __init__(self, llm_client, db_connection):
        self.llm_client = llm_client
        self.conn = db_connection
        self.agent1 = MarketIntelligenceAgent(llm_client)
        self.agent2 = CampaignCopywriterAgent(llm_client)
        self.agent3 = BrandComplianceAuditorAgent(llm_client)
        self.logs = []
        self.current_step = 0
        self.checkpoint = {}

    def log(self, msg: str):
        self.logs.append(msg)
        logger.info(msg)

    def run_pipeline(self, campaign_id: int, brand_rule_id: int,
                     progress_callback: Callable[[int, int, str], None] = None) -> Dict[str, Any]:
        """
        Chạy Pipeline đầy đủ qua 3 Agent tuần tự.
        
        Args:
            campaign_id: ID chiến dịch
            brand_rule_id: ID bộ quy tắc thương hiệu
            progress_callback: Hàm callback(step, total_steps, message) cập nhật UI real-time
        
        Returns:
            Dict chứa toàn bộ kết quả insights, posts, audit_report, logs...
        """
        self.logs = []
        self.checkpoint = {}
        
        # 1. Đọc dữ liệu từ DB
        brief = get_campaign_by_id(self.conn, campaign_id)
        if not brief:
            raise ValueError(f"Không tìm thấy chiến dịch ID {campaign_id}")
            
        brand_rule = get_brand_rule_by_id(self.conn, brand_rule_id)
        if not brand_rule:
            raise ValueError(f"Không tìm thấy bộ quy tắc thương hiệu ID {brand_rule_id}")

        # 2. Cập nhật status campaign
        update_campaign_status(self.conn, campaign_id, "In-Progress")
        
        try:
            # === CHẠY AGENT 1 ===
            self.current_step = 1
            if progress_callback:
                progress_callback(1, 3, "🔍 Agent 1: Đang phân tích thị trường & khách hàng mục tiêu...")
            self.log("=== BẮT ĐẦU AGENT 1: Market Intelligence ===")
            
            insights = self.agent1.execute(brief)
            self.checkpoint["agent1_output"] = insights
            self.log("✅ Agent 1 hoàn thành thành công!")

            # === CHẠY AGENT 2 ===
            self.current_step = 2
            if progress_callback:
                progress_callback(2, 3, "✍️ Agent 2: Đang sáng tạo kịch bản 20-30 bài viết theo phễu...")
            self.log("=== BẮT ĐẦU AGENT 2: Campaign Copywriter ===")
            
            input_agent2 = {"brief": brief, "insights": insights}
            copywriter_output = self.agent2.execute(input_agent2)
            self.checkpoint["agent2_output"] = copywriter_output
            posts_list = copywriter_output.get("posts", [])

            # Tự động gán hình ảnh đẹp và phù hợp từ Thư viện Media cho từng bài viết
            try:
                from utils.media_manager import auto_assign_images
                posts_list = auto_assign_images(posts_list, brief.get("product_name", ""))
            except Exception as e_media:
                logger.warning(f"Lỗi tự động gán media: {e_media}")

            self.log(f"✅ Agent 2 hoàn thành! Đã tạo {len(posts_list)} bài đăng kèm hình ảnh minh họa.")

            # === CHẠY AGENT 3 ===
            self.current_step = 3
            if progress_callback:
                progress_callback(3, 3, "🛡️ Agent 3: Đang kiểm duyệt bài viết & chấm điểm tuân thủ...")
            self.log("=== BẮT ĐẦU AGENT 3: Brand Compliance Auditor ===")
            
            input_agent3 = {"posts": posts_list, "brand_rules": brand_rule}
            audit_report = self.agent3.execute(input_agent3)
            self.checkpoint["agent3_output"] = audit_report
            overall_score = audit_report.get("overall_score", 0)
            self.log(f"✅ Agent 3 hoàn thành! Điểm tuân thủ tổng thể: {overall_score}/100")

            # === LƯU KẾT QUẢ VÀO DATABASE ===
            if progress_callback:
                progress_callback(3, 3, "💾 Đang lưu kết quả bài đăng và audit log vào Database...")
                
            # Xóa các bài viết cũ của chiến dịch này (nếu có) trước khi chèn bài mới
            delete_posts_by_campaign(self.conn, campaign_id)
            
            # Chuẩn bị dữ liệu chèn posts (Phòng thủ kiểm tra kiểu dữ liệu an toàn)
            posts_to_insert = []
            for post in posts_list:
                if isinstance(post, dict):
                    posts_to_insert.append({
                        "campaign_id": campaign_id,
                        "stage": post.get("stage", "Teaser"),
                        "channel": post.get("channel", "Facebook"),
                        "title": post.get("title", ""),
                        "content": post.get("content", ""),
                        "hashtags": post.get("hashtags", []),
                        "scheduled_date": post.get("scheduled_date", brief.get("start_date")),
                        "media_url": post.get("media_url")
                    })
                elif isinstance(post, str):
                    posts_to_insert.append({
                        "campaign_id": campaign_id,
                        "stage": "Launch",
                        "channel": "Facebook",
                        "title": post[:40],
                        "content": post,
                        "hashtags": [],
                        "scheduled_date": brief.get("start_date")
                    })
                
            created_post_ids = create_posts_bulk(self.conn, posts_to_insert)
            
            # Khớp post_id mới với kết quả audit từ Agent 3 cho TẤT CẢ các bài đã tạo
            audited_posts = audit_report.get("audited_posts", []) if isinstance(audit_report, dict) else []
            audit_logs_to_insert = []
            
            for idx, post_id in enumerate(created_post_ids):
                audited = audited_posts[idx] if idx < len(audited_posts) else {}
                if isinstance(audited, str):
                    audited = {"violations": [], "compliance_score": 100, "suggestions": audited}
                elif not isinstance(audited, dict):
                    audited = {}

                violations = audited.get("violations", [])
                if not isinstance(violations, list):
                    violations = [violations] if violations else []

                suggestions = audited.get("suggestions")
                if not suggestions and violations:
                    sug_list = [v.get("suggestion") for v in violations if isinstance(v, dict) and v.get("suggestion")]
                    suggestions = "; ".join([str(s) for s in sug_list if s])

                comp_score = audited.get("compliance_score", 100)
                try:
                    comp_score = float(comp_score)
                except (ValueError, TypeError):
                    comp_score = 100.0

                audit_logs_to_insert.append({
                    "post_id": post_id,
                    "rule_id": brand_rule_id,
                    "compliance_score": comp_score,
                    "violations_json": violations,
                    "suggestions": str(suggestions or "")
                })
                    
            if audit_logs_to_insert:
                create_audit_logs_bulk(self.conn, audit_logs_to_insert)

            # Cập nhật trạng thái chiến dịch hoàn tất
            update_campaign_status(self.conn, campaign_id, "Approved")
            
            final_result = {
                "insights": insights,
                "posts": posts_list,
                "content_strategy_summary": copywriter_output.get("content_strategy_summary", "") if isinstance(copywriter_output, dict) else "",
                "audit_report": audit_report,
                "total_posts": len(posts_list),
                "overall_score": overall_score,
                "logs": self.get_all_logs()
            }
            return final_result

        except Exception as e:
            self.log(f"❌ Lỗi Pipeline tại bước {self.current_step}: {e}")
            update_campaign_status(self.conn, campaign_id, "Draft")
            raise e

    def get_all_logs(self) -> list:
        return self.logs + self.agent1.logs + self.agent2.logs + self.agent3.logs
