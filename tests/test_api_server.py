"""
Test suite cho toàn bộ REST API Endpoints trong api_server.py.
Kiểm thử tính năng từ Health Check, Chiến dịch, Lịch đăng, Tuân thủ, AI Jobs, Pipeline đến Đối tác và Admin.
"""

import pytest


def test_health_check(client):
    """Kiểm tra endpoint /api/health trả về 200 và trạng thái healthy."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "db_type" in data
    assert "engine" in data


def test_campaigns_crud_and_transition(client):
    """Kiểm tra toàn bộ vòng đời chiến dịch: Tạo -> Sửa -> Chuyển trạng thái -> Xóa."""
    # 1. Tạo chiến dịch mới
    new_camp = {
        "name": "Chiến Dịch Test Tự Động 2026",
        "product_name": "Sản Phẩm Test Pro",
        "target_audience": "Người dùng đam mê công nghệ",
        "budget": 25000.0,
        "channels": ["Facebook", "TikTok"],
        "start_date": "2026-12-01",
        "end_date": "2026-12-31"
    }
    create_res = client.post("/api/campaigns", json=new_camp)
    assert create_res.status_code == 200
    created_id = create_res.json()["id"]
    assert created_id > 0

    # 2. Lấy danh sách kiểm tra có chiến dịch vừa tạo
    list_res = client.get("/api/campaigns")
    assert list_res.status_code == 200
    camps = list_res.json()
    assert any(c["id"] == created_id for c in camps)

    # 3. Cập nhật thông tin chiến dịch
    update_res = client.put(f"/api/campaigns/{created_id}", json={
        "name": "Chiến Dịch Test Đã Cập Nhật",
        "budget": 30000.0
    })
    assert update_res.status_code == 200

    # 4. Chuyển trạng thái chiến dịch (Transition)
    trans_res = client.post(f"/api/campaigns/{created_id}/transition", json={
        "to_status": "In-Progress"
    })
    assert trans_res.status_code == 200
    assert trans_res.json()["new_status"] == "In-Progress"

    # 5. Xóa chiến dịch
    del_res = client.delete(f"/api/campaigns/{created_id}")
    assert del_res.status_code == 200


def test_objectives_and_budget_lines(client):
    """Kiểm tra thêm mục tiêu SMART và dòng ngân sách vào chiến dịch."""
    camps_res = client.get("/api/campaigns")
    camps = camps_res.json()
    assert len(camps) > 0
    camp_id = camps[0]["id"]

    # Thêm mục tiêu SMART
    obj_data = {
        "objective_type": "awareness",
        "metric": "Reach",
        "target_value": 500000.0,
        "unit": "người",
        "deadline": "2026-12-31"
    }
    obj_res = client.post(f"/api/campaigns/{camp_id}/objectives", json=obj_data)
    assert obj_res.status_code == 200

    # Lấy danh sách mục tiêu
    get_objs = client.get(f"/api/campaigns/{camp_id}/objectives")
    assert get_objs.status_code == 200
    assert isinstance(get_objs.json(), list)

    # Thêm dòng ngân sách
    b_data = {
        "category": "Media",
        "channel": "TikTok Ads",
        "planned_amount": 5000.0,
        "note": "Ngân sách chạy Spark Ads"
    }
    b_res = client.post(f"/api/campaigns/{camp_id}/budget-lines", json=b_data)
    assert b_res.status_code == 200

    # Lấy danh sách ngân sách
    get_b = client.get(f"/api/campaigns/{camp_id}/budget-lines")
    assert get_b.status_code == 200
    assert isinstance(get_b.json(), list)


def test_posts_and_calendar_workflow(client):
    """Kiểm tra quản lý bài viết: Lấy danh sách, cập nhật nội dung, duyệt và xuất bản."""
    posts_res = client.get("/api/posts")
    assert posts_res.status_code == 200
    posts = posts_res.json()
    assert len(posts) > 0
    post_id = posts[0]["id"]

    # Cập nhật trạng thái duyệt bài
    patch_res = client.patch(f"/api/posts/{post_id}", json={
        "status": "Approved",
        "compliance_score": 98
    })
    assert patch_res.status_code == 200

    # Xuất bản bài viết
    pub_res = client.post(f"/api/posts/{post_id}/publish", json={
        "published_url": "https://tiktok.com/@auravietnam/video/74839201"
    })
    assert pub_res.status_code == 200
    assert pub_res.json()["success"] is True


def test_brand_rules_and_compliance_check(client):
    """Kiểm tra quản trị bộ quy tắc thương hiệu & chạy kiểm duyệt tuân thủ 3 lớp."""
    rules_res = client.get("/api/brand-rules")
    assert rules_res.status_code == 200
    rules = rules_res.json()
    assert len(rules) > 0

    posts = client.get("/api/posts").json()
    post_id = posts[0]["id"]

    # Chạy kiểm duyệt tuân thủ cho bài viết
    chk_res = client.post(f"/api/posts/{post_id}/compliance-check")
    assert chk_res.status_code == 200
    chk_data = chk_res.json()
    assert "score" in chk_data
    assert "risk_level" in chk_data
    assert "violations" in chk_data


def test_ai_jobs_dynamic_input_analysis(client):
    """
    Kiểm tra AI phân tích SWOT chính xác theo dữ liệu người dùng nhập (không dùng text cứng).
    Ví dụ: Thông số điện thoại cao cấp (Harman/Kardon, Leica 300MP, giá 35 triệu, chip 0.02nm).
    """
    payload = {
        "agent": "market_intel",
        "type": "swot",
        "campaign_id": 1,
        "data": {
            "strengths": "loa kết hợp harman/kardon, camera 300MB đầu tiên trên thế giới cùng bộ lọc leica, màn hình 5000nits, chip Xpring tiến trình 0.02nm",
            "weaknesses": "giá bán cao 35.000.000 cho bản thấp nhất",
            "opportunities": "xu hướng bùng nổ trong phân khúc điện thoại flagship",
            "threats": "cạnh tranh gay gắt với các dòng điện thoại cao cấp vừa ra trên thị trường"
        }
    }
    res = client.post("/api/ai-jobs", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "succeeded"
    output = data["output"]

    # Phải phản ánh đúng dữ liệu người dùng đã nhập
    assert "harman/kardon" in output.lower() or "leica" in output.lower()
    assert "35.000.000" in output
    assert "flagship" in output.lower()
    assert "MA TRẬN PHỐI HỢP CHIẾN LƯỢC" in output
    assert "CHIẾN LƯỢC S-O" in output
    assert "CHIẾN LƯỢC W-O" in output


def test_ai_jobs_competitors_and_stp(client):
    """Kiểm tra AI phân tích đối thủ cạnh tranh và phân khúc STP & Persona."""
    # Competitor analysis
    comp_res = client.post("/api/ai-jobs", json={
        "agent": "market_intel",
        "type": "competitor",
        "data": [
            {
                "name": "Flagship Pro X",
                "positioning": "Nhiếp ảnh chân dung",
                "channels": "TikTok, YouTube",
                "strengths": "Thương hiệu lâu đời, độ nhận diện cao",
                "weaknesses": "Thời lượng pin yếu, giá đắt"
            }
        ]
    })
    assert comp_res.status_code == 200
    comp_output = comp_res.json()["output"]
    assert "Flagship Pro X" in comp_output
    assert "KHOẢNG TRỐNG THỊ TRƯỜNG" in comp_output

    # STP analysis
    stp_res = client.post("/api/ai-jobs", json={
        "agent": "market_intel",
        "type": "stp",
        "data": {
            "stp": {
                "segment": "Giới trẻ yêu công nghệ 18-35 tuổi",
                "target": "Content Creators & Nhiếp ảnh gia di động",
                "positioning": "Siêu phẩm flagship nhiếp ảnh đỉnh cao"
            },
            "personas": [
                {
                    "name": "Hoàng Nam",
                    "role": "Reviewer Công Nghệ",
                    "income": "30 triệu/tháng",
                    "painPoints": "Điện thoại hiện tại quay video nhanh nóng máy",
                    "channels": "YouTube, TikTok"
                }
            ]
        }
    })
    assert stp_res.status_code == 200
    stp_output = stp_res.json()["output"]
    assert "Hoàng Nam" in stp_output
    assert "Content Creators" in stp_output


def test_ai_pipeline_execution(client):
    """Kiểm tra chạy toàn bộ quy trình AI 3 Agent (Pipeline Orchestrator)."""
    camps = client.get("/api/campaigns").json()
    camp_id = camps[0]["id"]

    res = client.post(f"/api/campaigns/{camp_id}/run-pipeline", json={"brand_rule_id": 1})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["posts_count"] > 0
    assert "overall_score" in data
    assert "logs" in data
    assert len(data["logs"]) > 0


def test_performance_metrics_and_partners(client):
    """Kiểm tra nhập số liệu hiệu suất thực tế & quản lý đối tác KOL/KOC."""
    camps = client.get("/api/campaigns").json()
    camp_id = camps[0]["id"]

    # Nhập số liệu hiệu suất
    perf_data = {
        "channel": "TikTok",
        "metric_date": "2026-11-15",
        "views": 150000,
        "reach": 120000,
        "engagements": 18500,
        "clicks": 4200,
        "orders": 310,
        "gmv": 108500000.0,
        "ad_spend": 15000000.0
    }
    perf_res = client.post(f"/api/campaigns/{camp_id}/performance", json=perf_data)
    assert perf_res.status_code == 200

    # Đọc lại số liệu
    get_perf = client.get(f"/api/campaigns/{camp_id}/performance")
    assert get_perf.status_code == 200
    assert isinstance(get_perf.json(), list)

    # Quản lý đối tác
    new_partner = {
        "partner_type": "KOL",
        "name": "TechReviewer Việt Nam",
        "platform": "YouTube",
        "follower_count": 850000,
        "contact_email": "booking@techreviewer.vn",
        "fee_per_post": 15000000.0
    }
    part_res = client.post("/api/partners", json=new_partner)
    assert part_res.status_code == 200

    get_part = client.get("/api/partners")
    assert get_part.status_code == 200
    partners = get_part.json()
    assert any(p["name"] == "TechReviewer Việt Nam" for p in partners)


def test_users_and_authentication(client):
    """Kiểm tra quản lý người dùng và xác thực đăng nhập."""
    # Lấy danh sách users
    users_res = client.get("/api/users")
    assert users_res.status_code == 200
    users = users_res.json()
    assert len(users) > 0

    # Đăng nhập với tài khoản hợp lệ
    login_res = client.post("/api/auth/login", json={
        "username": "nhan",
        "password": "nhan1903"
    })
    assert login_res.status_code == 200
    res_data = login_res.json()
    assert res_data["success"] is True
    user = res_data["user"]
    assert user["username"] == "nhan"
    assert "role" in user


def test_products_and_claims(client):
    """Kiểm tra quản lý sản phẩm Dược mỹ phẩm và phê duyệt Claims (Legal Reviewer)."""
    prods_res = client.get("/api/products")
    assert prods_res.status_code == 200
    prods = prods_res.json()
    assert len(prods) > 0
    prod_id = prods[0]["id"]

    # Tạo claim mới
    claim_res = client.post(f"/api/products/{prod_id}/claims", json={
        "claim_text": "Phục hồi 95% hàng rào bảo vệ da sau 14 ngày kiểm nghiệm lâm sàng",
        "claim_type": "efficacy",
        "valid_until": "2027-12-31"
    })
    assert claim_res.status_code == 200
    claim_id = claim_res.json()["id"]

    # Phê duyệt claim
    appr_res = client.post(f"/api/claims/{claim_id}/approve", json={
        "approved_by": "Dr. Nguyễn Văn A (Chief Medical Officer)"
    })
    assert appr_res.status_code == 200
    assert appr_res.json()["success"] is True


def test_admin_config_and_cache(client):
    """Kiểm tra quản trị hệ thống: Đọc/Lưu API Keys và Xóa bộ nhớ đệm."""
    # Đọc cấu hình keys
    cfg_res = client.get("/api/config/api-keys")
    assert cfg_res.status_code == 200
    assert "gemini_api_key_configured" in cfg_res.json()

    # Lưu cấu hình keys
    save_res = client.post("/api/config/api-keys", json={
        "gemini_api_key": "AIzaSyD_TEST_AUTOMATED_RUNNER_KEY"
    })
    assert save_res.status_code == 200

    # Xóa cache
    cache_res = client.post("/api/admin/clear-cache")
    assert cache_res.status_code == 200
    assert cache_res.json()["success"] is True
