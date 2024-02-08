from flask import Flask, render_template, session, redirect, request, jsonify
from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ajeifjaifjaeofjd'

boggle_game = Boggle()
    
val = ''

@app.route("/")
def home():
    """Home page that display start button"""

    return render_template("home.html")

@app.route("/start", methods=["POST"])
def start_game():
    """Handles game start ang generates new boggle game board"""
    session['board'] = boggle_game.make_board()
    return redirect("/board")

@app.route("/board", methods=["POST", "GET"])
def board():
    """Main game screen"""
    return render_template("board.html", board=session.get('board'), highscore=session.get('highscore', 0))

@app.route("/submit-guess")
def submit_guess():
    """Handles submitting a guess and checks if the words is valid or not"""
    val = boggle_game.check_valid_word(session.get('board'), request.args['guess'])
    return jsonify({'result': val})

@app.route("/post-score", methods=["POST"])
def post_score():
    """
    Final game score
    Compares score to highscore and sets highscore based on that value
    Records number of plays and updates session with all info
    """
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    session['plays'] = plays + 1

    session['highscore'] = max(score, highscore)

    print(score, highscore, score > highscore)

    return jsonify(newHighScore = score > highscore)