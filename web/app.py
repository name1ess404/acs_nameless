import sys
import os
import shutil
from flask import Flask, render_template, request, send_from_directory
from core.downloader import download_song
from tempfile import mkdtemp
import zipfile

# Make parent directory visible to Python
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            # Create a temporary folder for this download session
            temp_folder = mkdtemp(dir=os.path.join(BASE_DIR, "downloads"))

            # Download songs into temp folder
            downloaded_files = download_song(url, temp_folder)

            if not downloaded_files:
                return "Download failed. Check URL.", 400

            # If one file, send it directly
            if len(downloaded_files) == 1:
                return send_from_directory(
                    directory=temp_folder,
                    path=downloaded_files[0],
                    as_attachment=True
                )

            # If multiple files, zip them
            zip_path = os.path.join(BASE_DIR, "downloads", "playlist.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for file in downloaded_files:
                    zipf.write(os.path.join(temp_folder, file), arcname=file)

            # Clean up temp folder
            shutil.rmtree(temp_folder)

            # Send zip
            return send_from_directory(
                directory=os.path.join(BASE_DIR, "downloads"),
                path="playlist.zip",
                as_attachment=True
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
