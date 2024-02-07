from flask import Flask, render_template, session, redirect, request, jsonify
from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ajeifjaifjaeofjd'

boggle_game = Boggle()
    
val = ''

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/start", methods=["POST"])
def start_game():
    session['board'] = boggle_game.make_board()
    return redirect("/board")

@app.route("/board", methods=["POST"])
def board():
    return render_template("board.html", board=session.get('board'))

@app.route("/submit-guess")
def submit_guess():
    val = boggle_game.check_valid_word(session.get('board'), request.args['guess'])
    return jsonify({'result': val})

@app.route("/post-score", methods=["POST"])
def post_score():
    score = request.json["score"]
    return jsonify({'highscore':score})