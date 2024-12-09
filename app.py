from flask import Flask, render_template, request, redirect, session, jsonify
from helpers import get_pokemon_description, get_pokemon_image, start_new_session, get_score, get_random_pokemon_filter
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = 'swablu'

# Mock global state for current Pokémon
current_pokemon = "Pikachu"


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Clear the session to reset any previous game state
        session.clear()

        # Get the user's name and choice
        name = request.form.get('name', "").strip()
        game_mode = request.form.get('game_mode')
        game_type = request.form.get('game_type')
        selected_generations = request.form.get('generation', "I, II, III, IV, V, VI, VII, VIII").split(',')

        # Error handling
        if not name:
            return render_template('index.html', warning="Name cannot be blank")
        if not game_mode:
            return render_template('index.html', warning="Please select your mode of gameplay")
        if not game_type:
            return render_template('index.html', warning="Please select your game format")

        # Join the selected generations into a string
        generations_string = ', '.join(selected_generations)

        # Start a new session with the user's name and game type
        start_new_session(name, game_type, generations_string, game_mode)

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
    generations = session.get('generations', ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"])  # Default to all generations
    game_mode = session.get('game_mode', 'free')  # Default to free play

    # Convert generations to a list if it is a string
    if isinstance(generations, str):
        generations = generations.split(',')  # Split the string into a list
        generations = [gen.strip() for gen in generations]  # Remove any extra whitespace

    if not session_id:
        return redirect('/')  # Redirect to home if session ID is missing

    # Handle timed mode: Check if the timer has expired
    from datetime import datetime, timedelta

    if game_mode == 'timed':
        if 'start_time' not in session:
            session['start_time'] = datetime.now().isoformat()  # Set the start time
            print(f"DEBUG: Timer started at {session['start_time']}")

        start_time = datetime.fromisoformat(session['start_time'])
        end_time = start_time + timedelta(seconds=60)

        print(f"DEBUG: Current time: {datetime.now()}, End time: {end_time}, Time remaining: {end_time - datetime.now()}")



        # Redirect if the timer has expired
        if datetime.now() > end_time - timedelta(seconds=2):
            session['game_completed'] = True
            print("DEBUG: Timer expired. session['game_completed'] set to True.")
            return redirect("/results")  # End the game if time has expired
    else:
        # Default end_time for free play (not used but required for render_template)
        end_time = datetime.now() + timedelta(hours=1)  # Placeholder


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
            return render_template('image.html', result=result, image=get_pokemon_image(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=True, end_time=end_time.isoformat())

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
                return render_template('image.html', result=result, image=get_pokemon_image(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=True, end_time=end_time.isoformat())
            else:
                result = "Incorrect! Try again."

        conn.close()
        # Render the page for incorrect guesses
        correctly_identified, total_shown = get_score(session_id)
        return render_template('image.html', result=result, image=get_pokemon_image(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=False, end_time=end_time.isoformat())

    # Handle GET requests (initial page load)
    current_pokemon = get_random_pokemon_filter(generations)
    correctly_identified, total_shown = get_score(session_id)
    return render_template('image.html', result="", image=get_pokemon_image(current_pokemon), correctly_identified=correctly_identified, total_shown=total_shown, wait=False, end_time=end_time.isoformat())

@app.route('/description', methods=["GET", "POST"])
def playDescription():
    global current_pokemon

    session_id = session.get('session_id')  # Get the current session ID
    generations = session.get('generations', ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"])  # Default to all generations

    # Convert generations to a list if it is a string
    if isinstance(generations, str):
        generations = generations.split(',')  # Split the string into a list
        generations = [gen.strip() for gen in generations]  # Remove any extra whitespace

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
    current_pokemon = get_random_pokemon_filter(generations)
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



@app.route('/results', methods=["GET"])
def results():
    print(f"DEBUG: Session data at /results: {session}")

    # Fetch data from session
    name = session.get('name', 'Unknown')
    session_id = session.get('session_id', 'Unknown')
    generations = session.get('generations', [])  # Convert list to string
    game_mode = session.get('game_mode', 'free')  # Timed or free play

    # Query the database to calculate the score and total Pokémon shown
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    # Count the number of correctly guessed Pokémon
    cursor.execute('''
        SELECT COUNT(DISTINCT user_guess)
        FROM guesses
        WHERE session_id = ? AND is_correct = 1
    ''', (session_id,))
    score = cursor.fetchone()[0]

    # Count the total number of Pokémon shown
    cursor.execute('''
        SELECT COUNT(DISTINCT pokemon_name)
        FROM guesses
        WHERE session_id = ?
    ''', (session_id,))
    total_shown = cursor.fetchone()[0]


    # Save to leaderboard only if the game was timed
    if session.get('game_completed', False) and game_mode == 'timed':
        print("DEBUG: Saving to leaderboard...")
        conn = sqlite3.connect('pokemon.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO leaderboard (name, session_id, pokemon_guessed_correctly, total_pokemon_shown, generations)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, session_id, score, total_shown, generations))
        conn.commit()
    else:
        print("DEBUG: Conditions for saving to leaderboard not met.")

    # Fetch leaderboard data
    cursor.execute('''
        SELECT
                name,
                pokemon_guessed_correctly,
                CAST(ROUND((pokemon_guessed_correctly * 1.0 / total_pokemon_shown) * 100, 0) AS INTEGER) || '%' AS accuracy,
                generations
        FROM leaderboard
        WHERE name != 'Unknown'
        ORDER BY pokemon_guessed_correctly DESC, accuracy DESC
        LIMIT 10
    ''')
    leaderboard = cursor.fetchall()
    conn.close()

    # Clear session data to prevent duplicate saves
    session.clear()

    # Render results
    return render_template(
        'results.html',
        name=name,
        score=score,
        total_shown=total_shown,
        generations=generations,
        game_mode=game_mode,
        leaderboard = leaderboard

    )


@app.route('/leaderboard', methods=["GET"])
def leaderboard():
    # Connect to the database and fetch leaderboard data
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    # Fetch leaderboard data with filters applied
    cursor.execute('''
        SELECT
            name,
            pokemon_guessed_correctly,
            CAST(ROUND((pokemon_guessed_correctly * 1.0 / total_pokemon_shown) * 100, 0) AS INTEGER) || '%' AS accuracy,
            generations,
            timestamp
        FROM leaderboard
        WHERE
            name != 'Unknown' AND
            total_pokemon_shown > 0
        ORDER BY pokemon_guessed_correctly DESC, accuracy DESC
    ''')
    full_leaderboard = cursor.fetchall()
    conn.close()

    # Pass the data to the template
    return render_template('leaderboard.html', leaderboard=full_leaderboard)
