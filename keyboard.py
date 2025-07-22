from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
import os

CHANNELS_URL = os.getenv("CHANNELS_URL")

channels_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📢 1-kanalga obuna bo'lish", url=CHANNELS_URL[0])],
])