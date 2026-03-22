import yt_dlp
import os
import shutil

# ------------------- CONFIG -------------------
DOWNLOAD_DIR = "downloads"
TEMP_DIR = ".temp_processing"  # Hidden temp folder

# Create hidden temp folder
if os.name == 'nt':
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.system(f'attrib +h {TEMP_DIR}')
else:
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
    
    try:
        with yt_dlp.YoutubeDL({'extract_flat': True, 'quiet': True, 'no_warnings': True}) as ydl_flat:
            info = ydl_flat.extract_info(url, download=False)
            is_playlist = 'entries' in info

        urls_to_download = []
        if is_playlist:
            # Use the real webpage_url for each video
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
                    shutil.move(os.path.join(TEMP_DIR, file), os.path.join(DOWNLOAD_DIR, file))

            # Clean up leftover files
            for leftover in os.listdir(TEMP_DIR):
                os.remove(os.path.join(TEMP_DIR, leftover))

    except:
        pass  # Silent fail, no output

# ------------------- MAIN -------------------
if __name__ == "__main__":
    url = input().strip()
    download_song(url)
