"""
Extract url, English and Spanish names from BGA

"""

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


#URL with all the games
url_english="https://boardgamearena.com/gamelist?section=all"
url_spanish="https://es.boardgamearena.com/gamelist?section=all"

info_english=[]
info_spanish=[]
for item in [[url_english,info_english],[url_spanish,info_spanish]]:
    page_all_games = requests.get(item[0])
    bga_all = BeautifulSoup(page_all_games.text, "html.parser")
    #we search for the part in where all games appear:
    games_list=bga_all.find('div', id="gamelist_itemrow_inner_all")
    #we save the links and the name
    for a in games_list.find_all('a',href=True):
        item[1].append((a.get('href'),re.sub(' +', ' ',a.find('div',class_="gameitem_baseline gamename").text.replace('\n',''))))
        
data_english=pd.DataFrame(info_english,columns=['url','Name'])
data_spanish=pd.DataFrame(info_spanish,columns=['url','Nombre'])
all_data=pd.merge(data_english,data_spanish,on='url')
all_data.to_csv('BGA.csv')