#!/usr/bin/python

import os
import glob
from flask import Flask, jsonify, request, render_template, make_response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/list")
def get_list():
    # /app/files 以下のファイル一覧を取得する
    files_raw = [
        f for f in glob.glob("/app/files/**/*", recursive=True) if os.path.isfile(f)
    ]

    # files 中の各ファイルパスから `/app/files` を除去する
    files = list(map(lambda x: x.replace("/app/files/", ""), files_raw))

    # JSON としてファイル名一覧を返す
    return jsonify(files)


@app.route("/download")
def get_file():
    # GET パラメータ `id` の値を取得する
    id = request.args.get("id", "")

    # GET パラメータが指定されていなければ、400 Bad Request を返す
    if id == "":
        return "error", 400

    # ダウンロード要求があったファイルを読み出す
    filename = "/app/files/" + id
    content = ""

    # 61行目の処理でパスを指定して取得する必要があるので、
    # ホワイトリストにはパスまでの情報を入れる必要あり
    file_list = [
        "/app/files/sample0.txt",
        "/app/files/sample1.txt",
        "/app/files/sample2.txt",
        "/app/files/sample3.txt",
        "/app/files/sample4.txt",
        "/app/files/sample5.txt",
        "/app/files/sample6.txt",
        "/app/files/sample7.txt",
        "/app/files/sample8.txt",
        "/app/files/sample9.txt",
        "/app/files/sample10.txt",
        "/app/files/sub/a.txt",
        "/app/files/sub/a.txt",
    ]

    try:
        if filename in file_list:
            with open(filename, "r") as f:
                content = f.read()
        else:
            return "directory_traversalしないで", 405
    except FileNotFoundError:
        # 指定されたファイルが存在しなかった場合、404 Not Found を返す
        return "", 404

    # Content-Disposition: attachment ヘッダとともにファイルを返す
    resp = make_response(content)
    resp.headers["Content-Disposition"] = "attachment; filename=" + id
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
