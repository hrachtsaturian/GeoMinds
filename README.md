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

https://opentdb.com/api.php?amount=20&category=22&difficulty={difficulty_name}&type=multiple

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
- GET /users/<user_id>: Retrieve user information.
- POST /games/: Create a new game session.
- GET /games/<game_id>/questions/<question_id>: Retrieve a specific question in a game.
- POST /games/<game_id>/questions/<question_id>/answers: Submit an answer to a question.
- GET /games/<game_id>/summary: Retrieve the summary of a game session.
  
#### Functionality Features
- User Authentication/Authorization: Signup and login functionality.
- Game Sessions: Create games, score points, and set up timers for each game.
- Rankings Management: Create a leaderboard that sorts users by their scores from highest to lowest.
  
###### Enjoy the game and test your geography knowledge!
