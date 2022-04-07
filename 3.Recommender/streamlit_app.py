"""
Creation of the streamlit app
"""

import streamlit as st
import pandas as pd
from recommender import recommendation_content_based
from utilities_streamlit import display_data

#streamlit run /home/maggie/BGA_games_recommender/3.Recommender/streamlit_app.py

#we load the data
df=pd.read_csv('3.Recommender/boardgames.csv')

#names of the games in english and spanish
names=sorted(df['Name'].to_list(),key=str.lower)
nombres=sorted(df['Nombre'].to_list(),key=str.lower)
names_all=[names, nombres]

#category cols
category_cols = [col for col in df.columns if 'Category:' in col]
category_cols_2=[col.replace('Category: ', '') for col in category_cols]
#categories in Spanish
with open('3.Recommender/categorias.txt') as file:
    categorias=file.read().splitlines()
#spanish-english category dictionary
dict_cat_spanish=dict(zip(categorias,sorted(category_cols_2)))
def category_col(category):
    """Given a category in Spanish, returns the corresponding column in df"""
    if category in dict_cat_spanish.keys():
        category=dict_cat_spanish[category]
    return 'Category: ' + category
categories_all=[sorted(category_cols_2),sorted(categorias)]

#mechanic cols
mechanic_cols = [col for col in df.columns if 'Mechanic:' in col]
mechanic_cols_2 = [col.replace('Mechanic: ', '') for col in mechanic_cols]
#mechanics in Spanish
with open('3.Recommender/mecanicas.txt') as file:
    mecanicas=file.read().splitlines()
#spanish-english mechanic dictionary
dict_mec_spanish=dict(zip(mecanicas,sorted(mechanic_cols_2)))
def mechanic_col(mechanic):
    """Given a mechanic in Spanish, returns the corresponding column in df"""
    if mechanic in dict_mec_spanish.keys():
        mechanic=dict_mec_spanish[mechanic]
    return 'Mechanic: ' + mechanic
mechanics_all=[sorted(mechanic_cols_2),sorted(mecanicas)]


#Texts in English and in Spanish that we will use in the app
title=['BGA games recommender','Recomendador de juegos de BGA']
header=["A content-based recommender for games in Board Game Arena",
        "Un recomendador basado en contenido de juegos de Board Game Arena"]
text_intro=["""Given games you like, we will recommend
            [Board Game Arena (BGA)](https://boardgamearena.com/) games that 
            are similar in terms of category and mechanics,
            according to the classification of [Board Game Geek (BGG)](https://boardgamegeek.com/).
            To a lesser extent, we also take into account the rating of the 
            game
             in BGG.\n""",
            """Dados juegos que te gustan, te recomendaremos juegos en
            [Board Game Arena (BGA)](https://boardgamearena.com/) similares en
            cuanto a la categoría y mecánica, según la clasificación de
            [Board Game Geek (BGG)](https://boardgamegeek.com/).
            En menor medida, también tenemos en cuenta el rating del juego
            en BGG.\n"""]
text_intro2=["""If you are a BGA's player, you can copy your BGA game
                    history below. Or you can select your BGA favourite games, 
                    or choose the categories/mechanics that you like.""",
                    """Si sos un jugador de BGA, podés copiar tu
                    historial de partidas abajo. O podés seleccionar tus juegos
                    favoritos de BGA o elegir las categorías/mecánicas que
                    te gustan."""]
text_options=["Choose the option you prefer:","Elige la opción que prefieras:"]
list_options=[("BGA's history",'Favourite games',
                        'Categories and mechanics you like'),
                       ("Historial de partidas en BGA",'Juegos favoritos',
                        'Categorías y mecánicas que te gustan')]
text_history=["Copy your BGA's history (in English):",
              "Copiá tu historial de BGA (en español):"]
history_help=["""English version of BGA only. Logged in BGA, go to this
              [page](https://boardgamearena.com/player?section=lastresults).
              In the right you will see "your user's game history". 
              Click there. In this new page you will find your 
              "Most played games". Copy and paste the games in the same format 
              as appears there. "Game_name" : "number_of_plays" games, each game
              separeted by one space or enter. 
              Example: Stone Age: 60 games Carcassonne: 60 games. Press Ctrl + Enter to see the 
              data you entered.""",
              """Para versión en español de BGA solamente. Cuando hayas iniciado sesión en
              BGA, andá a esta [página](https://boardgamearena.com/player?section=lastresults).
              A la derecha, vas a ver "Historial de partidas de" y tu usuario.
              Hacé click. En esta nueva página vas a encontrar tus
              "Juegos más jugados". Copiá y pegá los juegos en el mismo formato
              que aparecen.
              "Nombre_del_juego" : "número_de_partidas" partidas,
              cada juego separado por un espacio o enter.
              Ejemplo: Stone Age: 60 partidas Carcassonne: 60 partidas. Apretá Ctrl + Enter para ver 
              los datos que ingresaste."""]
fav_help=['You can choose as many games as you want','Podés elegir tantos juegos como quieras']
cat_help=["""You can select as many categories as you want.
          Check this [link](https://boardgamegeek.com/browse/boardgamecategory)
         as a guide.""", """Podés seleccionar tantas categorías como quieras.
         Chequeá este [link](https://boardgamegeek.com/browse/boardgamecategory) como guía."""]
mec_help=["""You can select as many mechanics as you want.
          Check this [link](https://boardgamegeek.com/browse/boardgamemechanic)
         as a guide.""", """Podés seleccionar tantas mecánicas como quieras.
         Chequeá este [link](https://boardgamegeek.com/browse/boardgamemechanic) como guía."""]
text_fav_games=['Choose your favorite games from BGA',
                'Selecciona tus juegos favoritos de BGA']
text_cat=['Choose categories you like',
          'Selecciona las categorías que te gustan']
text_mec=['Choose mechanics you like',
          'Selecciona las mecánicas que te gustan']
text_recommend=['Recommend','Recomendaciones']
text_other_games=['More recommendations:',
                  'Más recomendaciones:']
text_other_games_ranking=["""Other games you might like, not related
                          to your preferences, but highly rated on BGG""",
                          """"Otros juegos que te pueden gustar, no
                          relacionados con tus preferencias, pero con rating alto en BGG"""]
text_warning_empty=['Enter your infomation/preferences','Ingresá tu información/preferencias']
text_warning=['Check your input','Chequeá lo que ingresaste']
text_no_new_games=['You know all the games in our database!',
                   'Conocés todos los juegos en nuestra base de datos!']
text_last_updated=['\n Last updated: 7 April 2022', ' \n Última actualización: 7 de abril de 2022']


#we need the following to hide indexes in a table
# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)


###the app###

#first we choose the language
language_option = st.sidebar.selectbox('Language/Idioma', ['English', 'Español'])

def page(language): #if number=0, the page will
    """design of streamlit app depending on the language"""
    #title
    st.title(title[language])
    #header
    st.header(header[language])
    #we load an image
    st.image('3.Recommender/games.png', use_column_width=True)
    #last updated
    with st.sidebar:
        st.write(text_last_updated[language])
    #introductory text
    st.write(text_intro[language])
    st.write(text_intro2[language])
    #input options
    options= st.radio(text_options[language],list_options[language])
    #we will check if the input is empty
    empty=False
    if options==list_options[language][0]: #game history
        history_data=st.text_area(text_history[language],help=history_help[language])
        user_data=display_data(history_data,language,0) #we display the user's input
        try: #we try to display the data
            st.write(user_data)
            if user_data.shape[0]==0:
                empty=True
        except:
            ""
        case=0 #we will use the cases for the recommender
    elif options==list_options[language][1]: #favourite games
        fav_games = st.multiselect(text_fav_games[language],names_all[language],help=fav_help[language])
        user_data=display_data(fav_games,language,1)
        st.write(user_data)
        case=1
        if user_data.shape[0]==0:
            empty=True
    elif options==list_options[language][2]: #categories and mechanics
        cat=st.multiselect(text_cat[language],categories_all[language],help=cat_help[language])
        mec=st.multiselect(text_mec[language],mechanics_all[language],help=mec_help[language])
        col1, col2 = st.columns(2) #we display the info in two tables
        with col1:
            st.table(display_data(cat,language,2))
        with col2:
            st.table(display_data(mec,language,3))
        user_data=[[category_col(category) for category in cat],
                   [mechanic_col(mechanic) for mechanic in mec],language]
        case=2
        if len(user_data[0])==0 and len(user_data[1])==0:
            empty=True
    if st.button(text_recommend[language]):
        try:
            if empty: #we check that the user's input is not empty
                st.warning(text_warning_empty[language])
            else: #if user's input not empty
                #the names of the games
                recommendation=recommendation_content_based(user_data,case)[0]
                #the games that the user don't know
                number_new_games=recommendation.shape[0]
                #games with cat and mec scores no null
                nonull=recommendation_content_based(user_data,case)[1]
                if number_new_games==0: #the user knows all the games
                    st.write(text_no_new_games[language])
                else: #if the user doesn't know all the games
                    #we recommend at most 10 games
                    for row in range(min(nonull,10,number_new_games)):
                        col1, col2 = st.columns(2)
                        with col1: #we give the name of the game and the BGA url
                            st.write(str(row+1)+') [' + recommendation[recommendation.columns[0]].iloc[row]
                                     +'](https://boardgamearena.com'+recommendation.url.iloc[row]+')')
                        with col2: #we give an image of the game
                            st.image(recommendation.Thumbnail.iloc[row])
                    if nonull<=10: #this means that number_new_games is big, we recommend games by BGG rating
                        with st.expander(text_other_games_ranking[language], expanded=False):
                            for row in range(10):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(str(nonull+row+1)+') [' + recommendation[recommendation.columns[0]].iloc[nonull + row]
                                             +'](https://boardgamearena.com'+recommendation.url.iloc[nonull + row]+')')
                                with col2:
                                    st.image(recommendation.Thumbnail.iloc[nonull + row])
                    else:
                        if number_new_games>10:
                            #we show more games, 10 more at most
                            with st.expander(text_other_games[language], expanded=False):
                                for row in range(10,min(20,nonull,number_new_games)):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(str(row+1)+') [' + recommendation[recommendation.columns[0]].iloc[row]
                                                 +'](https://boardgamearena.com'+recommendation.url.iloc[row]+')')
                                    with col2:
                                        st.image(recommendation.Thumbnail.iloc[row])
        except:
            st.warning(text_warning[language])
        

#we present the app depending on the language
if language_option=='English':
    page(0)
else:
    page(1)
