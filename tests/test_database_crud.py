"""
Unit tests trực tiếp cho tầng Database CRUD (database/crud.py) và Connection Pool.
Kiểm tra tính toàn vẹn dữ liệu, các truy vấn SELECT, INSERT, UPDATE, DELETE và cơ chế Dual-Database (PostgreSQL / SQLite).
"""

import pytest
import database.crud as crud
from database.connection import get_connection, is_postgres_available


def test_database_connection(db_conn):
    """Kiểm tra kết nối cơ sở dữ liệu hoạt động và trả về đối tượng hợp lệ."""
    assert db_conn is not None


def test_crud_campaign_lifecycle(db_conn):
    """Kiểm tra tạo, đọc, sửa trạng thái, và xóa chiến dịch trong database."""
    # 1. Tạo campaign
    camp_id = crud.create_campaign(
        db_conn,
        name="Chiến Dịch CRUD Test",
        product_name="Serum Test B5",
        target_audience="Khách hàng da dầu",
        budget="5000",
        channels="TikTok, Facebook",
        start_date="2026-11-01",
        end_date="2026-11-30"
    )
    assert camp_id > 0

    # 2. Đọc campaign theo ID
    camp = crud.get_campaign_by_id(db_conn, camp_id)
    assert camp is not None
    assert camp["name"] == "Chiến Dịch CRUD Test"
    assert camp["status"] == "Draft"

    # 3. Cập nhật trạng thái campaign
    ok = crud.update_campaign_status(db_conn, camp_id, "Approved")
    assert ok is True
    updated = crud.get_campaign_by_id(db_conn, camp_id)
    assert updated["status"] == "Approved"

    # 4. Xóa campaign
    del_ok = crud.delete_campaign(db_conn, camp_id)
    assert del_ok is True
    deleted = crud.get_campaign_by_id(db_conn, camp_id)
    assert deleted is None


def test_crud_posts_bulk_and_status(db_conn):
    """Kiểm tra tạo hàng loạt bài viết, cập nhật trạng thái và xuất bản."""
    camps = crud.get_all_campaigns(db_conn)
    assert len(camps) > 0
    camp_id = camps[0]["id"]

    posts_to_create = [
        {
            "campaign_id": camp_id,
            "stage": "Teaser",
            "channel": "Facebook",
            "title": "Bài viết test 1",
            "content": "Nội dung bài viết test 1",
            "hashtags": ["#Test1", "#Aura"],
            "scheduled_date": "2026-11-20"
        },
        {
            "campaign_id": camp_id,
            "stage": "Launch",
            "channel": "TikTok",
            "title": "Bài viết test 2",
            "content": "Nội dung bài viết test 2",
            "hashtags": ["#Test2"],
            "scheduled_date": "2026-11-22"
        }
    ]

    created_ids = crud.create_posts_bulk(db_conn, posts_to_create)
    assert len(created_ids) == 2

    # Cập nhật trạng thái bài 1
    crud.update_post_status(db_conn, created_ids[0], "Approved")
    post1 = crud.get_post_by_id(db_conn, created_ids[0])
    assert post1["status"] == "Approved"

    # Đánh dấu bài 1 đã xuất bản
    crud.mark_post_as_published(db_conn, created_ids[0], published_url="https://facebook.com/post/999")
    post1_pub = crud.get_post_by_id(db_conn, created_ids[0])
    assert post1_pub["status"] == "Published"
    assert post1_pub["published_url"] == "https://facebook.com/post/999"


def test_crud_brand_rules(db_conn):
    """Kiểm tra tạo, đọc và cập nhật bộ quy tắc thương hiệu."""
    rule_id = crud.create_brand_rule(
        db_conn,
        rule_name="Quy Tắc Test 2026",
        forbidden_words=["tuyệt đối 100%", "chữa khỏi hoàn toàn"],
        mandatory_keywords=["đã kiểm nghiệm", "an toàn"],
        tone_of_voice="Chuyên gia khoa học"
    )
    assert rule_id > 0

    rule = crud.get_brand_rule_by_id(db_conn, rule_id)
    assert rule is not None
    assert rule["rule_name"] == "Quy Tắc Test 2026"
    assert "tuyệt đối 100%" in rule["forbidden_words"]

    # Cập nhật rule
    crud.update_brand_rule(db_conn, rule_id, tone_of_voice="Chuyên gia da liễu")
    updated_rule = crud.get_brand_rule_by_id(db_conn, rule_id)
    assert updated_rule["tone_of_voice"] == "Chuyên gia da liễu"

    # Dọn dẹp
    crud.delete_brand_rule(db_conn, rule_id)


def test_crud_user_authentication(db_conn):
    """Kiểm tra mã hóa mật khẩu, tạo user, xác thực và đổi role."""
    test_user = "test_agent_user"
    test_pass = "TestPassword@2026"

    # Tạo user
    uid = crud.create_user(
        db_conn,
        username=test_user,
        password=test_pass,
        full_name="User Kiểm Thử Tự Động",
        role="Content Creator",
        email="test_agent@aura.vn"
    )
    assert uid > 0

    # Xác thực mật khẩu đúng
    auth_user = crud.authenticate_user(db_conn, test_user, test_pass)
    assert auth_user is not None
    assert auth_user["username"] == test_user

    # Xác thực mật khẩu sai -> phải None
    bad_auth = crud.authenticate_user(db_conn, test_user, "WrongPassword")
    assert bad_auth is None

    # Cập nhật role
    crud.update_user_role(db_conn, uid, "Marketing Lead")
    all_users = crud.get_all_users(db_conn)
    u_found = next((u for u in all_users if u["id"] == uid), None)
    assert u_found["role"] == "Marketing Lead"

    # Xóa user
    crud.delete_user(db_conn, uid)


def test_crud_performance_and_partners(db_conn):
    """Kiểm tra upsert số liệu hiệu suất và đối tác."""
    camps = crud.get_all_campaigns(db_conn)
    camp_id = camps[0]["id"]

    # Upsert metrics
    crud.upsert_performance_metrics(
        db_conn,
        campaign_id=camp_id,
        channel="Instagram",
        metric_date="2026-11-16",
        reach=55000,
        engagements=6200,
        clicks=1800,
        orders=95,
        gmv=33250000.0,
        ad_spend=7000000.0
    )

    perf = crud.get_campaign_performance(db_conn, camp_id)
    assert isinstance(perf, list)
    assert len(perf) > 0

    # Thêm đối tác
    pid = crud.create_partner(
        db_conn,
        partner_type="KOC",
        name="Làn Da Dịu Lành",
        platform="TikTok",
        follower_count=120000,
        fee_per_post=3000000.0
    )
    assert pid > 0
    partners = crud.get_all_partners(db_conn)
    assert any(p["name"] == "Làn Da Dịu Lành" for p in partners)
