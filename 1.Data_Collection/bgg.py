
"""
We create the database BGG.csv

We collect the data from the BGG ids.

We use info_game from the module onegamebgg.
"""

import pandas as pd
from infogamebgg import info_game

#we open the file with the BGG ids.
with open('ids.txt') as file:
    ids=file.read().splitlines()

#initialize a list for the new information
info=[]

#add info for each id
for id_number in ids:
    try:
        info.append(info_game(id_number))
        print(id_number)
    except:
        print(id_number +' it does not work')

#we only add board games with info dictionary (there are also expansions in the id list)
info_onlybg=[item for item in info if isinstance(item, dict)]
                 
#data frame with new data
bgg_data = pd.DataFrame(info_onlybg)

#we save the table
bgg_data.to_csv('BGG.csv')