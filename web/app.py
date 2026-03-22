import sys
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import threading
from core.downloader import download_song

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

app = Flask(__name__, template_folder="templates")
DOWNLOAD_DIR = os.path.join("static", "downloads")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            # Run download in a thread
            def thread_target():
                files = download_song(url)
                if files:
                    print("Downloaded:", files)

            threading.Thread(target=thread_target).start()

            # Show a simple "Downloading..." page or redirect to homepage
            return render_template("index.html", message="Downloading your song(s)... Check back in a few seconds!")

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
