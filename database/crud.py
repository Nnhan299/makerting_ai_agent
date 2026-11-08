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


# ============================================================
# === OBJECTIVES (SMART Goals) ===
# ============================================================

def create_objective(conn, campaign_id: int, objective_type: str, metric: str,
                     target_value: float, unit: str, deadline: str,
                     baseline_value: float = None) -> int:
    """Tạo mục tiêu SMART cho chiến dịch."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
            cursor.execute(
                """INSERT INTO objectives
                   (campaign_id, objective_type, metric, target_value, unit, deadline, baseline_value)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (campaign_id, objective_type, metric, target_value, unit, deadline, baseline_value)
            )
            row = cursor.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]
        else:
            cursor.execute(
                """INSERT INTO objectives
                   (campaign_id, objective_type, metric, target_value, unit, deadline, baseline_value)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (campaign_id, objective_type, metric, target_value, unit, deadline, baseline_value)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def get_objectives(conn, campaign_id: int) -> List[Dict[str, Any]]:
    """Lấy danh sách mục tiêu SMART theo chiến dịch."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT * FROM objectives WHERE campaign_id = {param_ph} ORDER BY created_at ASC",
            (campaign_id,)
        )
        return [_row_to_dict(r) for r in cursor.fetchall()]
    finally:
        cursor.close()


# ============================================================
# === BUDGET_LINES ===
# ============================================================

def create_budget_line(conn, campaign_id: int, category: str, channel: str,
                       planned_amount: float, note: str = '') -> int:
    """Tạo dòng ngân sách chi tiết cho chiến dịch."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
            cursor.execute(
                """INSERT INTO budget_lines
                   (campaign_id, category, channel, planned_amount, note)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id""",
                (campaign_id, category, channel, planned_amount, note)
            )
            row = cursor.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]
        else:
            cursor.execute(
                """INSERT INTO budget_lines
                   (campaign_id, category, channel, planned_amount, note)
                   VALUES (?, ?, ?, ?, ?)""",
                (campaign_id, category, channel, planned_amount, note)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def get_budget_lines(conn, campaign_id: int) -> List[Dict[str, Any]]:
    """Lấy danh sách dòng ngân sách theo chiến dịch."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT * FROM budget_lines WHERE campaign_id = {param_ph} ORDER BY created_at ASC",
            (campaign_id,)
        )
        return [_row_to_dict(r) for r in cursor.fetchall()]
    finally:
        cursor.close()


# ============================================================
# === COMPLIANCE_CHECKS ===
# ============================================================

def create_compliance_check(conn, post_id: int, score: int, risk_level: str,
                            findings: list, engine_version: str = '1.0') -> int:
    """Lưu kết quả compliance check cho bài viết."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
            findings_val = Json(findings) if Json else json.dumps(findings, ensure_ascii=False)
            cursor.execute(
                """INSERT INTO compliance_checks
                   (post_id, score, risk_level, findings, engine_version)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id""",
                (post_id, score, risk_level, findings_val, engine_version)
            )
            row = cursor.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]
        else:
            cursor.execute(
                """INSERT INTO compliance_checks
                   (post_id, score, risk_level, findings, engine_version)
                   VALUES (?, ?, ?, ?, ?)""",
                (post_id, score, risk_level, json.dumps(findings, ensure_ascii=False), engine_version)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def get_latest_compliance_check(conn, post_id: int) -> Optional[Dict[str, Any]]:
    """Lấy kết quả compliance check mới nhất của bài viết."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT * FROM compliance_checks WHERE post_id = {param_ph} ORDER BY created_at DESC LIMIT 1",
            (post_id,)
        )
        row = cursor.fetchone()
        if row:
            d = _row_to_dict(row)
            d["findings"] = _parse_violations(d.get("findings"))
            return d
        return None
    finally:
        cursor.close()


# ============================================================
# === AI_JOBS ===
# ============================================================

def create_ai_job(conn, agent: str, campaign_id: int, input_data: dict,
                  post_id: int = None, requested_by: str = None) -> int:
    """Tạo AI job mới với trạng thái queued."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
            input_val = Json(input_data) if Json else json.dumps(input_data, ensure_ascii=False)
            cursor.execute(
                """INSERT INTO ai_jobs
                   (agent, campaign_id, post_id, input, requested_by)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id""",
                (agent, campaign_id, post_id, input_val, requested_by)
            )
            row = cursor.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]
        else:
            cursor.execute(
                """INSERT INTO ai_jobs
                   (agent, campaign_id, post_id, input, requested_by)
                   VALUES (?, ?, ?, ?, ?)""",
                (agent, campaign_id, post_id, json.dumps(input_data, ensure_ascii=False), requested_by)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def update_ai_job(conn, job_id: int, status: str, output: dict = None,
                  error: str = None, tokens_in: int = 0, tokens_out: int = 0,
                  cost: float = 0) -> bool:
    """Cập nhật trạng thái và kết quả AI job."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        if is_pg:
            output_val = (Json(output) if Json else json.dumps(output, ensure_ascii=False)) if output is not None else None
            finished_expr = "now()" if status in ("succeeded", "failed", "cancelled") else "NULL"
            started_expr = "now()" if status == "running" else "started_at"
            cursor.execute(
                f"""UPDATE ai_jobs SET
                    status = {param_ph}, output = {param_ph}, error = {param_ph},
                    input_tokens = {param_ph}, output_tokens = {param_ph}, cost_usd = {param_ph},
                    started_at = CASE WHEN status = 'queued' AND {param_ph} = 'running' THEN now() ELSE started_at END,
                    finished_at = CASE WHEN {param_ph} IN ('succeeded','failed','cancelled') THEN now() ELSE finished_at END
                    WHERE id = {param_ph}""",
                (status, output_val, error, tokens_in, tokens_out, cost, status, status, job_id)
            )
        else:
            output_str = json.dumps(output, ensure_ascii=False) if output is not None else None
            cursor.execute(
                f"""UPDATE ai_jobs SET
                    status = {param_ph}, output = {param_ph}, error = {param_ph},
                    input_tokens = {param_ph}, output_tokens = {param_ph}, cost_usd = {param_ph}
                    WHERE id = {param_ph}""",
                (status, output_str, error, tokens_in, tokens_out, cost, job_id)
            )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()


def get_ai_job(conn, job_id: int) -> Optional[Dict[str, Any]]:
    """Lấy thông tin AI job theo ID."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM ai_jobs WHERE id = {param_ph}", (job_id,))
        row = cursor.fetchone()
        if row:
            d = _row_to_dict(row)
            if isinstance(d.get("input"), str):
                try:
                    d["input"] = json.loads(d["input"])
                except Exception:
                    pass
            if isinstance(d.get("output"), str):
                try:
                    d["output"] = json.loads(d["output"])
                except Exception:
                    pass
            return d
        return None
    finally:
        cursor.close()


def get_all_ai_jobs(conn) -> List[Dict[str, Any]]:
    """Lấy danh sách tất cả AI jobs."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM ai_jobs ORDER BY queued_at DESC LIMIT 100")
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = _row_to_dict(r)
            if isinstance(d.get("input"), str):
                try:
                    d["input"] = json.loads(d["input"])
                except Exception:
                    pass
            if isinstance(d.get("output"), str):
                try:
                    d["output"] = json.loads(d["output"])
                except Exception:
                    pass
            result.append(d)
        return result
    finally:
        cursor.close()


# ============================================================
# === PARTNERS ===
# ============================================================

def create_partner(conn, partner_type: str, name: str, platform: str = None,
                   follower_count: int = 0, contact_email: str = None,
                   fee_per_post: float = None) -> int:
    """Tạo đối tác mới (KOL/KOC/agency)."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
            cursor.execute(
                """INSERT INTO partners
                   (partner_type, name, platform, follower_count, contact_email, fee_per_post)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (partner_type, name, platform, follower_count, contact_email, fee_per_post)
            )
            row = cursor.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]
        else:
            cursor.execute(
                """INSERT INTO partners
                   (partner_type, name, platform, follower_count, contact_email, fee_per_post)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (partner_type, name, platform, follower_count, contact_email, fee_per_post)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def get_all_partners(conn) -> List[Dict[str, Any]]:
    """Lấy danh sách tất cả đối tác."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM partners ORDER BY created_at DESC")
        return [_row_to_dict(r) for r in cursor.fetchall()]
    finally:
        cursor.close()


# ============================================================
# === PERFORMANCE_METRICS ===
# ============================================================

def upsert_performance_metrics(conn, campaign_id: int, channel: str,
                                metric_date: str, traffic_type: str = 'organic',
                                post_id: int = None, **metrics) -> bool:
    """Cập nhật hoặc tạo mới số liệu hiệu suất (upsert theo campaign+channel+date+traffic)."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    views = metrics.get("views", 0)
    reach = metrics.get("reach", 0)
    engagements = metrics.get("engagements", 0)
    clicks = metrics.get("clicks", 0)
    orders = metrics.get("orders", 0)
    gmv = metrics.get("gmv", 0)
    spend = metrics.get("spend", 0)

    cursor = conn.cursor()
    try:
        if is_pg:
            cursor.execute(
                """INSERT INTO performance_metrics
                   (campaign_id, post_id, channel, metric_date, traffic_type,
                    views, reach, engagements, clicks, orders, gmv, spend)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT DO NOTHING""",
                (campaign_id, post_id, channel, metric_date, traffic_type,
                 views, reach, engagements, clicks, orders, gmv, spend)
            )
        else:
            cursor.execute(
                """INSERT OR IGNORE INTO performance_metrics
                   (campaign_id, post_id, channel, metric_date, traffic_type,
                    views, reach, engagements, clicks, orders, gmv, spend)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (campaign_id, post_id, channel, metric_date, traffic_type,
                 views, reach, engagements, clicks, orders, gmv, spend)
            )
        conn.commit()
        return True
    finally:
        cursor.close()


def get_campaign_performance(conn, campaign_id: int) -> List[Dict[str, Any]]:
    """Lấy danh sách số liệu hiệu suất của chiến dịch."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""SELECT * FROM performance_metrics
               WHERE campaign_id = {param_ph}
               ORDER BY metric_date DESC, channel ASC""",
            (campaign_id,)
        )
        return [_row_to_dict(r) for r in cursor.fetchall()]
    finally:
        cursor.close()


# ============================================================
# === PRODUCTS & CLAIMS (Mục 5.3 & Nguyên tắc P3) ===
# ============================================================

def get_all_products(conn) -> List[Dict[str, Any]]:
    """Lấy danh sách tất cả sản phẩm."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM products ORDER BY id ASC")
        return [_row_to_dict(r) for r in cursor.fetchall()]
    finally:
        cursor.close()


def get_product_by_id(conn, product_id: int) -> Optional[Dict[str, Any]]:
    """Lấy chi tiết sản phẩm theo ID."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM products WHERE id = {param_ph}", (product_id,))
        r = cursor.fetchone()
        return _row_to_dict(r) if r else None
    finally:
        cursor.close()


def get_claims_by_product(conn, product_id: int) -> List[Dict[str, Any]]:
    """Lấy danh sách claim của một sản phẩm."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM product_claims WHERE product_id = {param_ph} ORDER BY id ASC", (product_id,))
        return [_row_to_dict(r) for r in cursor.fetchall()]
    finally:
        cursor.close()


def create_product_claim(conn, product_id: int, claim_text: str, claim_type: str = 'benefit', valid_until: str = None) -> int:
    """Tạo claim mới cho sản phẩm ở trạng thái draft."""
    is_pg = _is_pg(conn)
    cursor = conn.cursor()
    try:
        if is_pg:
            cursor.execute(
                """INSERT INTO product_claims (product_id, claim_text, claim_type, status, valid_until, created_at)
                   VALUES (%s, %s, %s, 'draft', %s, NOW()) RETURNING id""",
                (product_id, claim_text, claim_type, valid_until)
            )
            r = cursor.fetchone()
            conn.commit()
            return r["id"] if isinstance(r, dict) else r[0]
        else:
            now = datetime.now().isoformat()
            cursor.execute(
                """INSERT INTO product_claims (product_id, claim_text, claim_type, status, valid_until, created_at)
                   VALUES (?, ?, ?, 'draft', ?, ?)""",
                (product_id, claim_text, claim_type, valid_until, now)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()


def approve_claim(conn, claim_id: int, approved_by: str = "Legal Reviewer") -> bool:
    """Duyệt claim sản phẩm (chuyển sang approved)."""
    is_pg = _is_pg(conn)
    param_ph = "%s" if is_pg else "?"
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"UPDATE product_claims SET status = 'approved', approved_by = {param_ph}, approved_at = NOW() WHERE id = {param_ph}",
            (approved_by, claim_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()

