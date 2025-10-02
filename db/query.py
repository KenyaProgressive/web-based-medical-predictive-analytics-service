CREATE_TABLE_BPM = """
    TRUNCATE bpm;
    CREATE TABLE IF NOT EXISTS bpm(
    id serial PRIMARY KEY,
    time FLOAT NOT NULL,
    bpm FLOAT
)"""

CREATE_TABLE_UTERUS = """
    TRUNCATE uterus;
    CREATE TABLE IF NOT EXISTS uterus(
    id serial PRIMARY KEY,
    time FLOAT NOT NULL,
    uterus FLOAT
)"""