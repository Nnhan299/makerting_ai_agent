"""
Module kết nối cơ sở dữ liệu PostgreSQL cho hệ thống Marketing AI.
Tự động tạo database nếu chưa tồn tại và cung cấp RealDictCursor.
"""

import os
from contextlib import contextmanager
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Đọc biến môi trường
load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "marketing_ai")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DATABASE_URL = os.getenv("DATABASE_URL", None)


def ensure_database_exists():
    """
    Tự động kết nối đến DB hệ thống mặc định ('postgres') và tạo database POSTGRES_DB nếu chưa có.
    """
    if DATABASE_URL:
        return
    try:
        # Kết nối DB mặc định 'postgres'
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname="postgres",
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (POSTGRES_DB,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f'CREATE DATABASE "{POSTGRES_DB}"')
                print(f"[OK] Da tu dong tao database PostgreSQL '{POSTGRES_DB}' thanh cong.")
        conn.close()
    except Exception as e:
        print(f"[WARNING] Khong the kiem tra/tao auto DB: {e}")


def get_connection():
    """
    Tạo kết nối đến PostgreSQL database (sử dụng RealDictCursor).
    """
    ensure_database_exists()
    
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    else:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            cursor_factory=RealDictCursor
        )
    return conn


@contextmanager
def get_db_context():
    """
    Context manager cho kết nối database PostgreSQL.
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
