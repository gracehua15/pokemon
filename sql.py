import sqlite3

def create_tables():
    """Create the database tables if they don't exist."""
    conn = sqlite3.connect('pokemon.db')  # Connect to the SQLite database
    cursor = conn.cursor()

    # Create the `game_sessions` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_sessions (
            session_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the `guesses` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guesses (
            guess_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            pokemon_name TEXT,
            user_guess TEXT,
            is_correct BOOLEAN,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES game_sessions(session_id)
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database tables created successfully.")

if __name__ == "__main__":
    create_tables()
