from flask import (Flask, g, render_template, flash,
                   redirect, url_for, request, abort)
from flask_login import (LoginManager, current_user,
                         login_required, login_user, logout_user)
from flask_bcrypt import check_password_hash

import forms
import models

# TODO: dependencies file, credentials for first user, comments, pep8
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
    try:
        entry = models.Entry.get(models.Entry.id == id)
        return render_template('detail.html', entry=entry)
    except models.DoesNotExist:
        abort(404)


@app.route('/entries/tagged/<tag>')
def tag_stream(tag):
    posts = models.Entry.select().join(models.Tag).where(
        models.Tag.tag == tag
    )
    if posts.count() == 0:
        abort(404)
    else:
        return render_template('index.html', posts=posts)


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
        user = models.User.get(
            models.User.username == form.username.data
        )
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(
                models.User.username == form.username.data
            )
        except models.DoesNotExist:
            flash(
                ('Sorry! Your username or '
                 'password is incorrect.')
            )
        else:
            if check_password_hash(
                user.password, form.password.data
            ):
                login_user(user)
                flash('Welcome back!')
                return redirect(url_for('index'))
            else:
                flash(
                    ('Sorry! Your username or '
                     'password is incorrect.')
                )
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
            resources=form.resources.data,
            tag_string=form.tag_string.data
        )
        tags = form.tag_string.data.split(',')
        for tag in tags:
            models.Tag.create(
                tag=tag,
                entry=new_post
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
            string_tags = form.tag_string.data.split(',')
            for tag in string_tags:
                tag, created = models.Tag.get_or_create(
                    tag=tag, entry=entry)
            obj_tags = models.Tag.select().where(
                models.Tag.entry == entry
            )
            for tag in obj_tags:
                if tag.tag not in string_tags:
                    tag.delete_instance()
            form.populate_obj(entry)
            entry.save()
            flash('Entery successfully saved!')
            return redirect(url_for('detail', id=entry.id))
    else:
        flash(
            'Sorry! You don\'t have permission to edit this post!'
        )
        return redirect(url_for('detail', id=entry.id))
    return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/<int:id>/delete', methods=('GET', 'POST'))
@ login_required
def delete_post(id):
    entry = models.Entry.get(models.Entry.id == id)
    tags = models.Tag.select().where(models.Tag.entry == entry)
    for tag in tags:
        tag.delete_instance()
    entry.delete_instance()
    flash('Entry successfully deleted!')
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
