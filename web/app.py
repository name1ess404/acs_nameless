import sys
import os

# Make the parent directory of 'web/' visible to Python
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
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
    # Use 0.0.0.0 so Render can reach your app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
