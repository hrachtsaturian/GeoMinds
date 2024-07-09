from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=13)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=30)])
    team = SelectField(
        choices=[
            ("", "Choose your team"),
            ("1", "Water"),
            ("2", "Earth"),
            ("3", "Fire"),
            ("4", "Air"),
        ],
        validators=[DataRequired()],
    )
    password = PasswordField("Password", validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Form for login."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class EditForm(FlaskForm):
    """Form for editing user's profile."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=13)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=30)])
    team = SelectField(
        choices=[
            ("", "Choose your team"),
            ("1", "Water"),
            ("2", "Earth"),
            ("3", "Fire"),
            ("4", "Air"),
        ],
        validators=[DataRequired()],
    )
    password = PasswordField("Password", validators=[Length(min=6)])
