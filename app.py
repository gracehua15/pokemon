from flask import Flask, render_template, request, redirect, session, jsonify
from helpers import get_pokemon_description, get_random_pokemon, get_pokemon_image, start_new_session, get_score
import sqlite3

app = Flask(__name__)
app.secret_key = 'swablu'

# Mock global state for current Pokémon
current_pokemon = "Pikachu"


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get the user's name and choice
        name = request.form.get('name', "").strip()
        game_type = request.form.get('game_type')

        # Error handling
        if not name:
            return render_template('index.html', warning="Name cannot be blank")
        if not game_type:
            return render_template('index.html', warning="Please select a game type")

        # Start a new session with the user's name and game type
        start_new_session(name, game_type)

        # Reroute based on the game type
        if game_type == "image":
            return redirect("/image")
        elif game_type == "description":
            return redirect("description")

    return render_template('index.html')


@app.route('/image', methods=["GET", "POST"])
def playImage():
    global current_pokemon

    session_id = session.get('session_id')  # Get the current session ID
    if not session_id:
        return redirect('/')  # Redirect to home if session ID is missing

    if request.method == "POST":
        # Determine if the user guessed or skipped
        action = request.form.get('action', 'guess')  # Default to 'guess'
        conn = sqlite3.connect('pokemon.db')
        cursor = conn.cursor()

        # Skip logic
        if action == 'skip':
            # Log in database
            cursor.execute('''
                INSERT INTO guesses (session_id, pokemon_name, user_guess, is_correct)
                VALUES (?, ?, ?, ?)
            ''', (session_id, current_pokemon, None, False))
            conn.commit()

            # Load new pokemon
            result = current_pokemon
            correctly_identified, total_shown = get_score(session_id)
            return render_template('image.html', result=result, image=get_pokemon_image(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=True)

        # Guess logic
        else:
            user_guess = request.form.get('guess', "").strip().capitalize()
            is_correct = user_guess == current_pokemon.capitalize()

            # Log guess in database
            cursor.execute('''
                INSERT INTO guesses (session_id, pokemon_name, user_guess, is_correct)
                VALUES (?, ?, ?, ?)
            ''', (session_id, current_pokemon, user_guess, is_correct))
            conn.commit()

            # Display result
            if is_correct:
                result = "Correct!"
                # Keep the current Pokémon for 3 seconds; JavaScript will handle redirect
                correctly_identified, total_shown = get_score(session_id)
                return render_template('image.html', result=result, image=get_pokemon_image(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=True)
            else:
                result = "Incorrect! Try again."

        conn.close()
        # Render the page for incorrect guesses
        correctly_identified, total_shown = get_score(session_id)
        return render_template('image.html', result=result, image=get_pokemon_image(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=False)

    # Handle GET requests (initial page load)
    current_pokemon = get_random_pokemon()
    correctly_identified, total_shown = get_score(session_id)
    return render_template('image.html', result="", image=get_pokemon_image(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=False)

@app.route('/description', methods=["GET", "POST"])
def playDescription():
    global current_pokemon


    session_id = session.get('session_id')  # Get the current session ID
    if not session_id:
        return redirect('/')  # Redirect to home if session ID is missing

    if request.method == "POST":
        # Determine if the user guessed or skipped
        action = request.form.get('action', 'guess')  # Default to 'guess'
        conn = sqlite3.connect('pokemon.db')
        cursor = conn.cursor()

        # Skip logic
        if action == 'skip':
            # Log in database
            cursor.execute('''
                INSERT INTO guesses (session_id, pokemon_name, user_guess, is_correct)
                VALUES (?, ?, ?, ?)
            ''', (session_id, current_pokemon, None, False))
            conn.commit()

            # Load new pokemon
            result = current_pokemon
            correctly_identified, total_shown = get_score(session_id)
            return render_template('description.html', result=result, description=get_pokemon_description(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=True)

        # Guess logic
        else:
            user_guess = request.form.get('guess', "").strip().capitalize()
            is_correct = user_guess == current_pokemon.capitalize()

            # Log guess in database
            cursor.execute('''
                INSERT INTO guesses (session_id, pokemon_name, user_guess, is_correct)
                VALUES (?, ?, ?, ?)
            ''', (session_id, current_pokemon, user_guess, is_correct))
            conn.commit()

            # Display result
            if is_correct:
                result = "Correct!"
                # Keep the current Pokémon for 3 seconds; JavaScript will handle redirect
                correctly_identified, total_shown = get_score(session_id)
                return render_template('description.html', result=result, description=get_pokemon_description(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=True)
            else:
                result = "Incorrect! Try again."

        conn.close()
        # Render the page for incorrect guesses
        correctly_identified, total_shown = get_score(session_id)
        return render_template('description.html', result=result, description=get_pokemon_description(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=False)

    # Handle GET requests (initial page load)
    current_pokemon = get_random_pokemon()
    correctly_identified, total_shown = get_score(session_id)
    return render_template('description.html', result="", description=get_pokemon_description(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=False)

@app.route('/autocomplete', methods=["GET"])
def autocomplete():
    query = request.args.get('q', '').lower()  # Get the query parameter
    if not query:
        return jsonify([])  # Return an empty list if no query is provided

    try:
        # Connect to the database
        conn = sqlite3.connect('pokemon.db')
        cursor = conn.cursor()

        # Fetch matching Pokémon names
        cursor.execute('SELECT name FROM pokemon WHERE name LIKE ? LIMIT 10', ('%' + query + '%',))
        results = cursor.fetchall()
        conn.close()

        # Return names as a JSON response
        return jsonify([row[0] for row in results])
    except Exception as e:
        print(f"Error in /autocomplete: {e}")  # Log the error to the console
        return jsonify({"error": "An error occurred while fetching suggestions"}), 500

if __name__ == "__main__":
    app.run(debug=True)
