"""
Module CRUD (Create/Read/Update/Delete) cho 4 bảng của hệ thống Marketing AI với PostgreSQL.
Tất cả hàm nhận kết nối PostgreSQL (conn) làm tham số đầu tiên.
"""

import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from psycopg.types.json import Json


# ============================================================
# === CAMPAIGNS ===
# ============================================================

def create_campaign(conn, name: str, product_name: str,
                    target_audience: str = "", budget: str = "",
                    channels: str = "", start_date: str = "",
                    end_date: str = "") -> int:
    """
    Tạo chiến dịch mới.
    
    Args:
        conn: Kết nối PostgreSQL
        name: Tên chiến dịch
        product_name: Tên sản phẩm/dịch vụ
        target_audience: Mô tả đối tượng mục tiêu
        budget: Ngân sách dự kiến
        channels: Kênh xuất bản (chuỗi phân tách dấu phẩy, vd: "Facebook, LinkedIn")
        start_date: Ngày bắt đầu (YYYY-MM-DD)
        end_date: Ngày kết thúc (YYYY-MM-DD)
    
    Returns:
        int: ID (BIGINT) của chiến dịch vừa tạo
    """
    now = datetime.now()
    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO campaigns 
               (name, product_name, target_audience, budget, channels, start_date, end_date, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (name, product_name, target_audience, budget, channels, start_date, end_date, now, now)
        )
        row = cursor.fetchone()
        conn.commit()
        return row["id"] if isinstance(row, dict) else row[0]


def get_all_campaigns(conn) -> List[Dict[str, Any]]:
    """
    Lấy danh sách tất cả chiến dịch.
    
    Returns:
        List[Dict]: Danh sách chiến dịch dạng dictionary
    """
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_campaign_by_id(conn, campaign_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin chi tiết 1 chiến dịch theo ID.
    
    Args:
        campaign_id: ID chiến dịch
    
    Returns:
        Dict | None: Thông tin chiến dịch hoặc None nếu không tìm thấy
    """
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM campaigns WHERE id = %s", (campaign_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_campaign(conn, campaign_id: int, **kwargs) -> bool:
    """
    Cập nhật thông tin chiến dịch.
    
    Args:
        campaign_id: ID chiến dịch cần cập nhật
        **kwargs: Các trường cần cập nhật
    
    Returns:
        bool: True nếu cập nhật thành công
    """
    if not kwargs:
        return False
    
    kwargs["updated_at"] = datetime.now()
    set_clause = ", ".join(f"{key} = %s" for key in kwargs.keys())
    values = list(kwargs.values()) + [campaign_id]
    
    with conn.cursor() as cursor:
        cursor.execute(
            f"UPDATE campaigns SET {set_clause} WHERE id = %s",
            values
        )
        conn.commit()
        return cursor.rowcount > 0


def update_campaign_status(conn, campaign_id: int, new_status: str) -> bool:
    """
    Cập nhật trạng thái chiến dịch.
    
    Args:
        campaign_id: ID chiến dịch
        new_status: Trạng thái mới (Draft/In-Progress/Approved/Completed)
    
    Returns:
        bool: True nếu cập nhật thành công
    """
    now = datetime.now()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE campaigns SET status = %s, updated_at = %s WHERE id = %s",
            (new_status, now, campaign_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_campaign(conn, campaign_id: int) -> bool:
    """
    Xóa chiến dịch và các bài viết liên quan (CASCADE).
    
    Args:
        campaign_id: ID chiến dịch cần xóa
    
    Returns:
        bool: True nếu xóa thành công
    """
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM campaigns WHERE id = %s", (campaign_id,))
        conn.commit()
        return cursor.rowcount > 0


# ============================================================
# === CAMPAIGN_POSTS ===
# ============================================================

def create_post(conn, campaign_id: int, stage: str,
                channel: str, title: str = "", content: str = "",
                scheduled_date: str = "") -> int:
    """
    Tạo 1 bài viết mới cho chiến dịch.
    
    Args:
        campaign_id: ID chiến dịch
        stage: Giai đoạn (Teaser/Launch/CTA)
        channel: Kênh xuất bản (Facebook/LinkedIn/Email)
        title: Tiêu đề bài viết
        content: Nội dung bài viết
        scheduled_date: Ngày đăng dự kiến (YYYY-MM-DD)
    
    Returns:
        int: ID bài viết vừa tạo
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO campaign_posts 
               (campaign_id, stage, channel, title, content, scheduled_date)
               VALUES (%s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (campaign_id, stage, channel, title, content, scheduled_date if scheduled_date else None)
        )
        row = cursor.fetchone()
        conn.commit()
        return row["id"] if isinstance(row, dict) else row[0]


def create_posts_bulk(conn, posts: List[Dict[str, Any]]) -> List[int]:
    """
    Tạo nhiều bài viết cùng lúc.
    
    Args:
        posts: Danh sách dict bài viết
    
    Returns:
        List[int]: Danh sách ID vừa tạo
    """
    ids = []
    with conn.cursor() as cursor:
        for post in posts:
            scheduled = post.get("scheduled_date")
            cursor.execute(
                """INSERT INTO campaign_posts 
                   (campaign_id, stage, channel, title, content, scheduled_date)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (
                    post["campaign_id"], post["stage"], post["channel"],
                    post.get("title", ""), post["content"],
                    scheduled if scheduled else None
                )
            )
            row = cursor.fetchone()
            ids.append(row["id"] if isinstance(row, dict) else row[0])
        conn.commit()
    return ids


def get_posts_by_campaign(conn, campaign_id: int) -> List[Dict[str, Any]]:
    """
    Lấy danh sách bài viết theo chiến dịch.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM campaign_posts WHERE campaign_id = %s ORDER BY scheduled_date ASC, id ASC",
            (campaign_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_post_by_id(conn, post_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin 1 bài viết theo ID.
    """
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM campaign_posts WHERE id = %s", (post_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_post_content(conn, post_id: int, title: str, content: str) -> bool:
    """
    Cập nhật tiêu đề và nội dung bài viết.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE campaign_posts SET title = %s, content = %s WHERE id = %s",
            (title, content, post_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def update_post_status(conn, post_id: int, new_status: str) -> bool:
    """
    Cập nhật trạng thái bài viết (Pending/Approved/Rejected).
    """
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE campaign_posts SET status = %s WHERE id = %s",
            (new_status, post_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_posts_by_campaign(conn, campaign_id: int) -> bool:
    """
    Xóa tất cả bài viết thuộc 1 chiến dịch.
    """
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM campaign_posts WHERE campaign_id = %s", (campaign_id,))
        conn.commit()
        return cursor.rowcount > 0


# ============================================================
# === BRAND_RULES ===
# ============================================================

def create_brand_rule(conn, rule_name: str,
                      forbidden_words: str = "", mandatory_keywords: str = "",
                      tone_of_voice: str = "") -> int:
    """
    Tạo bộ quy tắc thương hiệu mới.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO brand_rules 
               (rule_name, forbidden_words, mandatory_keywords, tone_of_voice)
               VALUES (%s, %s, %s, %s)
               RETURNING id""",
            (rule_name, forbidden_words, mandatory_keywords, tone_of_voice)
        )
        row = cursor.fetchone()
        conn.commit()
        return row["id"] if isinstance(row, dict) else row[0]


def get_all_brand_rules(conn) -> List[Dict[str, Any]]:
    """
    Lấy danh sách tất cả bộ quy tắc thương hiệu.
    """
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM brand_rules ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_brand_rule_by_id(conn, rule_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin 1 bộ quy tắc theo ID.
    """
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM brand_rules WHERE id = %s", (rule_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_brand_rule(conn, rule_id: int, **kwargs) -> bool:
    """
    Cập nhật bộ quy tắc thương hiệu.
    """
    if not kwargs:
        return False
    
    set_clause = ", ".join(f"{key} = %s" for key in kwargs.keys())
    values = list(kwargs.values()) + [rule_id]
    
    with conn.cursor() as cursor:
        cursor.execute(
            f"UPDATE brand_rules SET {set_clause} WHERE id = %s",
            values
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_brand_rule(conn, rule_id: int) -> bool:
    """
    Xóa bộ quy tắc thương hiệu.
    """
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM brand_rules WHERE id = %s", (rule_id,))
        conn.commit()
        return cursor.rowcount > 0


# ============================================================
# === AUDIT_LOGS ===
# ============================================================

def create_audit_log(conn, post_id: int, rule_id: int,
                     compliance_score: float, violations_json: list,
                     suggestions: str = "") -> int:
    """
    Tạo log kiểm duyệt cho 1 bài viết (Lưu violations dưới dạng PostgreSQL JSONB).
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO audit_logs 
               (post_id, rule_id, compliance_score, violations_json, suggestions)
               VALUES (%s, %s, %s, %s, %s)
               RETURNING id""",
            (post_id, rule_id, compliance_score, Json(violations_json), suggestions)
        )
        row = cursor.fetchone()
        conn.commit()
        return row["id"] if isinstance(row, dict) else row[0]


def create_audit_logs_bulk(conn, logs: List[Dict[str, Any]]) -> List[int]:
    """
    Tạo nhiều audit log cùng lúc cho PostgreSQL.
    """
    ids = []
    with conn.cursor() as cursor:
        for log in logs:
            violations = log.get("violations_json", [])
            cursor.execute(
                """INSERT INTO audit_logs 
                   (post_id, rule_id, compliance_score, violations_json, suggestions)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id""",
                (
                    log["post_id"], log["rule_id"], log["compliance_score"],
                    Json(violations), log.get("suggestions", "")
                )
            )
            row = cursor.fetchone()
            ids.append(row["id"] if isinstance(row, dict) else row[0])
        conn.commit()
    return ids


def get_audit_by_post(conn, post_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy kết quả kiểm duyệt mới nhất của 1 bài viết.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM audit_logs WHERE post_id = %s ORDER BY audited_at DESC LIMIT 1",
            (post_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def get_audits_by_campaign(conn, campaign_id: int) -> List[Dict[str, Any]]:
    """
    Lấy tất cả kết quả kiểm duyệt của 1 chiến dịch.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """SELECT al.*, cp.title as post_title, cp.stage, cp.channel
               FROM audit_logs al
               JOIN campaign_posts cp ON al.post_id = cp.id
               WHERE cp.campaign_id = %s
               ORDER BY al.audited_at DESC""",
            (campaign_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
