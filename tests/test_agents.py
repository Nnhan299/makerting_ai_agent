"""
Unit tests cho tầng AI Agents và Orchestrator (agents/).
Kiểm thử bộ phân tích ma trận động (dynamic_market_analyzer), prompt builder của 3 Agent, và quy trình điều phối Pipeline.
"""

import pytest
from agents.dynamic_market_analyzer import analyze_swot, analyze_competitors, analyze_stp
from agents.market_intelligence import MarketIntelligenceAgent
from agents.campaign_copywriter import CampaignCopywriterAgent
from agents.brand_auditor import BrandComplianceAuditorAgent
from agents.orchestrator import AgentOrchestrator
from utils.llm_client import LLMClient
from database.connection import get_connection


def test_dynamic_swot_analyzer_phone_specs():
    """Kiểm tra analyze_swot phản ánh đúng 100% dữ liệu điện thoại mà người dùng đã nhập."""
    input_data = {
        "strengths": "loa harman/kardon, camera 300MP leica, màn hình 5000nits, chip Xpring 0.02nm",
        "weaknesses": "giá bán cao 35.000.000 cho bản thấp nhất",
        "opportunities": "xu hướng bùng nổ phân khúc điện thoại flagship",
        "threats": "cạnh tranh gay gắt từ các hãng điện thoại cao cấp vừa ra mắt"
    }
    result = analyze_swot(input_data)
    assert isinstance(result, str)
    assert len(result) > 500
    assert "harman/kardon" in result.lower() or "leica" in result.lower()
    assert "35.000.000" in result
    assert "flagship" in result.lower()
    assert "CHIẾN LƯỢC S-O" in result
    assert "CHIẾN LƯỢC W-O" in result
    assert "CHIẾN LƯỢC S-T" in result
    assert "CHIẾN LƯỢC W-T" in result


def test_dynamic_competitor_analyzer():
    """Kiểm tra analyze_competitors trích xuất đúng danh sách đối thủ và tính khoảng trống thị trường."""
    comps = [
        {
            "name": "Thương hiệu A",
            "positioning": "Phân khúc phổ thông",
            "channels": "TikTok",
            "strengths": "Giá rẻ, nhiều khuyến mãi",
            "weaknesses": "Chất lượng hoàn thiện kém, dịch vụ bảo hành chậm"
        },
        {
            "name": "Thương hiệu B",
            "positioning": "Phân khúc cao cấp",
            "channels": "Facebook, Showroom",
            "strengths": "Thiết kế sang trọng",
            "weaknesses": "Giá đắt, hệ điều hành khó dùng"
        }
    ]
    report = analyze_competitors(comps)
    assert "Thương hiệu A" in report
    assert "Thương hiệu B" in report
    assert "KHOẢNG TRỐNG THỊ TRƯỜNG" in report
    assert "CHIẾN THUẬT ĐỐI ĐẦU ĐỀ XUẤT" in report


def test_dynamic_stp_analyzer():
    """Kiểm tra analyze_stp xử lý đúng Segment, Target, Positioning và Persona chi tiết."""
    stp = {
        "segment": "Thành thị, 20-35 tuổi, thu nhập khá",
        "target": "Giới trẻ đam mê phong cách sống tối giản và công nghệ cao",
        "positioning": "Thiết bị định hình phong cách sống hiện đại"
    }
    personas = [
        {
            "name": "Nguyễn Mai Anh",
            "role": "Graphic Designer",
            "income": "25 triệu/tháng",
            "painPoints": "Cần màn hình chuẩn màu và pin trâu làm việc cả ngày",
            "channels": "Instagram, Behance, YouTube"
        }
    ]
    report = analyze_stp(stp, personas)
    assert "Nguyễn Mai Anh" in report
    assert "Graphic Designer" in report
    assert "phong cách sống tối giản" in report
    assert "LỘ TRÌNH TIẾP CẬN" in report


def test_agent1_market_intelligence():
    """Kiểm tra Agent 1: MarketIntelligenceAgent tạo prompt và validate output."""
    client = LLMClient()
    agent1 = MarketIntelligenceAgent(client)

    sample_brief = {
        "name": "Serum PureGlow 2026",
        "product_name": "Serum Niacinamide 10%",
        "target_audience": "Nữ 18-28 tuổi",
        "budget": "15000",
        "channels": "TikTok, Instagram",
        "start_date": "2026-10-10",
        "end_date": "2026-11-10"
    }

    user_prompt = agent1.build_user_prompt(sample_brief)
    assert "Serum PureGlow 2026" in user_prompt
    assert "Niacinamide 10%" in user_prompt

    # Test execution
    res = agent1.execute(sample_brief)
    assert isinstance(res, dict)
    assert "target_persona" in res or "usp" in res or "pain_points" in res


def test_agent2_campaign_copywriter():
    """Kiểm tra Agent 2: CampaignCopywriterAgent tạo danh sách bài viết theo phễu."""
    client = LLMClient()
    agent2 = CampaignCopywriterAgent(client)

    input_data = {
        "brief": {
            "name": "Serum PureGlow 2026",
            "product_name": "Serum Niacinamide 10%",
            "channels": "TikTok, Facebook",
            "start_date": "2026-10-10"
        },
        "insights": {
            "usp": "Phục hồi màng ẩm sinh học",
            "pain_points": ["Da khô rát", "Mụn kích ứng"]
        }
    }

    res = agent2.execute(input_data)
    assert isinstance(res, dict)
    assert "posts" in res
    assert len(res["posts"]) > 0


def test_agent3_brand_auditor():
    """Kiểm tra Agent 3: BrandComplianceAuditorAgent chấm điểm tuân thủ thương hiệu."""
    client = LLMClient()
    agent3 = BrandComplianceAuditorAgent(client)

    input_data = {
        "posts": [
            {
                "title": "Bài viết thử nghiệm",
                "content": "Sản phẩm serum cấp ẩm lành tính, đã kiểm nghiệm an toàn trên da nhạy cảm.",
                "channel": "Facebook"
            }
        ],
        "brand_rules": {
            "forbidden_words": ["cam kết 100%", "chữa khỏi hoàn toàn"],
            "mandatory_keywords": ["an toàn", "kiểm nghiệm"],
            "tone_of_voice": "Chuyên gia y khoa",
            "compliance_threshold": 90
        }
    }

    res = agent3.execute(input_data)
    assert isinstance(res, dict)
    assert "overall_score" in res
    assert res["overall_score"] >= 0


def test_agent_orchestrator_full_flow():
    """Kiểm tra AgentOrchestrator điều phối thành công trọn vẹn 3 Agent."""
    conn = get_connection()
    try:
        client = LLMClient()
        orchestrator = AgentOrchestrator(client, conn)
        # Sử dụng campaign 1 và brand_rule 1
        result = orchestrator.run_pipeline(campaign_id=1, brand_rule_id=1)
        assert isinstance(result, dict)
        assert "insights" in result
        assert "posts" in result
        assert "audit_report" in result
        assert len(orchestrator.logs) > 0
    finally:
        conn.close()
