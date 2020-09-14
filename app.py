from flask import Flask, g, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_bcrypt import check_password_hash

import forms
import models

# TODO: display flashed messages, associate users and posts,
# only let user edit own posts

app = Flask(__name__)
app.secret_key = '#^354635^#&#%^TEHGDEH^%Y3637tehgd'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    try:
        return models.User.get(models.User.id == id)
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
    posts = models.Entry.select()
    return render_template('index.html', posts=posts)


@app.route('/entries/<int:id>')
def detail(id):
    entry = models.Entry.get(models.Entry.id == id)
    return render_template('detail.html', entry=entry)


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash('Registration successful!')
        models.User.make_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        user = models.User.get(models.User.username == form.username.data)
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash('Sorry! Your username or password is incorrect.')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Welcome back!')
                return redirect(url_for('index'))
            else:
                flash('Sorry! Your username or password is incorrect.')
    return render_template('login.html', form=form)


@ app.route('/logout')
@ login_required
def logout():
    logout_user()
    flash('You\'ve been successfully logged out!')
    return redirect(url_for('index'))


@ app.route('/entries/new', methods=('GET', 'POST'))
@ login_required
def add_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        new_post = models.Entry.create(
            title=form.title.data,
            user=g.user.id,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resources=form.resources.data
        )
        return redirect(url_for('detail', id=new_post.id))
    return render_template('new.html', form=form)


@ app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
@ login_required
def edit_post(id):
    entry = models.Entry.get(models.Entry.id == id)
    if g.user == entry.user:
        form = forms.EntryForm(obj=entry)
        if form.validate_on_submit():
            form.populate_obj(entry)
            entry.save()
            flash('Entery successfully saved!')
            return redirect(url_for('detail', id=entry.id))
    else:
        flash('Sorry! You don\'t have permission to edit this post!')
        return redirect(url_for('detail', id=entry.id))
    return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/<int:id>/delete', methods=('GET', 'POST'))
@ login_required
def delete_post(id):
    entry = models.Entry.get(models.Entry.id == id)
    entry.delete_instance()
    flash('Entry successfully deleted!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
