from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from db_manager import db_session
from nba_classes import Scoreboard, Game, Boxscore
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown

app = Flask(__name__)
Bootstrap(app)
Markdown(app)

scoreboards = None

def check_globals() -> None:
    global scoreboards

    if not scoreboards:
        scoreboards = Scoreboard.query.all()
    
@app.route('/')
def display_scoreboards():
    check_globals()
    return render_template('scoreboards.html', scoreboards=scoreboards)

@app.route('/<int:score_id>/')
def display_games(score_id: int):
    check_globals()
    games_list = scoreboards[int(score_id)].display()[1]
    return render_template('games.html', games=games_list, score_id=score_id)

@app.route('/<int:score_id>/<int:game_id>/')
def display_boxscore(score_id: int, game_id: int):
    check_globals()

    try:
        boxscore = scoreboards[int(score_id)].games[int(game_id)].display()
        return render_template('boxscore.html', boxscore=boxscore)
    except:
        scoreboards[int(score_id)].scrape()
        boxscore = scoreboards[int(score_id)].games[int(game_id)].display()
        return render_template('boxscore.html', boxscore=boxscore)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()