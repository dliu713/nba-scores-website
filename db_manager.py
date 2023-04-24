# db_manager.py

import csv
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

#create an engine for your DB using sqlite and storing it in a file named reddit.sqlite
engine = create_engine("sqlite:///nba.sqlite", echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db(): # 15 LOC

    # import your classes that represent tables in the DB and then create_all of the tables
    from nba_classes import Scoreboard
    Base.metadata.create_all(bind=engine)

    # read in the games from the scoreboard url and add them to your database by creating Game objects

    scoreboard_url = 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'
    scoreboard = Scoreboard(scoreboard_url)
    db_session.add(scoreboard)
    db_session.commit()
