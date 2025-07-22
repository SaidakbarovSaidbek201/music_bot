from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS_URL

channels_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📢 1-kanalga obuna bo'lish", url=CHANNELS_URL[0])],
])