import re
import os
import requests
from db_manager import Base
from sqlalchemy import Column, Integer, String, Boolean

# 3 endpoints
# Landing page displays the scoreboard: all game links
# Second endpoint -- add scoreboard number to URL to see today's games
# 3rd endpoint - add game id to URL to see boxscore
# URLs:
# https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json
# https://cdn.nba.com/static/json/liveData/boxscore/boxscore_0042200123.json

class Scoreboard(Base):
    __tablename__ = 'scoreboards'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)

    def __init__(self, url):
        self.url = url

    def scrape(self):
        # scrape the scoreboard URL and instantiate a list of Game objects
        headers = {'User-Agent': 'Mozilla/5.0'}
        #headers={'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-30332-sp23'))}
        response = requests.get(self.url, headers=headers)
        data= response.json()['scoreboard']['games']
        self.games = [Game(game['gameId'], game['gameCode'], game['gameStatusText'], game['seriesGameNumber'], game['seriesText'], game['seriesConference'], game['poRoundDesc'], game['homeTeam'], game['awayTeam'], game['gameLeaders']) for game in data]

    def display(self):
        # return a tuple with the scoreboard URL and a list of Games you want to display
        display_list = []
        self.scrape()
        for game in self.games:
            display_list.append(game)
        return self.url, display_list

    def __repr__(self) -> str:
        return super().__repr__()

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)

    def __init__(self, id, code, statustext, game_num, seriestext, conf, round, home, away, leaders) -> None:
        self.gameId = id
        self.gameCode = code
        self.statustext = statustext
        self.gameNumber = game_num
        self.seriestext = seriestext
        self.conf = conf
        self.round = round

        self.homeCity = home['teamCity']
        self.awayCity = away['teamCity']
        self.homeName = home['teamName']
        self.awayName = away['teamName']
        self.awaySeed = away['seed']
        self.homeSeed = home['seed']
        self.awayScore = away['score']
        self.homeScore = home['score']
        self.awayQ1 = away['periods'][0]['score']
        self.awayQ2 = away['periods'][1]['score']
        self.awayQ3=away['periods'][2]['score']
        self.awayQ4=away['periods'][3]['score']
        self.homeQ1=home['periods'][0]['score']
        self.homeQ2=home['periods'][1]['score']
        self.homeQ3=home['periods'][2]['score']
        self.homeQ4=home['periods'][3]['score']
        if away['inBonus'] == '0':
            self.awayBonus = 'No'
        else:
            self.awayBonus = 'Yes'
        if home['inBonus'] == '0':
            self.homeBonus = 'No'
        else:
            self.homeBonus = 'Yes'
        self.homeTimeouts = home['timeoutsRemaining']
        self.awayTimeouts = away['timeoutsRemaining']
        self.leadersH = leaders["homeLeaders"]["name"]
        self.leaderPosH = leaders["homeLeaders"]["position"]
        self.leaderPTSH = leaders["homeLeaders"]['points']
        self.leaderREBH = leaders["homeLeaders"]['rebounds']
        self.leaderASTH = leaders['homeLeaders']['assists']
        self.leadersA = leaders["awayLeaders"]["name"]
        self.leaderPosA= leaders["awayLeaders"]["position"]
        self.leaderPTSA = leaders["awayLeaders"]['points']
        self.leaderREBA = leaders["awayLeaders"]['rebounds']
        self.leaderASTA = leaders['awayLeaders']['assists']
       
        self.header = f'{self.awaySeed} {self.awayCity} {self.awayName} @ {self.homeSeed} {self.homeCity} {self.homeName}'
        self.body = f'{self.conf} {self.round} {self.gameNumber}:'
        self.status = f'Game Status: {self.statustext}'
        self.score = f'Score: {self.awayName} {self.awayScore} - {self.homeName} {self.homeScore}'
        self.awayByQuarter=f'{self.awayName} by quarter: Q1: {self.awayQ1}, Q2: {self.awayQ2}, Q3: {self.awayQ3}, Q4: {self.awayQ4}'
        self.homeByQuarter=f'{self.homeName} by quarter: Q1: {self.homeQ1}, Q2: {self.homeQ2}, Q3: {self.homeQ3}, Q4: {self.homeQ4}'
        self.timeoutsA=f'{self.awayName} timeouts remaining: {self.awayTimeouts}'
        self.timeoutsH=f'{self.homeName} timeouts remaining: {self.homeTimeouts}'
        self.bonusA =f'{self.awayName} in the bonus: {self.awayBonus}'
        self.bonusH=f'{self.homeName} in the bonus: {self.homeBonus}'
        self.awayLeaderStats=f'Away Leader: {self.leadersA} points--{self.leaderPTSA} rebounds--{self.leaderREBA} assists--{self.leaderASTA}'
        self.homeLeaderStats=f'Home Leader: {self.leadersH} points--{self.leaderPTSH} rebounds--{self.leaderREBH} assists--{self.leaderASTH}'

    def display(self):
        # return a boxscore object
        self.boxscore = Boxscore(self.gameId)
        return self.boxscore

    def __repr__(self) -> str:
        return super().__repr__()

class Boxscore(Base):
    __tablename__ = 'boxscore'
    id = Column(Integer, primary_key = True)
    url = Column(String, unique=True)

    def __init__(self, id):
        self.gameId = id
        #self.url = 'https://cdn.nba.com/static/json/liveData/boxscore/boxscore_0042200123.json'
        self.url = 'https://cdn.nba.com/static/json/liveData/boxscore/boxscore_' + id + '.json'
        self.game_started = True
        self.not_started = 'This game has not yet started. This page will be updated following tip-off...'

        try:
            self.scrape()
        except:
            self.data = {}

    def scrape(self) -> None:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            self.data = response.json()["game"]
            self.homeTeam = self.data["homeTeam"]["teamName"]
            self.awayTeam = self.data["awayTeam"]["teamName"]
        else:
            self.data = {}
            self.game_started = False

    def __repr__(self) -> str:
        return super().__repr__()

#class Team():

#class Player():