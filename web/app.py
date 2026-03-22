import sys
import os
import shutil
import zipfile
import traceback

from flask import Flask, render_template, request, send_from_directory
from tempfile import mkdtemp


# ---------- FIX IMPORT ----------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.downloader import download_song

# ---------- FLASK ----------

app = Flask(__name__, template_folder="templates")


DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        url = request.form.get("url")

        if url:

            try:

                temp_folder = mkdtemp(dir=DOWNLOADS_DIR)

                files = download_song(url, temp_folder)

                if not files:
                    return "Download failed. Check URL.", 400

                # single file

                if len(files) == 1:

                    return send_from_directory(
                        directory=temp_folder,
                        path=files[0],
                        as_attachment=True
                    )

                # multiple → zip

                zip_name = "playlist.zip"

                zip_path = os.path.join(DOWNLOADS_DIR, zip_name)

                with zipfile.ZipFile(zip_path, "w") as z:

                    for f in files:

                        z.write(
                            os.path.join(temp_folder, f),
                            arcname=f
                        )

                shutil.rmtree(temp_folder)

                return send_from_directory(
                    directory=DOWNLOADS_DIR,
                    path=zip_name,
                    as_attachment=True
                )

            except Exception as e:

                traceback.print_exc()

                return str(e), 500

    return render_template("index.html")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
