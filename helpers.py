import sqlite3
import uuid
from flask import session

def get_pokemon_description(pokemon_name):
    # Connect to the database
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    # Query to fetch the description for the given Pokémon name
    query = "SELECT description FROM pokemon WHERE name = ?"
    cursor.execute(query, (pokemon_name,))

    # Fetch the result
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return the description if found, or a default message if not
    if result:
        return result[0]  # The description is the first (and only) column in the result
    else:
        return "A mysterious Pokémon..."

def get_random_pokemon():
    # Connect to the database
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    # Query to select a random Pokemon
    query = "SELECT name FROM pokemon ORDER BY RANDOM() LIMIT 1"
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return the name directly (or None if the table is empty)
    return result[0] if result else None

def get_pokemon_image(pokemon_name):
    # Connect to the database
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    # Query to fetch the description for the given Pokémon name
    query = "SELECT image_link FROM pokemon WHERE name = ?"
    cursor.execute(query, (pokemon_name,))

    # Fetch the result
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return the description if found, or a default message if not
    if result:
        return result[0]  # The description is the first (and only) column in the result
    else:
        return "A mysterious Pokémon..."

def start_new_session(user_name, game_type):
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    session['session_id'] = session_id  # Store session ID in Flask session

    # Log session in the database
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO game_sessions (session_id, name, game_type)
        VALUES (?, ?, ?)
    ''', (session_id, user_name, game_type))
    conn.commit()
    conn.close()

def get_score(session_id):
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    # Numerator: Count unique Pokémon correctly identified
    cursor.execute('''
        SELECT COUNT(DISTINCT pokemon_name)
        FROM guesses
        WHERE session_id = ? AND is_correct = 1
    ''', (session_id,))
    correctly_identified = cursor.fetchone()[0]

    # Denominator: Count unique Pokémon shown
    cursor.execute('''
        SELECT COUNT(DISTINCT pokemon_name)
        FROM guesses
        WHERE session_id = ?
    ''', (session_id,))
    total_shown = cursor.fetchone()[0]

    conn.close()
    return correctly_identified, total_shown
