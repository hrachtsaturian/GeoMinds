## GeoMinds: Trivia Game
### Overview
GeoMinds is a geography and countries trivia game that challenges users with multiple-choice questions. Players have 5 minutes to complete the quiz, which consists of questions at varying difficulty levels. Points are awarded based on the difficulty of the questions: 5 points for easy, 7 points for medium, and 10 points for hard. If the time runs out, the game will terminate, and no score will be recorded.

### Tech Stack
#### Front End
- HTML
- CSS
- JavaScript
- jQuery
- Bootstrap
- Jinja
- WTForms
#### Back End
- Python/Flask
- SQLAlchemy
- PostgreSQL
  
### Goal
The main goal of this project is to create an entertaining app where users can participate in a trivia game based on the theme of geography.

### Target Users
The game is designed for a general audience.

### API
The following API is used to fetch trivia questions:

GET - `https://opentdb.com/api.php`

Query params: 
- amount=20 (20 questions)
- category=22 (geography category)
- difficulty=easy (easy, medium, hard)
- type=multiple (4 choices)

### Live Demo
Check out the live demo: GeoMinds on Render

https://geominds.onrender.com

### Project Breakdown
#### Database Models
- User: Represents a user of the game.
- Game: Represents a game session.
- Question: Represents a trivia question.
- Choice: Represents multiple choices for each question.
- UserAnswer: Represents the user's answer to a question.
  
#### RESTful API
- GET `/users/<user_id>` Retrieve user information.
- POST `/games` Create a new game session.
- GET `/games/<game_id>/questions/<question_id>` Retrieve a specific question in a game.
- POST `/games/<game_id>/questions/<question_id>/answers` Submit an answer to a question.
- GET `/games/<game_id>/summary` Retrieve the summary of a game session.
  
#### Functionality Features
- User Authentication/Authorization: Signup and login functionality.
- Game Sessions: Create games, score points, and set up time control.
- Rankings: View the leaderboard sorted by users' scores from highest to lowest.

#### How to run locally
1. Set up PostgreSQL database named `geominds`
  - `CREATE DATABASE geominds;`
2. Install packages (suggested to use Python 3.7)
  - `pip3.7 install -r requirements.txt`
3. Launch flask application
  - `flask run`
4. Navigate to the following URL in your browser
  - `http://127.0.0.1:5000/`
  
###### Enjoy the game and test your geography knowledge!
