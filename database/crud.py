"""
Module CRUD hỗ trợ Dual-Database (PostgreSQL & SQLite tự động chuyển đổi).
Nhận kết nối (conn) làm tham số đầu tiên, tự động thích ứng cú pháp và kiểu dữ liệu.
"""

import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from database.connection import get_db_type

try:
    from psycopg.types.json import Json
except ImportError:
    Json = None


def _is_pg(conn) -> bool:
    return get_db_type(conn) == "postgres"


def _row_to_dict(row) -> Dict[str, Any]:
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    return dict(row)


def _parse_violations(val: Any) -> list:
    if val is None:
        return []
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        try:
            return json.loads(val)
        except Exception:
            return []
    return []


# ============================================================
# === CAMPAIGNS ===
# ============================================================

def create_campaign(conn, name: str, product_name: str,
                    target_audience: str = "", budget: str = "",
                    channels: str = "", start_date: str = "",
                    end_date: str = "") -> int:
    """Tạo chiến dịch mới (hỗ trợ cả PostgreSQL & SQLite)."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
            cursor.execute(
                """INSERT INTO campaigns 
                   (name, product_name, target_audience, budget, channels, start_date, end_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (name, product_name, target_audience, budget, channels, start_date, end_date)
            )
            row = cursor.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]
        else:
            now = datetime.now().isoformat()
            cursor.execute(
                """INSERT INTO campaigns 
                   (name, product_name, target_audience, budget, channels, start_date, end_date, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, product_name, target_audience, budget, channels, start_date, end_date, now, now)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def get_all_campaigns(conn) -> List[Dict[str, Any]]:
    """Lấy danh sách tất cả chiến dịch."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        cursor.close()


def get_campaign_by_id(conn, campaign_id: int) -> Optional[Dict[str, Any]]:
    """Lấy chi tiết 1 chiến dịch theo ID."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM campaigns WHERE id = {param_ph}", (campaign_id,))
        row = cursor.fetchone()
        return _row_to_dict(row)
    finally:
        cursor.close()


def update_campaign(conn, campaign_id: int, **kwargs) -> bool:
    """Cập nhật thông tin chiến dịch."""
    if not kwargs:
        return False
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    
    set_clause = ", ".join(f"{k} = {param_ph}" for k in kwargs.keys())
    values = list(kwargs.values()) + [campaign_id]
    
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE campaigns SET {set_clause} WHERE id = {param_ph}", values)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def update_campaign_status(conn, campaign_id: int, new_status: str) -> bool:
    """Cập nhật trạng thái chiến dịch."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE campaigns SET status = {param_ph} WHERE id = {param_ph}", (new_status, campaign_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def delete_campaign(conn, campaign_id: int) -> bool:
    """Xóa chiến dịch theo ID."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM campaigns WHERE id = {param_ph}", (campaign_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


# ============================================================
# === CAMPAIGN_POSTS ===
# ============================================================

def create_post(conn, campaign_id: int, stage: str,
                channel: str, title: str = "", content: str = "",
                scheduled_date: str = "") -> int:
    """Tạo 1 bài viết mới cho chiến dịch."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
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
        else:
            cursor.execute(
                """INSERT INTO campaign_posts 
                   (campaign_id, stage, channel, title, content, scheduled_date)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (campaign_id, stage, channel, title, content, scheduled_date if scheduled_date else None)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def create_posts_bulk(conn, posts: List[Dict[str, Any]]) -> List[int]:
    """Tạo nhiều bài viết cùng lúc."""
    is_pg = _is_pg(conn)
    ids = []
    cursor = conn.cursor()
    try:
        for post in posts:
            scheduled = post.get("scheduled_date")
            title = post.get("title", "")
            content = post.get("content", "")
            channel = post.get("channel", "Facebook")
            stage = post.get("stage", "Teaser")
            camp_id = post["campaign_id"]
            media_url = post.get("media_url")
            
            if is_pg:
                cursor.execute(
                    """INSERT INTO campaign_posts 
                       (campaign_id, stage, channel, title, content, scheduled_date, media_url)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)
                       RETURNING id""",
                    (camp_id, stage, channel, title, content, scheduled if scheduled else None, media_url)
                )
                row = cursor.fetchone()
                ids.append(row["id"] if isinstance(row, dict) else row[0])
            else:
                cursor.execute(
                    """INSERT INTO campaign_posts 
                       (campaign_id, stage, channel, title, content, scheduled_date, media_url)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (camp_id, stage, channel, title, content, scheduled if scheduled else None, media_url)
                )
                ids.append(cursor.lastrowid)
        conn.commit()
        return ids
    finally:
        cursor.close()


def get_posts_by_campaign(conn, campaign_id: int) -> List[Dict[str, Any]]:
    """Lấy danh sách bài viết theo chiến dịch."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT * FROM campaign_posts WHERE campaign_id = {param_ph} ORDER BY scheduled_date ASC, id ASC",
            (campaign_id,)
        )
        rows = cursor.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        cursor.close()


def get_all_posts(conn) -> List[Dict[str, Any]]:
    """Lấy danh sách tất cả bài viết trong toàn bộ hệ thống."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM campaign_posts ORDER BY scheduled_date ASC, id ASC")
        rows = cursor.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        cursor.close()


def get_post_by_id(conn, post_id: int) -> Optional[Dict[str, Any]]:
    """Lấy thông tin 1 bài viết theo ID."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM campaign_posts WHERE id = {param_ph}", (post_id,))
        row = cursor.fetchone()
        return _row_to_dict(row)
    finally:
        cursor.close()


def update_post_content(conn, post_id: int, title: str, content: str, media_url: str = None) -> bool:
    """Cập nhật tiêu đề, nội dung và hình ảnh bài viết."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        if media_url is not None:
            cursor.execute(
                f"UPDATE campaign_posts SET title = {param_ph}, content = {param_ph}, media_url = {param_ph} WHERE id = {param_ph}",
                (title, content, media_url, post_id)
            )
        else:
            cursor.execute(
                f"UPDATE campaign_posts SET title = {param_ph}, content = {param_ph} WHERE id = {param_ph}",
                (title, content, post_id)
            )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def update_post_media(conn, post_id: int, media_url: str) -> bool:
    """Cập nhật hình ảnh bài viết từ Thư viện ảnh hoặc Upload mới."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"UPDATE campaign_posts SET media_url = {param_ph} WHERE id = {param_ph}",
            (media_url, post_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def update_post_status(conn, post_id: int, new_status: str) -> bool:
    """Cập nhật trạng thái bài viết (Pending/Approved/Rejected/Published)."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"UPDATE campaign_posts SET status = {param_ph} WHERE id = {param_ph}",
            (new_status, post_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def mark_post_as_published(conn, post_id: int, published_url: str = "") -> bool:
    """Đánh dấu bài viết đã xuất bản tự động thành công lên mạng xã hội kèm thời gian và link bài."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    now_expr = "CURRENT_TIMESTAMP" if is_pg else "datetime('now')"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"UPDATE campaign_posts SET status = 'Published', published_at = {now_expr}, published_url = {param_ph} WHERE id = {param_ph}",
            (published_url, post_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def delete_posts_by_campaign(conn, campaign_id: int) -> bool:
    """Xóa tất cả bài viết thuộc 1 chiến dịch."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM campaign_posts WHERE campaign_id = {param_ph}", (campaign_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


# ============================================================
# === BRAND_RULES ===
# ============================================================

def create_brand_rule(conn, rule_name: str,
                      forbidden_words: str = "", mandatory_keywords: str = "",
                      tone_of_voice: str = "", industry: str = "") -> int:
    """Tạo bộ quy tắc thương hiệu mới."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
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
        else:
            cursor.execute(
                """INSERT INTO brand_rules 
                   (rule_name, forbidden_words, mandatory_keywords, tone_of_voice)
                   VALUES (?, ?, ?, ?)""",
                (rule_name, forbidden_words, mandatory_keywords, tone_of_voice)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def get_all_brand_rules(conn) -> List[Dict[str, Any]]:
    """Lấy danh sách tất cả bộ quy tắc thương hiệu."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM brand_rules ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        cursor.close()


def get_brand_rule_by_id(conn, rule_id: int) -> Optional[Dict[str, Any]]:
    """Lấy thông tin 1 bộ quy tắc theo ID."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM brand_rules WHERE id = {param_ph}", (rule_id,))
        row = cursor.fetchone()
        return _row_to_dict(row)
    finally:
        cursor.close()


def update_brand_rule(conn, rule_id: int, **kwargs) -> bool:
    """Cập nhật bộ quy tắc thương hiệu."""
    if not kwargs:
        return False
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    set_clause = ", ".join(f"{k} = {param_ph}" for k in kwargs.keys())
    values = list(kwargs.values()) + [rule_id]
    
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE brand_rules SET {set_clause} WHERE id = {param_ph}", values)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def delete_brand_rule(conn, rule_id: int) -> bool:
    """Xóa bộ quy tắc thương hiệu."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM brand_rules WHERE id = {param_ph}", (rule_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


# ============================================================
# === AUDIT_LOGS ===
# ============================================================

def create_audit_log(conn, post_id: int, rule_id: int,
                     compliance_score: float, violations_json: list,
                     suggestions: str = "") -> int:
    """Tạo log kiểm duyệt cho 1 bài viết."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
            v_val = Json(violations_json) if Json else json.dumps(violations_json, ensure_ascii=False)
            cursor.execute(
                """INSERT INTO audit_logs 
                   (post_id, rule_id, compliance_score, violations_json, suggestions)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id""",
                (post_id, rule_id, compliance_score, v_val, suggestions)
            )
            row = cursor.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]
        else:
            cursor.execute(
                """INSERT INTO audit_logs 
                   (post_id, rule_id, compliance_score, violations_json, suggestions)
                   VALUES (?, ?, ?, ?, ?)""",
                (post_id, rule_id, compliance_score, json.dumps(violations_json, ensure_ascii=False), suggestions)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def create_audit_logs_bulk(conn, logs: List[Dict[str, Any]]) -> List[int]:
    """Tạo nhiều audit log cùng lúc."""
    is_pg = _is_pg(conn)
    ids = []
    cursor = conn.cursor()
    try:
        for log in logs:
            violations = log.get("violations_json", [])
            post_id = log["post_id"]
            rule_id = log["rule_id"]
            score = log["compliance_score"]
            sug = log.get("suggestions", "")
            
            if is_pg:
                v_val = Json(violations) if Json else json.dumps(violations, ensure_ascii=False)
                cursor.execute(
                    """INSERT INTO audit_logs 
                       (post_id, rule_id, compliance_score, violations_json, suggestions)
                       VALUES (%s, %s, %s, %s, %s)
                       RETURNING id""",
                    (post_id, rule_id, score, v_val, sug)
                )
                row = cursor.fetchone()
                ids.append(row["id"] if isinstance(row, dict) else row[0])
            else:
                cursor.execute(
                    """INSERT INTO audit_logs 
                       (post_id, rule_id, compliance_score, violations_json, suggestions)
                       VALUES (?, ?, ?, ?, ?)""",
                    (post_id, rule_id, score, json.dumps(violations, ensure_ascii=False), sug)
                )
                ids.append(cursor.lastrowid)
        conn.commit()
        return ids
    finally:
        cursor.close()


def get_audit_by_post(conn, post_id: int) -> Optional[Dict[str, Any]]:
    """Lấy kết quả kiểm duyệt mới nhất của 1 bài viết."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT * FROM audit_logs WHERE post_id = {param_ph} ORDER BY audited_at DESC LIMIT 1",
            (post_id,)
        )
        row = cursor.fetchone()
        if row:
            d = _row_to_dict(row)
            d["violations_json"] = _parse_violations(d.get("violations_json"))
            return d
        return None
    finally:
        cursor.close()


def get_audits_by_campaign(conn, campaign_id: int) -> List[Dict[str, Any]]:
    """Lấy tất cả kết quả kiểm duyệt của 1 chiến dịch."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""SELECT al.*, cp.title as post_title, cp.stage, cp.channel
               FROM audit_logs al
               JOIN campaign_posts cp ON al.post_id = cp.id
               WHERE cp.campaign_id = {param_ph}
               ORDER BY al.audited_at DESC""",
            (campaign_id,)
        )
        rows = cursor.fetchall()
        results = []
        for r in rows:
            d = _row_to_dict(r)
            d["violations_json"] = _parse_violations(d.get("violations_json"))
            results.append(d)
        return results
    finally:
        cursor.close()


def get_all_audits(conn) -> List[Dict[str, Any]]:
    """Lấy tất cả kết quả kiểm duyệt trong toàn bộ hệ thống."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM audit_logs ORDER BY id ASC")
        rows = cursor.fetchall()
        results = []
        for r in rows:
            d = _row_to_dict(r)
            d["violations_json"] = _parse_violations(d.get("violations_json"))
            results.append(d)
        return results
    finally:
        cursor.close()


# ============================================================
# === USERS & AUTHENTICATION ===
# ============================================================

def hash_password(password: str) -> str:
    """Hash mật khẩu bằng SHA-256 an toàn."""
    import hashlib
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(conn, username: str, password: str, full_name: str,
                email: str = "", role: str = "Content Creator") -> int:
    """Tạo người dùng mới."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    try:
        if is_pg:
            cursor.execute(
                """INSERT INTO users (username, password_hash, full_name, email, role, is_active)
                   VALUES (%s, %s, %s, %s, %s, TRUE)
                   RETURNING id""",
                (username.strip(), pwd_hash, full_name.strip(), email.strip(), role)
            )
            row = cursor.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]
        else:
            cursor.execute(
                """INSERT INTO users (username, password_hash, full_name, email, role, is_active)
                   VALUES (?, ?, ?, ?, ?, 1)""",
                (username.strip(), pwd_hash, full_name.strip(), email.strip(), role)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def authenticate_user(conn, username: str, password: str) -> Optional[Dict[str, Any]]:
    """Xác thực đăng nhập theo username và password."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    try:
        cursor.execute(
            f"SELECT * FROM users WHERE username = {param_ph} AND password_hash = {param_ph}",
            (username.strip(), pwd_hash)
        )
        row = cursor.fetchone()
        if row:
            d = _row_to_dict(row)
            if d.get("is_active"):
                return d
        return None
    finally:
        cursor.close()


def get_all_users(conn) -> List[Dict[str, Any]]:
    """Lấy danh sách tất cả người dùng hệ thống."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, full_name, email, role, is_active, created_at FROM users ORDER BY id ASC")
        rows = cursor.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        cursor.close()


def update_user_role(conn, user_id: int, new_role: str) -> bool:
    """Chỉ Admin mới có quyền đổi vai trò (role) của người dùng."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"UPDATE users SET role = {param_ph} WHERE id = {param_ph}",
            (new_role, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def update_user_status(conn, user_id: int, is_active: bool) -> bool:
    """Kích hoạt hoặc khóa tài khoản người dùng."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"UPDATE users SET is_active = {param_ph} WHERE id = {param_ph}",
            (is_active, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def delete_user(conn, user_id: int) -> bool:
    """Xóa người dùng (chỉ Admin thực hiện)."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM users WHERE id = {param_ph}", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
