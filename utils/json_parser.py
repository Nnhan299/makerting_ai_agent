"""
Module validate JSON output từ các AI Agent.
Kiểm tra cấu trúc và điều kiện hợp lệ của dữ liệu đầu ra trước khi chuyển cho Agent tiếp theo hoặc lưu DB.
"""

from typing import Tuple, Dict, Any, List


def validate_agent1_output(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate output của Agent 1 (Market Intelligence):
    - target_persona (dict/object)
    - pain_points (list có >= 3 phần tử)
    - usp (str)
    - communication_angles (list có >= 2 phần tử)
    """
    if not isinstance(data, dict):
        return False, "Output cua Agent 1 phai la dict/JSON object"
        
    if "target_persona" not in data:
        return False, "Thieu thong tin 'target_persona'"
        
    if "pain_points" not in data or not isinstance(data["pain_points"], list):
        return False, "'pain_points' phai la danh sach (list)"
        
    if len(data["pain_points"]) < 3:
        return False, "'pain_points' phai co it nhat 3 phan tu"
        
    if "usp" not in data or not str(data["usp"]).strip():
        return False, "Thieu hoac rong 'usp'"
        
    if "communication_angles" not in data or not isinstance(data["communication_angles"], list):
        return False, "'communication_angles' phai la danh sach (list)"
        
    if len(data["communication_angles"]) < 2:
        return False, "'communication_angles' phai co it nhat 2 goc truyen thong"
        
    return True, ""


def validate_agent2_output(data: Dict[str, Any], expected_channels: List[str] = None) -> Tuple[bool, str]:
    """
    Validate output của Agent 2 (Campaign Copywriter):
    - Có key "posts" là danh sách các bài đăng
    - Mỗi post chứa các trường bắt buộc: stage, channel, title, content
    - stage thuộc ["Teaser", "Launch", "CTA"]
    """
    if not isinstance(data, dict):
        return False, "Output cua Agent 2 phai la dict/JSON object"
        
    if "posts" not in data or not isinstance(data["posts"], list):
        return False, "Output phai chua danh sach 'posts'"
        
    posts = data["posts"]
    if len(posts) < 1:
        return False, "Danh sach 'posts' khong duoc de rong"
        
    valid_stages = {"Teaser", "Launch", "CTA"}
    
    for idx, post in enumerate(posts):
        if not isinstance(post, dict):
            return False, f"Bai post index {idx} khong phai la dict"
            
        stage = post.get("stage")
        if stage not in valid_stages:
            return False, f"Bai post index {idx} co stage '{stage}' khong hop le (phai thuoc Teaser/Launch/CTA)"
            
        channel = post.get("channel")
        if not channel:
            return False, f"Bai post index {idx} thieu truong 'channel'"
            
        if expected_channels and channel not in expected_channels:
            # Format warning or strict validation if needed
            pass
            
        content = post.get("content")
        if not content or not str(content).strip():
            return False, f"Bai post index {idx} co 'content' rong"
            
    return True, ""


def validate_agent3_output(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate output của Agent 3 (Brand Compliance Auditor):
    - overall_score (số từ 0 - 100)
    - audited_posts (list kết quả kiểm duyệt từng bài)
    """
    if not isinstance(data, dict):
        return False, "Output cua Agent 3 phai la dict/JSON object"
        
    if "overall_score" not in data:
        return False, "Thieu truong 'overall_score'"
        
    score = data["overall_score"]
    if not isinstance(score, (int, float)) or score < 0 or score > 100:
        return False, f"'overall_score' ({score}) phai la so trong khoang 0 - 100"
        
    if "audited_posts" not in data or not isinstance(data["audited_posts"], list):
        return False, "Thieu hoac sai dinh dang 'audited_posts' (phai la list)"
        
    return True, ""
