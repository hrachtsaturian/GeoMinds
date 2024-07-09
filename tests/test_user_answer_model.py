"""UserAnswer model tests."""

#    python -m unittest test_user_answer_model.py

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Game, Question, Choice, UserAnswer

os.environ["DATABASE_URL"] = "postgresql:///geominds_test"

from app import app



class UserAnswerModelTestCase(TestCase):

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

        c1 = Choice(question_id=qid1, choice_text="Paris")
        cid1 = 4444
        c1.id = cid1
        db.session.add(c1)
        db.session.commit()

        self.u1 = u1
        self.uid1 = uid1
        self.g1 = g1
        self.gid1 = gid1
        self.q1 = q1
        self.qid1 = qid1
        self.c1 = c1
        self.cid1 = cid1

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_create_user_answer(self):
        """Test creating a user answer."""

        ua1 = UserAnswer(
            user_id=self.uid1,
            game_id=self.gid1,
            question_id=self.qid1,
            choice_id=self.cid1,
        )
        uaid1 = 5555
        ua1.id = uaid1
        db.session.add(ua1)
        db.session.commit()

        user_answer = UserAnswer.query.get(uaid1)
        self.assertIsNotNone(user_answer)
        self.assertEqual(user_answer.user_id, self.uid1)
        self.assertEqual(user_answer.game_id, self.gid1)
        self.assertEqual(user_answer.question_id, self.qid1)
        self.assertEqual(user_answer.choice_id, self.cid1)

    def test_user_answer_relationships(self):
        """Test user answer relationships."""

        ua1 = UserAnswer(
            user_id=self.uid1,
            game_id=self.gid1,
            question_id=self.qid1,
            choice_id=self.cid1,
        )
        db.session.add(ua1)
        db.session.commit()

        user_answer = UserAnswer.query.filter_by(user_id=self.uid1).first()
        self.assertIsNotNone(user_answer)
        self.assertEqual(user_answer.user.id, self.uid1)
        self.assertEqual(user_answer.game.id, self.gid1)
        self.assertEqual(user_answer.question.id, self.qid1)
        self.assertEqual(user_answer.choice.id, self.cid1)

    