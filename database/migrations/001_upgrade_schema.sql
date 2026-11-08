-- ============================================================
-- Migration 001: Nâng cấp schema AuraAI
-- SAFE: Chỉ ADD, không DROP bảng/cột cũ
-- ============================================================

-- Thêm cột vào campaigns (nếu chưa có)
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS archetype text DEFAULT 'launch'
  CHECK (archetype IN ('launch','sale','lead_generation','always_on','branding'));
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS total_budget numeric(16,2);
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS plan_description text;

-- Thêm cột vào campaign_posts (nếu chưa có)
ALTER TABLE campaign_posts ADD COLUMN IF NOT EXISTS format text DEFAULT 'text_post'
  CHECK (format IN ('video_short','carousel','text_post','livestream_script','koc_brief'));
ALTER TABLE campaign_posts ADD COLUMN IF NOT EXISTS post_kind text DEFAULT 'organic'
  CHECK (post_kind IN ('organic','paid_ad','creator_partnership'));
ALTER TABLE campaign_posts ADD COLUMN IF NOT EXISTS disclosure_label text;
ALTER TABLE campaign_posts ADD COLUMN IF NOT EXISTS hook text;
ALTER TABLE campaign_posts ADD COLUMN IF NOT EXISTS hashtags text[] DEFAULT '{}';
ALTER TABLE campaign_posts ADD COLUMN IF NOT EXISTS assigned_to text;

-- Bảng mục tiêu SMART
CREATE TABLE IF NOT EXISTS objectives (
  id bigserial PRIMARY KEY,
  campaign_id bigint REFERENCES campaigns(id) ON DELETE CASCADE,
  objective_type text NOT NULL CHECK (objective_type IN ('awareness','engagement','conversion','retention','lead','revenue','market_share')),
  metric text NOT NULL,
  target_value numeric(18,4) NOT NULL,
  unit text,
  deadline date NOT NULL,
  baseline_value numeric(18,4),
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Bảng ngân sách chi tiết
CREATE TABLE IF NOT EXISTS budget_lines (
  id bigserial PRIMARY KEY,
  campaign_id bigint REFERENCES campaigns(id) ON DELETE CASCADE,
  category text NOT NULL CHECK (category IN ('paid_media','kol_koc','production','event','promotion','sponsorship','tools','contingency','other')),
  channel text,
  planned_amount numeric(16,2) NOT NULL DEFAULT 0,
  actual_amount numeric(16,2) NOT NULL DEFAULT 0,
  note text,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Bảng sản phẩm
CREATE TABLE IF NOT EXISTS products (
  id bigserial PRIMARY KEY,
  name text NOT NULL,
  code text UNIQUE,
  key_ingredients text,
  skin_types text[] DEFAULT '{}',
  notification_number text,
  price numeric(14,2),
  status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive','archived')),
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Bảng claim sản phẩm
CREATE TABLE IF NOT EXISTS product_claims (
  id bigserial PRIMARY KEY,
  product_id bigint REFERENCES products(id) ON DELETE CASCADE,
  claim_text text NOT NULL,
  claim_type text NOT NULL DEFAULT 'benefit'
    CHECK (claim_type IN ('benefit','ingredient','certification','comparison','statistic','other')),
  status text NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft','pending_review','approved','rejected','expired')),
  valid_until date,
  approved_by text,
  approved_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Bảng compliance checks
CREATE TABLE IF NOT EXISTS compliance_checks (
  id bigserial PRIMARY KEY,
  post_id bigint REFERENCES campaign_posts(id) ON DELETE CASCADE,
  score int NOT NULL DEFAULT 100 CHECK (score BETWEEN 0 AND 100),
  risk_level text NOT NULL DEFAULT 'low' CHECK (risk_level IN ('critical','warning','low')),
  findings jsonb NOT NULL DEFAULT '[]',
  engine_version text NOT NULL DEFAULT '1.0',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Bảng AI jobs
CREATE TABLE IF NOT EXISTS ai_jobs (
  id bigserial PRIMARY KEY,
  agent text NOT NULL CHECK (agent IN ('market_intel','brief_architect','content_synthesizer','compliance_semantic')),
  campaign_id bigint REFERENCES campaigns(id),
  post_id bigint REFERENCES campaign_posts(id),
  input jsonb NOT NULL DEFAULT '{}',
  output jsonb,
  status text NOT NULL DEFAULT 'queued' CHECK (status IN ('queued','running','succeeded','failed','cancelled')),
  error text,
  model text,
  input_tokens int DEFAULT 0,
  output_tokens int DEFAULT 0,
  cost_usd numeric(10,4) DEFAULT 0,
  queued_at timestamptz NOT NULL DEFAULT now(),
  started_at timestamptz,
  finished_at timestamptz,
  requested_by text
);

-- Bảng đối tác (KOL/KOC/agency)
CREATE TABLE IF NOT EXISTS partners (
  id bigserial PRIMARY KEY,
  partner_type text NOT NULL CHECK (partner_type IN ('agency','kol','koc','event_organizer','media','other')),
  name text NOT NULL,
  platform text,
  follower_count int DEFAULT 0,
  contact_email text,
  fee_per_post numeric(16,2),
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Bảng hiệu suất
CREATE TABLE IF NOT EXISTS performance_metrics (
  id bigserial PRIMARY KEY,
  campaign_id bigint REFERENCES campaigns(id),
  post_id bigint REFERENCES campaign_posts(id),
  channel text NOT NULL,
  metric_date date NOT NULL,
  traffic_type text NOT NULL DEFAULT 'organic' CHECK (traffic_type IN ('organic','paid')),
  views int DEFAULT 0,
  reach int DEFAULT 0,
  engagements int DEFAULT 0,
  clicks int DEFAULT 0,
  orders int DEFAULT 0,
  gmv numeric(16,2) DEFAULT 0,
  spend numeric(16,2) DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now()
);
