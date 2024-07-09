import os

from flask import Flask, render_template, flash, redirect, abort, request, session, g
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import requests
import random
import statistics

from forms import UserAddForm, LoginForm, EditForm
from models import db, connect_db, User, Game, Question, Choice, UserAnswer

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///geominds"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "it's a secret")

connect_db(app)

with app.app_context():
    db.create_all()


##############################################################################
# User & Rankings routes


@app.before_request
def add_user_to_g():
    """If we're logged in, add current user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get((session[CURR_USER_KEY]))

    else:
        g.user = None
        redirect("/")


def do_login(user):
    """Login user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, re-present form.
    If there is already user with that username: flash message and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                name=form.name.data,
                team=form.team.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("users/signup.html", form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template("users/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.
    If form not valid: flash message and re-present form.
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}", "success")
            return redirect("/")

        flash("Invalid credentials", "danger")

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    """Handle user logout."""

    session.pop(CURR_USER_KEY)
    return redirect("/login")


@app.route("/users/<int:user_id>")
def profile(user_id):
    """Show the profile of the user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    team_map = {"1": "Water", "2": "Earth", "3": "Fire", "4": "Air"}
    total_score = sum(
        [
            game.score
            for game in user.games
            if len(game.questions)
            == len(
                [
                    question
                    for question in game.questions
                    if question.user_answer is not None
                ]
            )
        ]
    )
    total_games_played = len(
        [
            game
            for game in user.games
            if len(game.questions)
            == len(
                [
                    question
                    for question in game.questions
                    if question.user_answer is not None
                ]
            )
        ]
    )

    users = User.query.all()
    ranking_list = []
    for ranked_user in users:
        row = {
            "id": ranked_user.id,
            "average_score_per_game": round(
                statistics.mean(
                    [
                        game.score
                        for game in ranked_user.games
                        if len(game.questions)
                        == len(
                            [
                                question
                                for question in game.questions
                                if question.user_answer is not None
                            ]
                        )
                    ]
                    if len(
                        [
                            game
                            for game in ranked_user.games
                            if len(game.questions)
                            == len(
                                [
                                    question
                                    for question in game.questions
                                    if question.user_answer is not None
                                ]
                            )
                        ]
                    )
                    else [0]
                )
            ),
        }
        ranking_list.append(row)

    ranking_list = sorted(
        ranking_list, key=lambda x: x["average_score_per_game"], reverse=True
    )
    place = None
    for index, row in enumerate(ranking_list):
        if row.get("id") == user_id:
            place = index + 1

    return render_template(
        "users/profile.html",
        user=user,
        team_map=team_map,
        total_score=total_score,
        total_games_played=total_games_played,
        place=place,
    )


@app.route("/users/edit", methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = EditForm(obj=user)

    if form.validate_on_submit():
        if not User.authenticate(user.username, form.password.data):
            flash("Password incorrect!", "danger")
            return redirect("/users/edit")

        try:
            user.username = form.username.data
            user.name = form.name.data
            user.team = form.team.data

            db.session.commit()

            return redirect(f"/users/{user.id}")

        except IntegrityError:
            flash("Invalid input", "danger")
            return redirect("/users/edit")

    else:
        return render_template("users/profile_edit.html", form=form, user_id=user.id)


@app.route("/users/delete", methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


@app.route("/rankings")
def rankings():
    """Show the table of rankings."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    users = User.query.all()
    ranking_list = []
    team_map = {"1": "Water", "2": "Earth", "3": "Fire", "4": "Air"}

    for user in users:
        row = {
            "id": user.id,
            "geomind": user.username,
            "team": team_map.get(user.team),
            "total_score": sum(
                [
                    game.score
                    for game in user.games
                    if len(game.questions)
                    == len(
                        [
                            question
                            for question in game.questions
                            if question.user_answer is not None
                        ]
                    )
                ]
            ),
            "total_games_played": len(
                [
                    game
                    for game in user.games
                    if len(game.questions)
                    == len(
                        [
                            question
                            for question in game.questions
                            if question.user_answer is not None
                        ]
                    )
                ]
            ),
            "average_score_per_game": round(
                statistics.mean(
                    [
                        game.score
                        for game in user.games
                        if len(game.questions)
                        == len(
                            [
                                question
                                for question in game.questions
                                if question.user_answer is not None
                            ]
                        )
                    ]
                    if len(
                        [
                            game
                            for game in user.games
                            if len(game.questions)
                            == len(
                                [
                                    question
                                    for question in game.questions
                                    if question.user_answer is not None
                                ]
                            )
                        ]
                    )
                    else [0]
                )
            ),
        }
        ranking_list.append(row)

    ranking_list = sorted(
        ranking_list, key=lambda x: x["average_score_per_game"], reverse=True
    )
    for index, row in enumerate(ranking_list):
        ranking_list[index]["place"] = index + 1

    return render_template("rankings.html", ranking_list=ranking_list)


@app.route("/")
def homepage():
    """Handle user homepage."""

    return render_template("home.html")


##############################################################################
# Game routes


# FRONT-END route
@app.route("/games/<int:game_id>/questions/<int:question_id>")
def show_game(game_id, question_id):
    "Show the game."

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    game = Game.query.get_or_404(game_id)

    if game.user_id != g.user.id:
        flash("Access forbidden.", "danger")
        return redirect("/")

    answers_count = UserAnswer.query.filter_by(game_id=game_id).count()

    g.is_active_game = True

    current_time = datetime.utcnow()
    if current_time >= game.createdAt + timedelta(seconds=300) and answers_count != len(
        game.questions
    ):
        return render_template("games/timeout.html")

    active_question = next(
        (question for question in game.questions if question.id == question_id), None
    )

    if not active_question:
        abort(404, description="Resource not found")

    unshuffled_choices = Choice.query.filter_by(question_id=question_id).all()
    random.seed(58 * int(question_id))
    choices = unshuffled_choices[:]
    random.shuffle(choices)
    user_answer = UserAnswer.query.filter_by(question_id=question_id).first()

    if not user_answer and answers_count != game.questions.index(active_question):
        abort(400)

    choice_colors = {}

    for choice in choices:
        if not user_answer:
            choice_colors[choice.id] = "btn-outline-primary"
        elif choice.id == active_question.correct_choice_id:
            choice_colors[choice.id] = "btn-success"
        elif choice.id != user_answer.choice_id:
            choice_colors[choice.id] = "btn-outline-primary"
        else:
            choice_colors[choice.id] = "btn-danger"

    if not user_answer:
        return render_template(
            "games/game.html",
            game=game,
            choices=choices,
            active_question=active_question,
            is_answered=False,
            choice_colors=choice_colors,
        )

    is_finished = False
    if answers_count == len(game.questions):
        is_finished = True
        next_url = f"/games/{game_id}/summary"
    else:
        next_question_id = game.questions[game.questions.index(active_question) + 1].id
        next_url = f"/games/{game_id}/questions/{next_question_id}"

    return render_template(
        "games/game.html",
        game=game,
        choices=choices,
        active_question=active_question,
        is_answered=True,
        choice_colors=choice_colors,
        next=next_url,
        is_finished=is_finished,
    )


@app.route("/games/<int:game_id>/summary")
def show_summary(game_id):
    """Show the results after test."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    game = Game.query.get_or_404(game_id)

    answers_count = UserAnswer.query.filter_by(game_id=game_id).count()
    if answers_count != len(game.questions):
        abort(400)

    total_correct_answers = 0

    for question in game.questions:
        if question.correct_choice_id == question.user_answer.choice_id:
            total_correct_answers += 1

        random.seed(58 * int(question.id))
        random.shuffle(question.choices)

    return render_template(
        "games/summary.html", game=game, total_correct_answers=total_correct_answers
    )


# BACK-END route
@app.route("/games", methods=["POST"])
def start_game():
    "Game launch."

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    difficulty = request.form.to_dict().get("difficulty", "1")
    difficulty_dict = {"1": "easy", "2": "medium", "3": "hard"}
    difficulty_name = difficulty_dict.get(difficulty, "easy")

    resp = {}

    try:
        trivia_api_url = f"https://opentdb.com/api.php?amount=20&category=22&difficulty={difficulty_name}&type=multiple"
        resp = requests.get(trivia_api_url).json()
        if resp.get("response_code") != 0:
            raise Exception
    except:
        flash("Something went wrong. Please try again.", "danger")
        return redirect("/")

    new_game = Game(user_id=g.user.id, difficulty=difficulty)
    db.session.add(new_game)
    db.session.commit()

    for el_question in resp.get("results", []):
        new_question = Question(
            game_id=new_game.id, question_text=el_question.get("question", "")
        )
        db.session.add(new_question)
        db.session.commit()

        new_correct_choice = Choice(
            question_id=new_question.id,
            choice_text=el_question.get("correct_answer", ""),
        )
        db.session.add(new_correct_choice)
        db.session.commit()

        new_question.correct_choice_id = new_correct_choice.id
        db.session.add(new_question)

        for el_choice in el_question.get("incorrect_answers", ""):
            new_choice = Choice(question_id=new_question.id, choice_text=el_choice)
            db.session.add(new_choice)

        db.session.commit()

    new_game = Game.query.get(new_game.id)

    return redirect(f"/games/{new_game.id}/questions/{new_game.questions[0].id}")


@app.route("/questions/<int:question_id>/answers", methods=["POST"])
def confirm_answer(question_id):
    """Confirming the answer of user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    question = Question.query.get_or_404(question_id)
    choice_id = request.form.get("choice_id", None)

    answers_count = UserAnswer.query.filter_by(game_id=question.game_id).count()
    if answers_count != question.game.questions.index(question):
        abort(400)

    if str(choice_id) not in [str(choice.id) for choice in question.choices]:
        abort(400)

    new_user_answer = UserAnswer(
        user_id=g.user.id,
        game_id=question.game_id,
        question_id=question_id,
        choice_id=choice_id,
    )

    db.session.add(new_user_answer)
    db.session.commit()

    if new_user_answer.choice_id == question.correct_choice_id:
        game = Game.query.get_or_404(question.game_id)
        score_increment = {"1": 5, "2": 7, "3": 10}
        game.score += score_increment.get(game.difficulty, 0)

        db.session.add(game)
        db.session.commit()

    return redirect(f"/games/{question.game_id}/questions/{question_id}")
