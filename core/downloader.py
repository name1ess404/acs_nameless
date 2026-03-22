import yt_dlp
import os
import shutil

# ------------------- Folders -------------------
DOWNLOAD_DIR = "downloads"
TEMP_DIR = ".temp_processing"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Force Deno runtime for yt-dlp
os.environ["YT_DLP_JS_RUNTIME"] = "deno"

def download_song(url, download_folder=None):
    """
    Downloads a YouTube video or playlist to the given folder.
    Returns list of downloaded MP3 filenames.
    """
    if download_folder is None:
        download_folder = DOWNLOAD_DIR

    opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True,
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    downloaded_files = []

    try:
        # Detect playlist or single video
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

            # Collect mp3 files
            for file in os.listdir(download_folder):
                if file.endswith(".mp3") and file not in downloaded_files:
                    downloaded_files.append(file)

    except Exception as e:
        print(f"Download failed: {e}")

    return downloaded_files
