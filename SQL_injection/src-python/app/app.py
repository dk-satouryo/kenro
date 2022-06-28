import os
import uuid
from flask import Flask, request, render_template, session
from database import db
from models import Post

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/post", methods=["POST"])
def post():
    if "title" not in request.form or "content" not in request.form:
        return "", 500

    if "uid" not in session:
        session["uid"] = uuid.uuid4().hex

    post = Post(session["uid"], request.form["title"], request.form["content"])
    db.session.add(post)
    db.session.commit()

    return index()


@app.route("/search")
def search():
    if "uid" not in session:
        session["uid"] = uuid.uuid4().hex

    title = request.args.get("title", "")

    # 問題点：生のSQLを使っている点に問題あり
    # q = "SELECT * FROM `posts` WHERE `title` LIKE '%{}%' AND `uid` = '{}'".format(
    #     title, session["uid"]
    # )
    # posts = list(db.session.execute(q))
    posts = (
        db.session.query(Post)
        .filter(Post.title == title and Post.uid == session["uid"])
        .all()
    )
    return render_template("search.html", keyword=title, posts=posts, count=len(posts))


@app.route("/")
def index():
    if "uid" not in session:
        session["uid"] = uuid.uuid4().hex
    posts = db.session.query(Post).filter(Post.uid == session["uid"]).all()
    return render_template("index.html", posts=posts, count=len(posts))


if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.secret_key = os.urandom(32)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run("0.0.0.0", port=int(os.environ.get("PORT", 8080)))
