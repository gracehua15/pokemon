USE pokemon;
CREATE TABLE pokemon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    generation TEXT NOT NULL,
    primary_type TEXT NOT NULL,
    secondary_type TEXT,
    description TEXT NOT NULL,
    image TEXT);
