BASICS

Backend: Python, flask, session management
Frontend: HTML, CSS, Javascript
Database: SQLite


ARCHITECTURE & DESIGN CHOICES

Timed vs Free Play: I wanted to have 2 versions of the game available - one for the competitively minded, and one who just wanted to play to their heart's content. But what's competition without having some pressure and the same constraints for everyone to work under - which is why I introduced the element of time. I also implemented a leaderboard - only for timed play - to further enhance the competitive nature.

Game State Management: I wanted each time a user played the game to be stored separately. I used Flask’s session to track: Player’s name, Selected generations, Current score and total Pokémon shown, Timer start time (for Timed Mode), Game completion status.

Autocomplete: Pokemon have weird names. I wanted to not penalize people for not remembering exactly how to spell a pokemon's name even if they knew basically what the pokemon was.

Scorekeeping logic: I thought it was only fair to mark an answer as "incorrect" if they ultimately didn't get it. I didn't want to penalize every guess that was wrong - because what if I just misspelled a pokemon's name? So you either guess until you get it correct (+1) or you give up, and you don't get the point.

Database: I created separate databases. 1 to store the "source of truth", and then 3 to track user engagement. Guesses, sessions, and leaderboard are all tied together using sessionID.
