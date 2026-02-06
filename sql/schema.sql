CREATE TABLE IF NOT EXISTS vehicle_cards (
    card_id TEXT PRIMARY KEY,
    vehicle_type TEXT,
    manufacturer TEXT,
    model TEXT,
    manufacture_year INTEGER,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS damage_detections (
    damage_id TEXT PRIMARY KEY,
    card_id TEXT,
    panel_name TEXT,
    damage_type TEXT,
    severity INTEGER,
    confidence REAL,
    detected_at TEXT
);

CREATE TABLE IF NOT EXISTS repairs (
    repair_id TEXT PRIMARY KEY,
    card_id TEXT,
    panel_name TEXT,
    repair_action TEXT,
    repair_cost REAL,
    approved INTEGER,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS quotes (
    quote_id TEXT PRIMARY KEY,
    card_id TEXT,
    total_estimated_cost REAL,
    currency TEXT,
    generated_at TEXT
);
