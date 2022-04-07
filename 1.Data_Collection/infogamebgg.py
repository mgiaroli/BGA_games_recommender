"""

Functions that allow us get information from a game using its BGG id.
We use lxml to scrape the data in xml format.

"""

from time import sleep
import requests
from lxml import etree



def req(url, sec=10):
    """Function to make tolerant server requests."""
    status_code = 500
    while status_code != 200:
        sleep(sec)
        try:
            result = requests.get(url)
            status_code = result.status_code
            if status_code != 200:
                print("Error - Response Code %i - Retrying" % (result.status_code))
        except: #Exception, probably loss of connection
            print("Exception occurred - Check connection! - Waiting three seconds")
            sleep(3)
    return result


def info_game(id_number):
    """Function that recopiles info from BGG using its id"""
    url='https://www.boardgamegeek.com/xmlapi2/thing?id='+str(id_number)+'&stats=1'
    result = req(url)
    root=etree.fromstring(result.content)
    game = root.find("item[@type='boardgame']")
    if game is not None:
        #we will return a dictionary for each game
        info={}
        info['Name']=game.find('name',{'type':'primary'}).get('value')
        info['GameID']=id_number
        try:
            info['Thumbnail']=game.find('thumbnail').text
        except:
            print(str(id_number) + ' falta la imagen')
        info['Description']=game.find('description').text
        info['Year']=int(game.find('yearpublished').get('value'))
        info['Min_players']=int(game.find('minplayers').get('value'))
        info['Max_players']=int(game.find('maxplayers').get('value'))
        info['Playing_time']=int(game.find('playingtime').get('value'))
        #we create a column for each category, 1 if corresponds to the game
        for key in game.findall("link[@type='boardgamecategory']"):
            info['Category: '+key.get('value')]=1
        #we create a column for each mechanic, 1 if corresponds to the game
        for key in game.findall("link[@type='boardgamemechanic']"):
            info['Mechanic: '+key.get('value')]=1
        info['Designer']=[item.get('value') for item in game.findall("link[@type='boardgamedesigner']")]
        info['Artist']=[item.get('value') for item in game.findall("link[@type='boardgameartist']")]
        stats=game.find('statistics')
        ratings=stats.find('ratings')
        info['Average_rating']=ratings.find('average').get('value')
        info['Users_rated']=ratings.find('usersrated').get('value')
        info['Bayes_average_rating']=ratings.find('bayesaverage').get('value')
        info['Average_weight']=ratings.find('averageweight').get('value')
        return info
    return 'Chequear '+str(id_number)
    