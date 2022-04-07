"""
Functions that will use to display the user information in the streamlit app
"""
import pandas as pd
import re
import streamlit as st

df_games=pd.read_csv('3.Recommender/boardgames.csv')

def history_data(data,language):
    """Return a dataframe with the user's game history"""
    warning=["""Check your input. Check that the names of the games
                      are written exactly as in BGA and that the games you 
                      entered are currently in BGA (and indexed in BGG)""",
              """Chequeá tu input. Chequeá que si los nombres de los juegos 
              están escritos exactamente como en BGA y que los juegos que 
              ingresaste están en BGA (e indexados en BGG)"""]
    warning2=["""Check how you fill your history data. The valid format is 
             "Game_name" : "number_of_plays" games, each game separeted by one space. 
             Example: Stone Age: 60 games Carcassonne: 60 games """,
             """Chequea como cargaste tu historial de partidas. El formato válido 
             es "Nombre_del_juego" : "número_de_partidas" partidas, 
             cada juego separado por un espacio. 
             Ejemplo: Stone Age: 60 partidas Carcassonne: 60 partidas"""]   
    try:
        if language==0: #English
            st.write(data)
            user_data=re.sub("Most played games","",data,count=1)
            user_data=re.sub("\[Filter]","",user_data).strip()
            played_games_list=user_data.split('games')
            played_games=[[item.strip().rsplit(':',1)[0],int(item.strip().rsplit(':',1)[1])] for item in played_games_list if len(item)>0]
            df=pd.DataFrame(played_games, columns = ['Name', 'Number of games played'])
            if df.shape[0]!=0 and df[df['Name'].isin(df_games['Name'])].shape[0]==0:
                return st.warning(warning[language])
        else: #Spanish
            st.write(data)
            user_data=re.sub("Juegos más jugados","",data,count=1)
            user_data=re.sub("\[Filtrar]","",user_data).strip()
            played_games_list=user_data.split('partidas')
            played_games=[[item.strip().rsplit(':',1)[0],int(item.strip().rsplit(':',1)[1])] for item in played_games_list if len(item)>0]
            df=pd.DataFrame(played_games, columns = ['Nombre', 'Partidas jugadas'])
            if df.shape[0]!=0 and df[df['Nombre'].isin(df_games['Nombre'])].shape[0]==0:
                return st.warning(warning[language])
        return df
    except:
        return st.warning(warning2[language])
        
        
def fav_games(data,language):
    """Return a dataframe with the user's favourite games"""
    if language==0: #English
        return pd.DataFrame(data,columns=['Name'])
    else: #Spanish
        return pd.DataFrame(data,columns=['Nombre'])

def cat(data,language):
    """We return a dataframe with the list of the liked categories"""
    if language==0: #english           
        return pd.DataFrame(data,columns=['Category'])
    else:
        return pd.DataFrame(data,columns=['Categoría'])

def mec(data,language):
    """We return a dataframe with the list of the liked mechanics"""
    if language==0: #english           
        return pd.DataFrame(data,columns=['Mechanic'])
    else:
        return pd.DataFrame(data,columns=['Mecánica'])


def display_data(data,language,option):
    """Function that displays the user information according to each case"""
    if option==0: #history
        return  history_data(data,language)
    elif option==1: #fav games
        return fav_games(data,language)
    elif option==2: # cat 
        return cat(data,language)
    elif option==3: #mec
        return mec(data,language)
