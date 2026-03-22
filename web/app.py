import sys
import os
import shutil
import traceback
import zipfile
from flask import Flask, render_template, request, send_from_directory
from core.downloader import download_song  # Make sure core/downloader.py exists
from tempfile import mkdtemp

# -----------------------
# Add parent directory so Python can see 'core'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
# -----------------------

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                # -----------------------
                # Use Render-safe temp folder
                downloads_dir = os.path.join(BASE_DIR, "downloads")
                os.makedirs(downloads_dir, exist_ok=True)

                temp_folder = mkdtemp(dir=downloads_dir)
                # -----------------------

                # Download the song(s) into temp_folder
                downloaded_files = download_song(url, temp_folder)

                if not downloaded_files:
                    return "Download failed. Check URL.", 400

                # -----------------------
                # If only one file, send it directly
                if len(downloaded_files) == 1:
                    return send_from_directory(
                        directory=temp_folder,
                        path=downloaded_files[0],
                        as_attachment=True
                    )

                # If multiple files, zip them
                zip_name = "playlist.zip"
                zip_path = os.path.join(downloads_dir, zip_name)
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for file in downloaded_files:
                        zipf.write(os.path.join(temp_folder, file), arcname=file)

                # Cleanup temp folder
                shutil.rmtree(temp_folder)

                # Send zip to user
                return send_from_directory(
                    directory=downloads_dir,
                    path=zip_name,
                    as_attachment=True
                )

            except Exception as e:
                # Print full error to logs
                traceback.print_exc()
                return f"Internal server error: {e}", 500

    # GET request → render form
    return render_template("index.html")


if __name__ == "__main__":
    # Use 0.0.0.0 so Render can reach the app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
