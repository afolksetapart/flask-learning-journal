from flask import Flask, g, render_template, flash
from flask_login import LoginManager, current_user, login_required

import forms
import models


app = Flask(__name__)
app.secret_key = '#^354635^#&#%^TEHGDEH^%Y3637tehgd'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    g.db = models.db
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
def index():
    return render_template('index.html')


@app.route('/entries/<int:id>')
def detail(id):
    entry = models.Entry.get(models.Entry.id == id)
    return render_template('detail.html', entry=entry)


@app.route('/login')
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        # validate credentials
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/entries/<int:id>/edit')
@login_required
def edit_post(id):
    entry = models.Entry.get(models.Entry.id == id)
    return render_template('edit.html', entry=entry)


@app.route('/add', methods=('GET', 'POST'))
@login_required
def add_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        new_post = models.Entry.create(
            title=form.title.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resources=form.resources.data
        )
        return redirect(url_for('detail', id=new_post.id))
    return render_template('new.html', form=form)


if __name__ == '__main__':
    models.initialize()
    models.Entry.create(
        title='My First Entry',
        time_spent=30,
        learned='a whole lot!'
    )
    app.run(debug=True)
