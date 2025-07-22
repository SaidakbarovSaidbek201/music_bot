import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from media_downloader import download_audio_from_video, download_video, check_all_channel_subscription
from yt_dlp import YoutubeDL
from config import BOT_TOKEN
from keyboard import channels_keyboard
import asyncio 
from youtubeapi import search_youtube_videos


TOKEN = BOT_TOKEN
bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(F.text == "/start")
async def start(message: Message):
    is_subscribed = await check_all_channel_subscription(bot, message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "Assalomu alaykum! Siz kanalga obuna bo'lishingiz kerak. "
            "Iltimos, quyidagi kanallarga obuna bo'ling va keyin qaytadan yozing.",
            reply_markup=channels_keyboard
        )
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text="🔍 Nomi bo‘yicha qidirish", callback_data="search_by_name")
        builder.button(text="🔗 YouTube URL yuborish", callback_data="send_url")
        builder.adjust(1)
        await message.answer("👋 Salom! Qanday yo‘l bilan yuklab olmoqchisiz?", reply_markup=builder.as_markup())


@dp.callback_query(F.data == "search_by_name")
async def prompt_for_search(call: CallbackQuery):
    await call.message.answer("🔍 Qaysi video yoki musiqani qidiryapsiz? Nomi yozing.")


@dp.message(F.text)
async def search_handler(message: Message, state: FSMContext):
    query = message.text.strip()
    if query.startswith("http"):
        return

    await message.answer(f"🔎 Qidirilmoqda: {query}")
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestaudio/best",
    }

    results = []
    try:
        with YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch10:{query}", download=False)["entries"]
            for video in search_results:
                results.append((video["title"], video["webpage_url"]))
    except Exception as e:
        return await message.answer(f"⚠️ Qidirishda xatolik: {e}")

    if not results:
        return await message.answer("❌ Hech qanday natija topilmadi.")

    builder = InlineKeyboardBuilder()
    for i, (title, url) in enumerate(results, 1):
        builder.button(text=f"{i}. {title[:50]}...", callback_data=f"choose_{url}")
    builder.adjust(1)

    await message.answer("🔽 Topilgan videolar:", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("choose_"))
async def choose_from_search(call: CallbackQuery, state: FSMContext):
    url = call.data.replace("choose_", "")
    await state.update_data(url=url)

    builder = InlineKeyboardBuilder()
    builder.button(text="🎵 Musiqa", callback_data="get_music")
    builder.button(text="🎬 Video", callback_data="get_video")
    builder.adjust(2)

    await call.message.answer("✅ Video topildi! Qanday formatda yuklab olasiz?", reply_markup=builder.as_markup())





@dp.callback_query(F.data == "send_url")
async def prompt_for_url(call: CallbackQuery):
    await call.message.answer("📎 YouTube manzilini yuboring (https://...) va men uni yuklab beraman.")

@dp.message(F.text)
async def search_handler(message: Message, state: FSMContext):
    query = message.text.strip()
    if query.startswith("http"):
        return

    await message.answer(f"🔎 Qidirilmoqda: {query}")

    try:
        results = search_youtube_videos(query)
    except Exception as e:
        return await message.answer(f"⚠️ Qidirishda xatolik: {e}")

    if not results:
        return await message.answer("❌ Hech qanday natija topilmadi.")

    builder = InlineKeyboardBuilder()
    for i, (title, url) in enumerate(results, 1):
        builder.button(text=f"{i}. {title[:50]}...", callback_data=f"choose_{url}")
    builder.adjust(1)

    await message.answer("🔽 Topilgan videolar:", reply_markup=builder.as_markup())







if __name__ == "__main__":
    import asyncio
    os.makedirs("downloads", exist_ok=True)
    asyncio.run(dp.start_polling(bot))
