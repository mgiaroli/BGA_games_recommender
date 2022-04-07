
"""
Update database Board_games_BGG.csv

We use this scrip when there are new BGG ids.

We use info_game from the module onegamebgg.
"""

import pandas as pd
from infogamebgg import info_game

#we load the BGG data base
bgg_data=pd.read_csv('BGG.csv',index_col=0)

#we open the file with the BGG ids.
with open('ids.txt') as file:
    ids=file.read().splitlines()

#initialize a list for the new information
info_new=[]

#check for each id if the correspondent game is already in our data or add info
NUM=1
for id_number in ids:
    if int(id_number) not in bgg_data.GameID.values:
        try:
            info_new.append(info_game(id_number))
        except:
            print(id_number +' it does not work')
    #print(num)
    NUM+=1

#we only add board games with info dictionary (there are also expansions in the id list)
info_new_onlybg=[item for item in info_new if isinstance(item, dict)]
                 
#data frame with new data
bgg_new_data = pd.DataFrame(info_new_onlybg)

#we add the new rows
Board_games_BGG=pd.concat([bgg_data,bgg_new_data],ignore_index=True)

#we save the table
Board_games_BGG.to_csv('BGG.csv')
