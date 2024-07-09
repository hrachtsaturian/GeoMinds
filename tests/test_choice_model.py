"""Choice model tests."""

#    python -m unittest test_choice_model.py

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Game, Question, Choice

os.environ["DATABASE_URL"] = "postgresql:///geominds_test"

from app import app



class ChoiceModelTestCase(TestCase):

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

        q1 = Question(game_id=gid1, question_text="What is the capital of France?")
        qid1 = 3333
        q1.id = qid1
        db.session.add(q1)
        db.session.commit()

        self.u1 = u1
        self.uid1 = uid1
        self.g1 = g1
        self.gid1 = gid1
        self.q1 = q1
        self.qid1 = qid1

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_create_choice(self):
        """Test creating a choice."""

        c1 = Choice(question_id=self.qid1, choice_text="Paris")
        cid1 = 4444
        c1.id = cid1
        db.session.add(c1)
        db.session.commit()

        choice = Choice.query.get(cid1)
        self.assertIsNotNone(choice)
        self.assertEqual(choice.question_id, self.qid1)
        self.assertEqual(choice.choice_text, "Paris")


    def test_choice_relationships(self):
        """Test choice and question relationships."""

        c1 = Choice(question_id=self.qid1, choice_text="Berlin")
        db.session.add(c1)
        db.session.commit()

        choice = Choice.query.filter_by(question_id=self.qid1).first()
        self.assertIsNotNone(choice)
        self.assertEqual(choice.question.id, self.qid1)
        self.assertEqual(
            choice.question.question_text, "What is the capital of France?"
        )

    def test_invalid_choice_creation(self):
        """Test invalid choice creation scenarios."""

        # Invalid choice with non-existing question_id
        with self.assertRaises(exc.IntegrityError) as context:
            invalid_choice = Choice(question_id=9999, choice_text="Invalid question ID")
            db.session.add(invalid_choice)
            db.session.commit()
        db.session.rollback()

        # Invalid choice with empty choice_text
        with self.assertRaises(exc.IntegrityError) as context:
            invalid_choice = Choice(question_id=self.qid1, choice_text=None)
            db.session.add(invalid_choice)
            db.session.commit()
        db.session.rollback()


if __name__ == "__main__":
    import unittest

    unittest.main()
