CREATE_TABLE_PARAMETRES = """CREATE TABLE IF NOT EXISTS parametres(
    id serial PRIMARY KEY,
    time FLOAT NOT NULL,
    bpm INTEGER,
    uterus FLOAT
)"""