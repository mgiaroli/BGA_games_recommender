# Recommender

The main goal of this project is to develop a recommender system for games in Board Game Arena. In this first approach, we built a content-based recommender, and we developed a web application in [**Streamlit**](https://streamlit.io/) to try our recommender.

The application is simple and there are two versions, in English and Spanish.
The user can choose one of the following options in order to create the user profile.

- Copy and paste own BGA game history
- Choose favorite games
- Select categories/mechanics 

The recommender depends on the user input. It is based on the categories and mechanics of the games, and to a lesser extent, we also take into account the Bayes average rating of the games in BGG. Once we create the user profile, we compute a similarity score for each game based on categories and another one based on mechanics. We add these scores, and then we add a small fraction of the Bayes average rating. We sort the games by this final score. 

The app recommends the games with the highest scores given by our recommender function. 

For more details, you can see the files in this folder: 

- recommender.py - Script that contains the content-based recommender function.
- streamlit_app.py - Script of the streamlit application.
- utilities_streamlit.py - Script with functions that will use in the app.
- boardgames.csv - Our database.
- categorias.txt, mecanicas.txt - Text files with the names of the categories and mechanics in Spanish.
- games.png - An image of board games.
- requirements.txt - A list of the packages we need to run the app.

You can try the app here:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/mgiaroli/bga_games_recommender/main/3.Recommender/streamlit_app.py)
