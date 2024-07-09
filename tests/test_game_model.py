"""Game model tests."""

#    python -m unittest test_game_model.py

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Game

os.environ["DATABASE_URL"] = "postgresql:///geominds_test"

from app import app



class GameModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        u1 = User(username="testuser", team="1", name="Test User", password="password")
        uid1 = 1111
        u1.id = uid1
        db.session.add(u1)
        db.session.commit()

        self.u1 = u1
        self.uid1 = uid1

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_create_game(self):
        """Test creating a game session."""

        game = Game(user_id=self.uid1, score=10, difficulty="2")
        gid = 1234
        game.id = gid
        db.session.add(game)
        db.session.commit()

        game = Game.query.get(gid)
        self.assertIsNotNone(game)
        self.assertEqual(game.user_id, self.uid1)
        self.assertEqual(game.score, 10)
        self.assertEqual(game.difficulty, "2")

    def test_game_relationships(self):
        """Test game and user relationships."""

        game = Game(user_id=self.uid1, score=20, difficulty="3")
        db.session.add(game)
        db.session.commit()

        game = Game.query.filter_by(user_id=self.uid1).first()
        self.assertIsNotNone(game)
        self.assertEqual(game.user.id, self.uid1)
        self.assertEqual(game.user.username, "testuser")

