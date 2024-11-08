from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """ Setup for the testing """
        app.config['TESTING'] = True
    
    def test_homepage(self):
        """ Test homepage """
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('board', session) 

    def test_valid_word(self):
        """ Test if a word is valid based on a sample board """
        with app.test_client() as client:
            # Game is a valid word
            with client.session_transaction() as current_session:
                current_session['board'] = [['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S']]
                
                resp = self.client.get('/check-word?word=games')
                self.assertEqual(resp.json['result', 'ok'])

    def test_invalid_real_word(self):
        """ Test if a word is valid but not on a the sample board """
        with app.test_client() as client:
            # Game is a valid word
            with client.session_transaction() as current_session:
                current_session['board'] = [['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S']]
                
                resp = self.client.get('/check-word?word=that')
                self.assertEqual(resp.json['result', 'not-on-board'])

                self.assertEqual(resp.status_code, 200)
    
    def test_if_real_word(self):
        """ Checks to see if in the dictionary """
        with app.test_client() as client:
            # made up word shouldn't be in dictionary
            with client.session_transaction() as current_session:
                current_session['board'] = [['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S'],
                                            ['G', 'A', 'M', 'E', 'S']]
                
                resp = self.client.get('/check-word?word=asdfg')
                self.assertEqual(resp.json['result', 'not-word'])

                self.assertEqual(resp.status_code, 200)
    
