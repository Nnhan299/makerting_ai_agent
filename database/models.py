"""
Module định nghĩa schema các bảng trong cơ sở dữ liệu hỗ trợ cả PostgreSQL & SQLite.
4 bảng chính theo đúng Báo cáo Đồ án tốt nghiệp:
1. campaigns
2. campaign_posts
3. brand_rules
4. audit_logs
"""

from database.connection import get_connection, get_db_type


# ============================================================
# === SCHEMA CHO POSTGRESQL ===
# ============================================================
PG_CAMPAIGNS_TABLE = """
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

PG_CAMPAIGN_POSTS_TABLE = """
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

PG_BRAND_RULES_TABLE = """
CREATE TABLE IF NOT EXISTS brand_rules (
    id                  BIGSERIAL PRIMARY KEY,
    rule_name           VARCHAR(255) NOT NULL,
    forbidden_words     TEXT,
    mandatory_keywords  TEXT,
    tone_of_voice       VARCHAR(100),
    created_at          TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"""


PG_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id            BIGSERIAL PRIMARY KEY,
    username      VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(100),
    role          VARCHAR(30) NOT NULL DEFAULT 'Content Creator'
                  CHECK (role IN ('Admin', 'Marketing Lead', 'Content Creator')),
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"""

PG_AUDIT_LOGS_TABLE = """
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


# ============================================================
# === SCHEMA CHO SQLITE ===
# ============================================================
SQLITE_CAMPAIGNS_TABLE = """
CREATE TABLE IF NOT EXISTS campaigns (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    product_name    TEXT NOT NULL,
    target_audience TEXT,
    budget          TEXT,
    channels        TEXT,
    start_date      TEXT NOT NULL,
    end_date        TEXT NOT NULL,
    status          TEXT DEFAULT 'Draft'
                    CHECK (status IN ('Draft', 'In-Progress', 'Approved', 'Completed')),
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at      TEXT
);
"""

SQLITE_CAMPAIGN_POSTS_TABLE = """
CREATE TABLE IF NOT EXISTS campaign_posts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id     INTEGER NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    stage           TEXT NOT NULL
                    CHECK (stage IN ('Teaser', 'Launch', 'CTA')),
    channel         TEXT NOT NULL,
    title           TEXT,
    content         TEXT NOT NULL,
    scheduled_date  TEXT,
    status          TEXT DEFAULT 'Pending'
                    CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

SQLITE_BRAND_RULES_TABLE = """
CREATE TABLE IF NOT EXISTS brand_rules (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name           TEXT NOT NULL,
    forbidden_words     TEXT,
    mandatory_keywords  TEXT,
    tone_of_voice       TEXT,
    created_at          TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


SQLITE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name     TEXT NOT NULL,
    email         TEXT,
    role          TEXT NOT NULL DEFAULT 'Content Creator'
                  CHECK (role IN ('Admin', 'Marketing Lead', 'Content Creator')),
    is_active     INTEGER DEFAULT 1,
    created_at    TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

SQLITE_AUDIT_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS audit_logs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id             INTEGER REFERENCES campaign_posts(id) ON DELETE CASCADE,
    rule_id             INTEGER REFERENCES brand_rules(id) ON DELETE SET NULL,
    compliance_score    REAL CHECK (compliance_score >= 0 AND compliance_score <= 100),
    violations_json     TEXT NOT NULL,
    suggestions         TEXT,
    audited_at          TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def init_database():
    """
    Khởi tạo bảng trong cơ sở dữ liệu (tự động nhận biết PostgreSQL hoặc SQLite).
    """
    conn = get_connection()
    db_type = get_db_type(conn)
    
    try:
        if db_type == "postgres":
            with conn.cursor() as cursor:
                cursor.execute(PG_CAMPAIGNS_TABLE)
                cursor.execute(PG_CAMPAIGN_POSTS_TABLE)
                cursor.execute(PG_BRAND_RULES_TABLE)
                cursor.execute(PG_AUDIT_LOGS_TABLE)
                cursor.execute(PG_USERS_TABLE)
            conn.commit()
            print("[OK] Database PostgreSQL da duoc khoi tao thanh cong voi 4 bang.")
        else:
            cursor = conn.cursor()
            cursor.execute(SQLITE_CAMPAIGNS_TABLE)
            cursor.execute(SQLITE_CAMPAIGN_POSTS_TABLE)
            cursor.execute(SQLITE_BRAND_RULES_TABLE)
            cursor.execute(SQLITE_AUDIT_LOGS_TABLE)
            cursor.execute(SQLITE_USERS_TABLE)
            conn.commit()
            print("[OK] Database SQLite da duoc khoi tao thanh cong voi 4 bang (data/marketing.db).")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Loi khoi tao database ({db_type}): {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
