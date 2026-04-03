import yt_dlp
import os

def download_video(url: str, output_dir="videos"):
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'mp4/best',
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return file_path