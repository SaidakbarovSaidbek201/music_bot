from yt_dlp import YoutubeDL
from pathlib import Path
import logging
from aiogram import Bot
from config import CHANNELS_ID

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


async def check_all_channel_subscription(bot: Bot, user_id: int):
    for channel in CHANNELS_ID:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'creator', 'administrator', "owner"]:
                return False
        except Exception as e:
            logging.error(f"Error checking subscription for {channel}: {e}")
            return False
    return True