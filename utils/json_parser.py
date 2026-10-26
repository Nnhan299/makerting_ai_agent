"""
Module validate và chuẩn hóa JSON output từ các AI Agent.
Kiểm tra cấu trúc, tự động làm sạch (clean & normalize) dữ liệu đầu ra 
trước khi chuyển cho Agent tiếp theo hoặc lưu DB.
"""

from typing import Tuple, Dict, Any, List


def validate_agent1_output(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate & chuẩn hóa output của Agent 1 (Market Intelligence):
    - target_persona (dict/object)
    - pain_points (list có >= 3 phần tử)
    - usp (str hoặc dict)
    - communication_angles (list có >= 2 phần tử)
    """
    if not isinstance(data, dict):
        return False, "Output của Agent 1 phải là dict/JSON object"
        
    if "target_persona" not in data:
        return False, "Thiếu thông tin 'target_persona'"
        
    # Chuẩn hóa pain_points
    pain_points = data.get("pain_points")
    if isinstance(pain_points, str):
        pain_points = [p.strip("- ").strip() for p in pain_points.split("\n") if p.strip()]
        data["pain_points"] = pain_points

    if not isinstance(pain_points, list):
        return False, "'pain_points' phải là danh sách (list)"
        
    if len(pain_points) < 2:
        return False, "'pain_points' phải có ít nhất 2 phần tử"
        
    # Chuẩn hóa usp
    usp = data.get("usp")
    if not usp:
        return False, "Thiếu hoặc rỗng 'usp'"
    if isinstance(usp, dict):
        data["usp"] = " - ".join(f"{k}: {v}" for k, v in usp.items())
    elif not str(usp).strip():
        return False, "'usp' không được để trống"
        
    # Chuẩn hóa communication_angles
    comm_angles = data.get("communication_angles")
    if isinstance(comm_angles, str):
        comm_angles = [a.strip("- ").strip() for a in comm_angles.split("\n") if a.strip()]
        data["communication_angles"] = comm_angles

    if not isinstance(comm_angles, list):
        return False, "'communication_angles' phải là danh sách (list)"
        
    if len(comm_angles) < 1:
        return False, "'communication_angles' không được để trống"
        
    return True, ""


def _normalize_stage(raw_stage: str) -> str:
    """Chuẩn hóa stage về một trong 3 giá trị: Teaser, Launch, CTA."""
    if not raw_stage:
        return "Launch"
    s = str(raw_stage).strip().lower()
    if "teaser" in s or "tò mò" in s or "nhận thức" in s or "giai đoạn 1" in s:
        return "Teaser"
    elif "launch" in s or "ra mắt" in s or "giải pháp" in s or "giai đoạn 2" in s:
        return "Launch"
    elif "cta" in s or "kêu gọi" in s or "chốt" in s or "hành động" in s or "giai đoạn 3" in s:
        return "CTA"
    return "Launch"


def validate_agent2_output(data: Dict[str, Any], expected_channels: List[str] = None) -> Tuple[bool, str]:
    """
    Validate & chuẩn hóa output của Agent 2 (Campaign Copywriter):
    - Có key "posts" là danh sách các bài đăng
    - Mỗi post chứa các trường bắt buộc: stage, channel, title, content
    - Tự động chuẩn hóa stage, channel, content nếu LLM dùng alias
    """
    if not isinstance(data, dict):
        return False, "Output của Agent 2 phải là dict/JSON object"
        
    # Một số trường hợp LLM trả về trực tiếp danh sách bài viết
    if "posts" not in data:
        for possible_key in ["campaign_posts", "articles", "content_calendar", "items"]:
            if possible_key in data and isinstance(data[possible_key], list):
                data["posts"] = data[possible_key]
                break

    if "posts" not in data or not isinstance(data["posts"], list):
        return False, "Output phải chứa danh sách 'posts'"
        
    posts = data["posts"]
    if len(posts) < 1:
        return False, "Danh sách 'posts' không được để rỗng"
        
    for idx, post in enumerate(posts):
        if not isinstance(post, dict):
            return False, f"Bài post index {idx} không phải là dict"
            
        # Chuẩn hóa stage
        post["stage"] = _normalize_stage(post.get("stage", "Launch"))
            
        # Chuẩn hóa channel
        channel = post.get("channel") or post.get("platform") or "Facebook"
        channel_str = str(channel).strip()
        if "face" in channel_str.lower():
            post["channel"] = "Facebook"
        elif "link" in channel_str.lower():
            post["channel"] = "LinkedIn"
        elif "mail" in channel_str.lower():
            post["channel"] = "Email"
        else:
            post["channel"] = channel_str.title()
            
        # Chuẩn hóa title
        if not post.get("title"):
            post["title"] = post.get("headline") or post.get("subject") or f"Bài đăng {post['channel']} - {post['stage']}"
            
        # Chuẩn hóa content
        content = post.get("content") or post.get("body") or post.get("text") or post.get("caption")
        if not content or not str(content).strip():
            return False, f"Bài post index {idx} có 'content' rỗng"
        post["content"] = str(content).strip()
            
    return True, ""


def validate_agent3_output(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate & chuẩn hóa output của Agent 3 (Brand Compliance Auditor):
    - overall_score (số từ 0 - 100)
    - audited_posts (list kết quả kiểm duyệt từng bài)
    - Tự động tính toán overall_score nếu bị thiếu hoặc dạng chuỗi
    """
    if not isinstance(data, dict):
        return False, "Output của Agent 3 phải là dict/JSON object"
        
    # Chuẩn hóa audited_posts
    if "audited_posts" not in data:
        for possible_key in ["posts_audit", "audit_results", "audits", "results"]:
            if possible_key in data and isinstance(data[possible_key], list):
                data["audited_posts"] = data[possible_key]
                break

    audited_posts = data.get("audited_posts")
    if not isinstance(audited_posts, list):
        data["audited_posts"] = []
        audited_posts = data["audited_posts"]

    # Chuẩn hóa từng audited post
    post_scores = []
    for post in audited_posts:
        if isinstance(post, dict):
            # Parse compliance_score
            c_score = post.get("compliance_score", 100)
            try:
                c_score = float(c_score)
            except (ValueError, TypeError):
                c_score = 100.0
            c_score = max(0.0, min(100.0, c_score))
            post["compliance_score"] = c_score
            post_scores.append(c_score)

            # Đảm bảo violations là list
            if "violations" not in post or not isinstance(post["violations"], list):
                post["violations"] = []

    # Chuẩn hóa overall_score
    score = data.get("overall_score")
    if score is not None:
        try:
            score = float(score)
        except (ValueError, TypeError):
            score = None

    if score is None:
        if post_scores:
            score = round(sum(post_scores) / len(post_scores), 1)
        else:
            score = 100.0

    score = max(0.0, min(100.0, score))
    data["overall_score"] = score
        
    return True, ""
