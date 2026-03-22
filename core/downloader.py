import yt_dlp
import os
import shutil

# ------------------- CONFIG -------------------
DOWNLOAD_DIR = os.path.join("web", "static", "downloads")
TEMP_DIR = os.path.join("web", ".temp_processing")  # Hidden temp folder

# Create hidden temp folder
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Force Deno runtime for yt-dlp
os.environ["YT_DLP_JS_RUNTIME"] = "deno"

# ------------------- DOWNLOAD FUNCTION -------------------
def download_song(url):
    opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True,
        'outtmpl': os.path.join(TEMP_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    downloaded_files = []

    try:
        # Check if it's a playlist
        with yt_dlp.YoutubeDL({'extract_flat': True, 'quiet': True, 'no_warnings': True}) as ydl_flat:
            info = ydl_flat.extract_info(url, download=False)
            is_playlist = 'entries' in info

        urls_to_download = []
        if is_playlist:
            entries = [e for e in info['entries'] if e is not None]
            urls_to_download = [e['url'] if 'url' in e else e['webpage_url'] for e in entries]
        else:
            urls_to_download = [url]

        for song_url in urls_to_download:
            with yt_dlp.YoutubeDL(opts) as ydl_song:
                ydl_song.download([song_url])

            # Move mp3 to DOWNLOAD_DIR
            for file in os.listdir(TEMP_DIR):
                if file.endswith(".mp3"):
                    dest_path = os.path.join(DOWNLOAD_DIR, file)
                    shutil.move(os.path.join(TEMP_DIR, file), dest_path)
                    downloaded_files.append(file)

            # Clean up leftover files
            for leftover in os.listdir(TEMP_DIR):
                os.remove(os.path.join(TEMP_DIR, leftover))

    except Exception as e:
        print("Download failed:", e)

    # Return the list of downloaded files
    return downloaded_files


# ------------------- TEST -------------------
if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    files = download_song(url)
    print("Downloaded files:", files)
