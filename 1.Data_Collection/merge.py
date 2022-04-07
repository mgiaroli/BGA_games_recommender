"""
We join the data from BGG and BGA.
We change the names of the games in BGG to coincide with the ones in BGA.
"""

import pandas as pd

#we load the data
bga=pd.read_csv('BGA.csv',index_col=0)
bgg=pd.read_csv('BGG.csv',index_col=0)

#We delete the spaces at the beginning and at the end of the string
bga['Name']=bga['Name'].apply(lambda x: x.strip())
bga['Nombre']=bga['Nombre'].apply(lambda x: x.strip())


#Change names
"""
Manually we change names that don't coincide. We found these differences running this scrip. 
When we find a difference, we add it to this dictionary, or check what is the problem.
The keys are the names from BGG and the values the names from BGA.
"""

replace_values={'L.L.A.M.A.' : 'LLAMA',
'Through the Ages: A New Story of Civilization' : 'Through the Ages: A new Story of Civilization',
'Through the Ages: A Story of Civilization' :  'Through the Ages',
'Carcassonne: Hunters and Gatherers' : 'Carcassonne: Hunters & Gatherers',
'Colorpop': 'Color Pop',
'Welcome to New Las Vegas':'Welcome To New Las Vegas',
'Yōkai':'Yokai',
'In the Year of the Dragon':'In The Year of the Dragon' ,
'Agricola (Revised Edition)' : 'Agricola',
'Welcome To...' :  'Welcome To',
'Railroad Ink: Deep Blue Edition' :  'Railroad Ink',
"Tzolk'in: The Mayan Calendar" :  "Tzolk'in",
'Trek 12: Himalaya': 'Trek 12',
'Conspiracy: Abyss Universe':'Conspiracy',
'The Crew: The Quest for Planet Nine':'The Crew',
'INSERT': 'Insert',
'Apocalypse au Zoo de Carson City': 'Apocalypse at the Zoo of Carson City',
'Battleship':'Battleships Pencil & Paper',
'Chinagold':'China Gold',
'Crazy Farmers and the Clôtures Électriques':'Crazy Farmers',
'Medina (Second Edition)':'Medina',
'Lewis & Clark: The Expedition':'Lewis & Clark',
'NOIR: Deductive Mystery Game':'Noir: Killer versus Inspector',
'Remember When ...':'Remember When',
'Evo':'Evo: The “Game no Name”',
'Go-Moku':'Gomoku',
'Il était une forêt': 'Once Upon A Forest',
'Polis: Fight for the Hegemony':'Polis: Fight for Hegemony',
'Escape from the Hidden Castle': 'Hugo',
'Tash-Kalar: Arena of Legends':'Tash-Kalar',
'Turn the Tide':'Turn the tide',
'Tarot': 'French Tarot',
'Blockers!':'Uptown',
'Cinch':'Pedro',
'Diamant':'Incan Gold',
'GOSU':'Gosu',
'Gurami: das Spiel':'GORami',
'Gyges':'Gygès',
'Hearts & Spades':'Sparts',
'Insidious Sevens':'Oh-Seven',
'Krosmaster: Arena':'Krosmaster Arena',
'Krosmaster: Blast':'Krosmaster Blast',
'Othello':'Reversi',
'イラストリー (Illustori)':'Illustori',
'What the Heck?': 'Vulture Culture',
'Hội Phố': 'Fai-fo',
'Super Tock 6':'Tock',
'See Sek':'Four Color Cards',
'Scum: The Food Chain Game': 'President',
'Tarock': 'Grosstarock',
'Clash of Deck':'Clash of Decks',
'Chinese Checkers': 'Chinese checkers',
'Contract Rummy':'Liverpool (Cozy Oaks) Rummy',
'Queens & Kings ...A Checkers Game' : 'Queens & Kings... A Checkers Game',
'The Lady and the Tiger':'The Lady and the Tiger (Doors)',
"I'm the Boss!":"I'm The Boss",
'7 Wonders: Architects':'7 Wonders Architects',
'Century: Spice Road':'Century',
'Stella: Dixit Universe':'Stella – Dixit Universe',
'Spot it!':'Spot it',
'Space Empires 4X':'Space Empires: 4X',
'Riichi Mahjong' : 'Japanese (Riichi) Mahjong',
"くまきちファミリーの最高のティータイム (Kmakici Family's Greatest Teatime)":"Kmakici Family's greatest teatime",
'Bao' :'Bao la Kiswahili',
'La Glace et le Ciel':'Ice and the Sky'}

bgg = bgg.replace({'Name': replace_values}) 

#Some other discrepancies. 

"""
Two games in BGG are called 'Solo'. One is called 'Solo Whist' in BGA. 
We make these changes: 
'Solo' 3347 --- 'Solo'
'Solo' 19451 --- 'Solo Whist'
"""

index_solo_whist=bgg[bgg.GameID==19451].index
bgg.at[index_solo_whist,'Name']='Solo Whist'


"""
Two games in BGG are called 'Ninety-Nine'. One is '99 (trick-taking card game)' and the other 
'99 (addition card game)'. The other one "O'NO 99", is not exactly any of them.
"""

index_99_trick_taking=bgg[bgg.GameID==6688].index
bgg.at[index_99_trick_taking,'Name']='99 (trick-taking card game)'

index_99_addition=bgg[bgg.GameID==101420].index
bgg.at[index_99_addition,'Name']='99 (addition card game)'


"""
We have two games from BGA that are closer to the same game in BGG
So we want that the two games share the same info from BGG.

'Pitch'--- 'Phat'
'Pitch'--- 'Caribbean All Fours'
'Belote'---'Coinche'  (there is another Belote!)
"""

index_1=bga[bga.Name=='Phat'].index
index_2=bga[bga.Name=='Caribbean All Fours'].index
index_3=bgg[bgg.Name=='Pitch'].index

index_4=bga[bga.Name=='Coinche'].index
index_5=bgg[bgg.Name=='Belote'].index

bgg_temp=bgg.drop(['Name'],axis=1)

#These are the new rows that we have to append
bgg_pitch_1=pd.concat([bga.iloc[index_1].reset_index(drop = True),bgg_temp.iloc[index_3].reset_index(drop = True)],axis=1)
bgg_pitch_2=pd.concat([bga.iloc[index_2].reset_index(drop = True),bgg_temp.iloc[index_3].reset_index(drop = True)],axis=1)
bgg_belote=pd.concat([bga.iloc[index_4].reset_index(drop = True),bgg_temp.iloc[index_5].reset_index(drop = True)],axis=1)

#We merge the two databases
bga_and_bgg=pd.merge(bga,bgg,on='Name')

#we append the modified rows 
bga_and_bgg=bga_and_bgg.append(bgg_pitch_1, ignore_index=True)
bga_and_bgg=bga_and_bgg.append(bgg_pitch_2, ignore_index=True)
bga_and_bgg=bga_and_bgg.append(bgg_belote, ignore_index=True)


#we look the games that are missing
bga_1=bga[~bga.Name.isin(bga_and_bgg.Name)]
bga_2=bga_1.Name.tolist()

bgg_1=bgg[~bgg.Name.isin(bga_and_bgg.Name)]
bgg_2=bgg_1.Name.tolist()

print('Games that appear in our BGA table but no in the BGG one:')
print(bga_2)
print('Games that appear in our BGG table but no in the BGA one:')
print(bgg_2)

#We can use these information to manually change names, add ids in the file id.txt or see if there is another problem. 

#We save the merge databases.
bga_and_bgg.to_csv('BGA_BGG_complete.csv')
