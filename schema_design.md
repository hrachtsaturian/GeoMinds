```
Users
-----
id PK int IDENTITY
username string UNIQUE 
name string 
password string UNIQUE 
total_score int
createdAt dateTime default=GETUTCDATE()

Games
-----
- id PK int IDENTITY
user_id int FK >- Users.id 
score int
difficulty string default=easy
createdAt dateTime default=GETUTCDATE()

Questions 
-----
id PK int IDENTITY
game_id int FK >- Games.id
correct_choice_id int FK >- Choices.id
question_text string

Choices
-----
id PK int IDENTITY
question_id int FK >- Questions.id
choice_text string

User_answers
-----
id PK int IDENTITY
user_id int FK >- Users.id
game_id int FK >- Games.id
question_id int FK >- Questions.id
choice_id int FK >- Choices.id
createdAt dateTime default=GETUTCDATE()
```