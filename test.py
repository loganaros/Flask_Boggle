from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_home_page(self):
        with self.client as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Start Boggle Game</h1>', html)

    def test_start_form(self):
        with self.client as client:
            res = client.post("/start")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)

    def test_board(self):
        with self.client as client:
            res = client.get("/board")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('plays'))

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        
        res = self.client.get('submit-guess?guess=cat')
        self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        self.client.get('/board')
        res = self.client.get('/submit-guess?guess=aiejoqijejof')
        self.assertEqual(res.json['result'], 'not-word')

    def test_wrong_word(self):
        self.client.get('/board')
        res = self.client.get('/submit-guess?guess=pardon')
        self.assertEqual(res.json['result'], 'not-on-board')