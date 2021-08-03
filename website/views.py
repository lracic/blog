import flask_login
from website import create_database
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask.helpers import flash
from .models import Post
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route('/create-post', methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash("Post cannot be empty", category='error')
        else:
            post = Post(text=text, author=current_user.id)
            print(post.author)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)
