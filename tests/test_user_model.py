"""User model tests."""

#    python -m unittest test_user_model.py

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
from unittest import TestCase
from sqlalchemy import exc
from datetime import datetime 

from models import db, User

os.environ["DATABASE_URL"] = "postgresql:///geominds_test"

from app import app


class UserModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before any tests."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.drop_all()
        db.create_all()

    def setUp(self):
        """Runs before each test."""
        self.client = app.test_client()
        self._create_sample_user()

    def tearDown(self):
        """Runs after each test."""
        db.session.rollback()

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests."""
        db.session.remove()
        db.drop_all()

    def _create_sample_user(self):
        """Helper method to create a sample user."""
        user = User(
            username="testuser",
            team="2",
            name="Test User",
            password="password",
            createdAt=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()

    def test_signup_new_user(self):
        """Test signup of a new user."""
        user = User.signup(
            username="newuser",
            team="3",
            name="New User",
            password="password",
        )
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.team, "3")
        self.assertEqual(user.name, "New User")



if __name__ == '__main__':
    unittest.main()