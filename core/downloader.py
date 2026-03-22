import yt_dlp
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COOKIES_FILE = os.path.join(BASE_DIR, "cookies.txt")


def download_song(url, download_folder):

    os.makedirs(download_folder, exist_ok=True)

    opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),

        'cookiefile': COOKIES_FILE,   # ✅ THIS FIXES BOT ERROR

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],

        'quiet': False,
        'ignoreerrors': False,
    }

    downloaded_files = []

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:

            info = ydl.extract_info(url, download=True)

            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        title = entry.get("title")
                        if title:
                            downloaded_files.append(title + ".mp3")

            else:
                title = info.get("title")
                if title:
                    downloaded_files.append(title + ".mp3")

    except Exception as e:
        print("DOWNLOAD ERROR:", e)

    downloaded_files = [
        f for f in downloaded_files
        if os.path.isfile(os.path.join(download_folder, f))
    ]

    print("FILES:", downloaded_files)

    return downloaded_files
