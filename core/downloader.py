import yt_dlp
import os

def download_song(url, download_folder):
    """
    Downloads a YouTube video or playlist to the given folder.
    Returns list of downloaded MP3 filenames.
    """
    os.makedirs(download_folder, exist_ok=True)

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
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if 'entries' in info:  # playlist
                for entry in info['entries']:
                    if entry is None:
                        continue
                    title = entry.get('title')
                    if title:
                        downloaded_files.append(f"{title}.mp3")
            else:  # single video
                title = info.get('title')
                if title:
                    downloaded_files.append(f"{title}.mp3")

    except Exception as e:
        print(f"Download failed for URL: {url}")
        print(e)

    # Verify files exist
    downloaded_files = [f for f in downloaded_files if os.path.isfile(os.path.join(download_folder, f))]

    return downloaded_files
