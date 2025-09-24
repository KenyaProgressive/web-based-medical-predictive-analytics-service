CREATE_TABLE_PARAMETRES = """CREATE TABLE IF NOT EXISTS parametres(
    id serial PRIMARY KEY,
    get_data_time TIMESTAMPTZ DEFAULT now(),
    bpm INTEGER,
    uterus INTEGER
)"""