"""
Script khởi tạo dữ liệu mẫu (Seed Demo Data) cho PostgreSQL database.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.models import init_database
from database.connection import get_connection
from database.crud import create_campaign, create_brand_rule, get_all_campaigns, get_all_brand_rules

def seed_data():
    print("[INFO] Khoi tao database PostgreSQL...")
    init_database()
    
    conn = get_connection()
    
    existing_camps = get_all_campaigns(conn)
    existing_rules = get_all_brand_rules(conn)
    
    if not existing_camps:
        print("[INFO] Tao chien dich demo 1...")
        create_campaign(
            conn=conn,
            name="Ra mắt Sữa rửa mặt XYZ Tháng 10",
            product_name="Sữa rửa mặt XYZ Salicylic Acid 2%",
            target_audience="Nữ 18-25 tuổi, da dầu mụn, sinh viên, muốn tìm sản phẩm skincare lành tính làm sạch sâu",
            budget="50.000.000 VND",
            channels="Facebook, Email",
            start_date="2026-10-01",
            end_date="2026-10-21"
        )
        
        print("[INFO] Tao chien dich demo 2...")
        create_campaign(
            conn=conn,
            name="Khuyến mãi Black Friday Skincare",
            product_name="Combo chăm sóc da mặt 3 bước XYZ",
            target_audience="Nữ 20-35 tuổi, người đi làm, hay mua sắm mỹ phẩm khuyến mãi trực tuyến",
            budget="100.000.000 VND",
            channels="Facebook, LinkedIn",
            start_date="2026-11-15",
            end_date="2026-11-30"
        )

    if not existing_rules:
        print("[INFO] Tao quy tac thuong hieu demo 1...")
        create_brand_rule(
            conn=conn,
            rule_name="Quy tắc ngành Mỹ phẩm & Dược mỹ phẩm",
            forbidden_words="tốt nhất, số 1, cam kết 100%, không tác dụng phụ, chữa khỏi, triệt để, vĩnh viễn",
            mandatory_keywords="XYZ Cosmetics",
            tone_of_voice="Trẻ trung"
        )
        
        print("[INFO] Tao quy tac thuong hieu demo 2...")
        create_brand_rule(
            conn=conn,
            rule_name="Quy tắc Quảng cáo Việt Nam",
            forbidden_words="tốt nhất, số 1, duy nhất, cam kết, đảm bảo 100%",
            mandatory_keywords="",
            tone_of_voice="Chuyên nghiệp"
        )
        
    conn.close()
    print("[OK] Da tao du lieu demo thanh cong va san sang hoat dong!")

if __name__ == "__main__":
    seed_data()
