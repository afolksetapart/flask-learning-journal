# Learning Journal
### A Journal App Built with Flask

Learning Journal is a basic journal application that allows users to:

- Create a secure account and password
- Log the amount of time spent learning a particular subject
- Keep track of helpful resources found along the way
- Write about what they've learned in their own words
- Organize journal entries by tags

## In Use

*This project requires you to have pipenv installed*

Install all project dependencies by navigating to the route directory and running:
```
pipenv install
```

Next, run **app.py** from the root directory with:
```
$ python3 app.py
```

The app will start a local server on **Port 5000**

If you'd like, login with the following credentials to edit or delete the existing post:
- username: test_user
- password: secret00

## Built With

- Python
- Flask
- Peewee
- WTForms
- BCrypt
