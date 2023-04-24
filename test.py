import re
import os
import requests
from db_manager import Base
from sqlalchemy import Column, Integer, String, Boolean

url = 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
data = response.json()['scoreboard']['games']
for game in data:
    gameID =game['gameId']
    print(gameID)
    print(game['homeTeam']['teamName'])
    #box_url = 'https://cdn.nba.com/static/json/liveData/boxscore/boxscore_0042200125.json'
    box_url = 'https://cdn.nba.com/static/json/liveData/boxscore/boxscore_' + gameID + '.json'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(box_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data['game']['gameCode'])
    else:
        print('Game has not started!')
    #data = response.json()
    #print(data['game']['gameCode'])