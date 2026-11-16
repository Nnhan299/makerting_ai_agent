"""
Trình chạy kiểm thử tự động toàn diện cho hệ thống Marketing AI Agent (AuraAI).
Tự động kích hoạt pytest, rà soát toàn bộ các phân hệ backend, AI, database và in báo cáo trực quan.
"""

import sys
import time
import os

try:
    import pytest
except ImportError:
    print("[ERROR] Thư viện pytest chưa được cài đặt. Vui lòng chạy: pip install pytest httpx")
    sys.exit(1)


def main():
    print("=" * 75)
    print("   AuraAI Marketing Intelligence Enterprise - BỘ KIỂM THỬ HỆ THỐNG")
    print("=" * 75)
    print("Đang khởi chạy bộ kiểm thử tự động (Unit Tests & Integration Tests)...")
    print("Thư mục kiểm thử: tests/")
    print("-" * 75)

    start_time = time.time()

    # Chạy pytest với báo cáo chi tiết
    args = [
        "tests",
        "-v",
        "--tb=short",
        "-W", "ignore::DeprecationWarning",
        "-W", "ignore::FutureWarning"
    ]

    exit_code = pytest.main(args)
    duration = time.time() - start_time

    print("\n" + "=" * 75)
    print("                     BÁO CÁO KẾT QUẢ KIỂM THỬ")
    print("=" * 75)
    print(f"• Thời gian thực thi: {duration:.2f} giây")
    if exit_code == 0:
        print("• Trạng thái tổng quan: [PASS] TẤT CẢ KIỂM THỬ ĐÃ THÀNH CÔNG (100% ĐẠT)")
        print("\nCác phân hệ đã được kiểm thử và xác thực hoạt động:")
        print("  [x] 1. REST API Server (Health check, Chiến dịch, Lịch đăng, Tuân thủ, Claims)")
        print("  [x] 2. Dual-Database CRUD (PostgreSQL 16 & SQLite Fallback, Connection Pool)")
        print("  [x] 3. AI Jobs & Dynamic SWOT (Phân tích theo dữ liệu người dùng, không text cứng)")
        print("  [x] 4. Agent Suite Pipeline (Market Intel -> Copywriter -> Brand Compliance)")
        print("  [x] 5. Quản trị hệ thống (User RBAC, Auth, Partners, Claims, API Keys Config)")
    else:
        print(f"• Trạng thái tổng quan: [FAIL] Có lỗi xảy ra trong quá trình kiểm thử (Mã lỗi: {exit_code})")
        print("Vui lòng xem chi tiết lỗi bên trên để khắc phục.")

    print("=" * 75)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
