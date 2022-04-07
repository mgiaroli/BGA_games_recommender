# Data Collection

We collected data of the Board Game Arena games from [Board Game Geek (BGG)](https://boardgamegeek.com)

In order to do this task, we use [BGG XML API2](https://boardgamegeek.com/wiki/page/BGG_XML_API2). This API allows us to request information about the boardgames. 

We need the id of the games to retrieve them, so to obtain the ids, we scraped ["Digital Implementations: Board Game Arena"](https://boardgamegeek.com/boardgamefamily/70360/digital-implementations-board-game-arena/linkeditems/boardgamefamily), a list in BGG that contains most of the games in BGA. For this task we used [Selenium](https://selenium-python.readthedocs.io/).

Once we have the ids, we made requests to the BGG API, in xml format, and we parsed the results using the library [lxml](https://lxml.de/). We collected the following information for each game: Name, GameID, Thumbnail, Description, Year, Min_players, Max_players, Playing_time, Designer, Artist, Average_rating, Users_rated, Bayes_average_rating, Averaga_weight, and also the Categories and Mechanics. 

As the game names can differ from the BGA ones, we extracted the names (in [English](https://boardgamearena.com/gamelist?section=all) and in [Spanish](https://es.boardgamearena.com/gamelist?section=all)), and the url directions, from BGA, using the library BeautifulSoup. Then we checked for discrepancies between the two datasets, we checked for missing/extra items, and finally we merged the data from BGG and BGA into one file with all the collected data.

The other files in this folder are:

- gameids.py - Script to collect the games ids.
- ids.txt - File with the games ids.
- infogamebgg.py - Script with functions to retrieve information from the BGG API for one game using its BGG id.
- bgg.py -Script to collect the data from the BGG API, using infogamebgg.py.
- BGG.csv - Data from BGG API.
- updatebgg.py - Script to update the data from BGG, when there are new games ids.
- namesbga.py - Script to extract games names from BGA.
- BGA.csv - Data from BGA.
- merge.py - Script to merge BGG.csv and BGA.csv
- BGA_BGG_complete.csv - The merged data.
