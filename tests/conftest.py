"""
Pytest configuration and shared fixtures for Marketing AI Agent test suite.
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Đảm bảo môi trường kiểm thử chạy nhanh, độc lập mạng
os.environ["TESTING"] = "1"
os.environ["GEMINI_API_KEY"] = ""

from api_server import app
from database.connection import get_connection


@pytest.fixture(scope="session")
def client():
    """TestClient gọi trực tiếp FastAPI server mà không cần mở cổng mạng."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def db_conn():
    """Kết nối database cho mỗi test case (tự động đóng sau khi hoàn tất)."""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
