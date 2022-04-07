"""

This file collect the Board Game Geek Id of the Board Game Arena games.

"""

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

def get_games_ids(pages):
    '''
    This function is used to get the ids of the games, scraping the data from
    https://boardgamegeek.com/boardgamefamily/70360/digital-implementations-board-game-arena/linkeditems/boardgamefamily
    Currently (April 5 2022) there are 18 pages. Each page has 25 games
    (except maybe the last one, which has less).
    The loop will loop through page by page and game by game, to collect the ids.
    We use selenium. We write the ids in the file ids.txt
    '''
    ids=[]
    
    for page in range(pages):
        number = str(page+1)
        webdriver_path = '/home/maggie/BGA_games_recommender/chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        browser = webdriver.Chrome(webdriver_path,chrome_options=options)
        browser.get("https://boardgamegeek.com/boardgamefamily/70360/digital-implementations-board-game-arena/linkeditems/boardgamefamily?pageid="+number)
        sleep(2)
        result= BeautifulSoup(browser.page_source, "html.parser")
        games=result.find_all('div', class_='summary-item-title summary-item-title-separated')
        for game in games:
            url=game.find('a',href=True).get('href')
            ids.append(url.split('/')[-2])
        print(number)
        browser.quit()
    with open("ids.txt", "w") as file:
        for item in ids:
            file.write("%s\n" % item)
    return ids


def update_game_ids(pages):
    """
    This functions is used to update the file that contains the ids of 
    the games. It does the same as get_games_ids, but add the new ids in the
    old file ids.txt
    """
    with open('ids.txt') as file:
        ids=file.read().splitlines()
    new_ids=[]
    for page in range(pages):
        number = str(page+1)
        webdriver_path = '/home/maggie/bga/chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        browser = webdriver.Chrome(webdriver_path,chrome_options=options)
        try:
            browser.get("https://boardgamegeek.com/boardgamefamily/70360/digital-implementations-board-game-arena/linkeditems/boardgamefamily?pageid="+number)
            sleep(2)
            result= BeautifulSoup(browser.page_source, "html.parser")
            games=result.find_all('div', class_='summary-item-title summary-item-title-separated')
            for game in games:
                url=game.find('a',href=True).get('href')
                if url.split('/')[-2] not in ids:
                    new_ids.append(url.split('/')[-2])
            print(number)
            browser.quit()
        except:
            print('Something goes wrong - Page number '+number)
    with open("ids.txt", "a") as file:
        for item in new_ids:
            file.write("%s\n" % item)
    print(new_ids)
    return ids+new_ids


#---there are 18 pages now
update_game_ids(18)
