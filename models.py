"""SQLAlchemy models for 'GeoMinds'."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Enum

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    team = db.Column(Enum("1", "2", "3", "4", name="team"), nullable=False, default="1")
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    games = db.relationship("Game", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}"

    @classmethod
    def signup(cls, username, team, name, password):
        """
        Sign up user.
        Hashes password and adds user to the system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(username=username, team=team, name=name, password=hashed_pwd)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """
        Find already-existing user with `username` and `password`.
        If it can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Game(db.Model):
    """Game session started."""

    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    score = db.Column(db.Integer, default=0)
    difficulty = db.Column(
        Enum("1", "2", "3", name="difficulty_levels"), nullable=False, default="1"
    )
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User")
    questions = db.relationship(
        "Question", back_populates="game", cascade="all, delete-orphan"
    )


class Question(db.Model):
    """Questions in the system."""

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id", ondelete="cascade"))
    correct_choice_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "choices.id", ondelete="cascade", name="fk_question_correct_choice"
        ),
    )
    question_text = db.Column(db.Text, nullable=False)

    game = db.relationship("Game")
    choices = db.relationship(
        "Choice",
        back_populates="question",
        cascade="all, delete-orphan",
        foreign_keys="Choice.question_id",
    )
    user_answer = db.relationship(
        "UserAnswer",
        uselist=False,
        back_populates="question",
        cascade="all, delete-orphan",
        foreign_keys="UserAnswer.question_id",
    )


class Choice(db.Model):
    """Choices for the questions."""

    __tablename__ = "choices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.id", ondelete="cascade", name="fk_choice_question"),
    )
    choice_text = db.Column(db.Text, nullable=False)

    question = db.relationship("Question", foreign_keys=[question_id])


class UserAnswer(db.Model):
    """Answers of the users."""

    __tablename__ = "user_answers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    game_id = db.Column(db.Integer, db.ForeignKey("games.id", ondelete="cascade"))
    question_id = db.Column(
        db.Integer, db.ForeignKey("questions.id", ondelete="cascade"), unique=True
    )
    choice_id = db.Column(db.Integer, db.ForeignKey("choices.id", ondelete="cascade"))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", foreign_keys=[user_id])
    game = db.relationship("Game", foreign_keys=[game_id])
    question = db.relationship("Question", foreign_keys=[question_id])
    choice = db.relationship("Choice", foreign_keys=[choice_id])


def connect_db(app):
    """Connect this database to our Flask app"""

    db.app = app
    db.init_app(app)
