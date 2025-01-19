from my_site.app import app, db
from flask import render_template, flash, redirect, url_for, request
from my_site.app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from my_site.app.models import User
import sqlalchemy as sa
from urllib.parse import urlsplit
from datetime import datetime, timezone
from .models import Post
from .forms import PostForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(text=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template("index.html", title='Home', form=form)


# @app.route("/posts/<username>")
# @login_required
# def user_posts(username):
#     user = User.query.filter_by(username=username).first()
#
#     if not user:
#         flash('No user with that username exists.', category='error')
#         return redirect(url_for('home'))
#
#     posts = Post.query.filter_by(author=user.id).all()
#     return render_template("posts.html", user=current_user, posts=posts, username=username)
# def create_post():
#     if request.method == 'POST':
#         text = request.form.get('text')
#         if not text:
#             flash('Say something!', category='error')
#         else:
#             post = Post(text=text, author=current_user.id)
#             db.session.add(post)
#             db.session.commit()
#             flash('Article created successfully', category='success')
#             return redirect(url_for('home'))
#     return render_template('create_posts.html', user=current_user)


#
# @app.route("/posts/<username>")
# @login_required
# def user_posts(username):
#     user = User.query.filter_by(username=username).first()
#
#     if not user:
#         flash('No user with that username exists.', category='error')
#         return redirect(url_for('login'))
#
#     posts = Post.query.filter_by(author=user.id).all()
#     return render_template("posts.html", user=current_user, posts=posts, username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are one of us now!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test1'},
        {'author': user, 'body': 'Test2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Saved!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)