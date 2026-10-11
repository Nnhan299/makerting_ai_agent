"""
Module định nghĩa schema các bảng trong cơ sở dữ liệu PostgreSQL.
Tạo 4 bảng chính theo đúng Báo cáo Đồ án tốt nghiệp:
1. campaigns (BIGSERIAL, VARCHAR, TEXT, DATE, TIMESTAMPTZ, CHECK constraints)
2. campaign_posts (BIGSERIAL, BIGINT FK, VARCHAR, TEXT, DATE, TIMESTAMPTZ, CHECK constraints)
3. brand_rules (BIGSERIAL, VARCHAR, TEXT, TIMESTAMPTZ)
4. audit_logs (BIGSERIAL, BIGINT FK, DOUBLE PRECISION, JSONB, TEXT, TIMESTAMPTZ)
"""

from database.connection import get_connection


# === SQL tạo bảng campaigns ===
CREATE_CAMPAIGNS_TABLE = """
CREATE TABLE IF NOT EXISTS campaigns (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    product_name    VARCHAR(255) NOT NULL,
    target_audience TEXT,
    budget          VARCHAR(50),
    channels        VARCHAR(255),
    start_date      DATE NOT NULL,
    end_date        DATE NOT NULL CHECK (end_date >= start_date),
    status          VARCHAR(20) DEFAULT 'Draft' 
                    CHECK (status IN ('Draft', 'In-Progress', 'Approved', 'Completed')),
    created_at      TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ
);
"""

# === SQL tạo bảng campaign_posts ===
CREATE_CAMPAIGN_POSTS_TABLE = """
CREATE TABLE IF NOT EXISTS campaign_posts (
    id              BIGSERIAL PRIMARY KEY,
    campaign_id     BIGINT NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    stage           VARCHAR(20) NOT NULL 
                    CHECK (stage IN ('Teaser', 'Launch', 'CTA')),
    channel         VARCHAR(50) NOT NULL,
    title           VARCHAR(500),
    content         TEXT NOT NULL,
    scheduled_date  DATE,
    status          VARCHAR(20) DEFAULT 'Pending' 
                    CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    created_at      TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"""

# === SQL tạo bảng brand_rules ===
CREATE_BRAND_RULES_TABLE = """
CREATE TABLE IF NOT EXISTS brand_rules (
    id                  BIGSERIAL PRIMARY KEY,
    rule_name           VARCHAR(255) NOT NULL,
    forbidden_words     TEXT,
    mandatory_keywords  TEXT,
    tone_of_voice       VARCHAR(100),
    created_at          TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"""

# === SQL tạo bảng audit_logs ===
CREATE_AUDIT_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS audit_logs (
    id                  BIGSERIAL PRIMARY KEY,
    post_id             BIGINT REFERENCES campaign_posts(id) ON DELETE CASCADE,
    rule_id             BIGINT REFERENCES brand_rules(id) ON DELETE SET NULL,
    compliance_score    DOUBLE PRECISION CHECK (compliance_score >= 0 AND compliance_score <= 100),
    violations_json     JSONB NOT NULL,
    suggestions         TEXT,
    audited_at          TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"""


def init_database():
    """
    Khởi tạo database PostgreSQL: tạo tất cả 4 bảng nếu chưa tồn tại.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_CAMPAIGNS_TABLE)
            cursor.execute(CREATE_CAMPAIGN_POSTS_TABLE)
            cursor.execute(CREATE_BRAND_RULES_TABLE)
            cursor.execute(CREATE_AUDIT_LOGS_TABLE)
        conn.commit()
        print("[OK] Database PostgreSQL da duoc khoi tao thanh cong voi 4 bang.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Loi khoi tao database PostgreSQL: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
