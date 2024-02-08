from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    
    def test_home_page(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Start Boggle Game</h1>', html)

    def test_start_form(self):
        with app.test_client() as client:
            res = client.post("/start")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)

    def test_board(self):
        with app.test_client() as client:
            res = client.get("/board")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
