"""Question model tests."""

#    python -m unittest test_question_model.py

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Game, Question

os.environ["DATABASE_URL"] = "postgresql:///geominds_test"

from app import app



class QuestionModelTestCase(TestCase):

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

        g1 = Game(user_id=uid1, score=0, difficulty="1")
        gid1 = 2222
        g1.id = gid1
        db.session.add(g1)
        db.session.commit()

        self.u1 = u1
        self.uid1 = uid1
        self.g1 = g1
        self.gid1 = gid1

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_create_question(self):
        """Test creating a question."""

        q1 = Question(game_id=self.gid1, question_text="What is the capital of France?")
        qid1 = 3333
        q1.id = qid1
        db.session.add(q1)
        db.session.commit()

        question = Question.query.get(qid1)
        self.assertIsNotNone(question)
        self.assertEqual(question.game_id, self.gid1)
        self.assertEqual(question.question_text, "What is the capital of France?")

    def test_question_relationships(self):
        """Test question and game relationships."""

        q1 = Question(
            game_id=self.gid1, question_text="What is the capital of Germany?"
        )
        db.session.add(q1)
        db.session.commit()

        question = Question.query.filter_by(game_id=self.gid1).first()
        self.assertIsNotNone(question)
        self.assertEqual(question.game.id, self.gid1)
        self.assertEqual(question.game.user.id, self.uid1)

    def test_invalid_question_creation(self):
        """Test invalid question creation scenarios."""

        # Invalid question with non-existing game_id
        with self.assertRaises(exc.IntegrityError) as context:
            invalid_question = Question(game_id=9999, question_text="Invalid game ID")
            db.session.add(invalid_question)
            db.session.commit()
        db.session.rollback()

        # Invalid question with empty question_text
        with self.assertRaises(exc.IntegrityError) as context:
            invalid_question = Question(game_id=self.gid1, question_text=None)
            db.session.add(invalid_question)
            db.session.commit()
        db.session.rollback()


if __name__ == "__main__":
    import unittest

    unittest.main()
