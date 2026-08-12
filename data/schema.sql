CREATE TABLE IF NOT EXISTS products (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  source TEXT NOT NULL,
  source_url TEXT,
  launched_at TEXT,
  category TEXT,
  score INTEGER,
  payload TEXT NOT NULL,
  analyzed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_products_launched_at
  ON products(launched_at DESC);

CREATE INDEX IF NOT EXISTS idx_products_category
  ON products(category);
