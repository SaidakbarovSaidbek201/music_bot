from yt_dlp import YoutubeDL
from pathlib import Path

def download_audio_from_video(url: str) -> str:
    output_path = "downloads/%(title)s.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'ffmpeg_location': r'C:\ffmpeg\bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")


def download_video(url: str) -> str:
    output_path = "downloads/%(title)s.%(ext)s"
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'ffmpeg_location': r'C:\ffmpeg\bin',
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename
