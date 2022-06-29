import os
import uuid
from flask import Flask, request, render_template, redirect, session
from database import db
from models import Post

app = Flask(__name__)

# csrf_token作成
import secrets
import binascii
csrf_token = binascii.hexlify(secrets.token_bytes(32)).decode()




@app.route("/post", methods=["POST"])
def post():
    if "content" not in request.form:
        return "", 400

    ## inputform内のcsrf_tokenがflaskで生成されたものと同一か検証している
    if request.form["csrf_token"] != csrf_token:
        return "", 401

    if "user_id" not in session:
        session["user_id"] = uuid.uuid4().hex

    post = Post(session["user_id"], request.form["content"])
    db.session.add(post)
    db.session.commit()

    return redirect("/")


@app.route("/")
def list():
    if "user_id" not in session:
        session["user_id"] = uuid.uuid4().hex

    posts = db.session.query(Post).filter(Post.user_id == session["user_id"]).all()

    return render_template("index.html", posts=posts, csrf_token=csrf_token)
    ## csrf_tokenをhtmlに渡している,htmlでは{{csrf_token}}で利用可能


def init_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.secret_key = os.urandom(32)
    db.init_app(app)

    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    init_app(app)
    app.run("0.0.0.0", port=int(os.environ.get("PORT", 8080)))
