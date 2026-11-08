"""Script chạy migration SQL an toàn (không xóa data cũ)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database.connection import get_connection

def apply():
    conn = get_connection()
    sql_path = os.path.join(os.path.dirname(__file__), '001_upgrade_schema.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    print("[Migration] ✅ Schema nâng cấp thành công!")

if __name__ == '__main__':
    apply()
