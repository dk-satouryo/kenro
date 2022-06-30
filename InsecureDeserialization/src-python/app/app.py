#!/usr/bin/python

import os
import pickle
import functools
import base64
import urllib
from flask import Flask, request, render_template, make_response

# pickle 等の危険なライブラリを外部からの信頼できない入力に使うのは避け、
# JSON や YAML 等のフォーマットを利用するように書き換えてみましょう。
# 注意: pickle 等が利用されている場合は不正答判定となります。

app = Flask(__name__)


def decode(preference_str):
    if preference_str != "":
        return pickle.loads(base64.b64decode(preference_str))
    else:
        return {}


def encode(preference):
    return base64.b64encode(pickle.dumps(preference)).decode()


def preference(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        try:
            p_raw = request.cookies.get("preference", "")
            preference = decode(urllib.parse.unquote(p_raw))

            if "color" not in preference:
                preference["color"] = "red"

            return method(preference, *args, **kwargs)

        except Exception as e:
            return "エラーが発生しました: " + str(e), 500

    return wrapper


@app.route("/settings", methods=["GET", "POST"])
@preference
def settings(preference):
    if request.method == "POST":
        if "color" in request.form and request.form["color"] in ["red", "blue"]:
            preference["color"] = request.form["color"]

    response = make_response(render_template("settings.html", preference=preference))

    # 注意: Cookie 中の値の文字種は RFC6265 などにより制限されています。
    # 参考: https://tools.ietf.org/html/rfc6265#section-4.1.1
    response.set_cookie("preference", value=urllib.parse.quote(encode(preference)))
    return response


@app.route("/", methods=["GET"])
@preference
def index(preference):
    items = [
        {
            "name": "ラーメン",
            "description": "麺にとことんこだわって作った醤油ラーメンです。",
            "by": "ふらっとカンパニー",
        },
        {
            "name": "ジンギスカン",
            "description": "北海道のソウルフードをご自宅でお楽しみいただけます。",
            "by": "ふらっと農場",
        },
        {
            "name": "とうもろこし",
            "description": "自然の恵みを直接お届け！24 本セットです。",
            "by": "ふらっと直売所",
        },
    ]
    response = make_response(
        render_template("index.html", preference=preference, items=items)
    )

    # 注意: Cookie 中の値の文字種は RFC6265 などにより制限されています。
    # 参考: https://tools.ietf.org/html/rfc6265#section-4.1.1
    response.set_cookie("preference", value=urllib.parse.quote(encode(preference)))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
