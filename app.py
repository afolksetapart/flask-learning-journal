from flask import Flask
from flask_login import LoginManager

import models

app = Flask(__name__)
app.secret_key = '#^354635^#&#%^TEHGDEH^%Y3637tehgd'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

if __name__ == '__main__':
    models.initialize()
    models.Entry.create(
        title='My First Entry',
        time_spent=30,
        learned='a whole lot!'
    )
    app.run(debug=True)
