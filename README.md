PROJECT DESCRIPTION

I created a web game called "Guess That Pokemon!" where it gives you a random image of a pokemon, and you have to guess what the pokemon is. I also tried to implement a version where you guess based on a description, rather than an image - but I removed this feature from the final product (though its route is still in the code).

There are 2 ways of playing the game: timed, or freeplay. In Timed, you have 1 minute to guess as many pokemon as possible. There is a leaderboard to track who was able to get the most number correct. In freeplay, you can guess until your heart's desire, but there is no leaderboard.

You also have the ability to filter by generations. If you're old school and don't know the pokemon from the more recent games, you can choose to only have pokemon show up from e.g., generations I, II, and III.

KEY FILES & FOLDERS

dbManagement: This is what I used to clean up some data that I was going to use later. From Kaggle, I found a csv of a pokemon database, containing lots and lots of information - a lot of which I didn't need. I also found a zip file of images of pokemon, titled by their name. In dbManagement, I cleaned up this data so that the names of pokemon in the csv matched the names of pokemon in the image files. I also had to add an image path for each row that gave the path to the corresponding pokemon image. (e.g., static/Pokemon/bulbasaur.png).

static: this is where all the pokemon images are stored & get pulled from (in folder Pokemon). This folder also contains my css for the website, as well as 3 png images of headers I pull into the web pages.

templates: There are 4 main pages that go into the final product (image, index, leaderboard, results). Index is the main page, that prompts users for their game preferences and starts the game. Image is the main content of gameplay - you can play timed or freeplay. Results is what shows up at the end of a timed gameplay that summarizes how you did, and shows a summarized leaderboard (10 entries). Leaderboard is a full list of all entries. There are 2 other templates in here - description.html (which I removed from the final product) and misc.html (which was just used to store excess information).

app.py: This is the main program! It has 6 routes: /, image, description, autocomplete, results, leaderboard. / is the home page that handles collecting information to render the proper version of the game. image and description are the different ways to play the game, and handles logic around generating random pokemon, pulling in their image, and validating if a user's guess is correct or not. autocomplete suggest pokemon based on what the user is typing in to help prompt the user in case they forget the exact spelling of a pokemon's name. results populates with the user's session stats, and renders a mini leaderborad. leaderboard actually pulls in full set of data.

helpers.py: These are the helper functions, such as getting a random pokemon (with generation filters accounted for), pulling in the actual image of the pokemon, starting a session, and keeping track of your score.

pokemon.db: There are 4 tables within the DB: pokemon, game_sessions, guesses, leaderboard. pokemon is the "source of truth" for all the answers. It contains all the pokemon, their image path, their generation, etc. game_session stores each time a game is played (incl. user name, which generations they selected to include, whether they played on timed vs freeplay). guesses stores every guess a user makes and is how you can keep track of their score. and leaderboard is the summary of each session's guesses - used to display in a more palatable format on the frontend.


YOUTUBE LINK

https://youtu.be/TvcRH5cjLVk


GOOGLE DRIVE ZIP

https://drive.google.com/file/d/1njt3MbkjP9aIm-pv7TULeiVQPRS5w47d/view?usp=sharing


