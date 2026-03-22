import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from flask import Flask, render_template, request, redirect
from core.downloader import download_song
import threading


app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        url = request.form.get("url")

        if url:
            threading.Thread(
                target=download_song,
                args=(url,)
            ).start()

            return redirect("/")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
