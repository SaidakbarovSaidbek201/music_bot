import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from media_downloader import download_audio_from_video, download_video

TOKEN = "7537990926:AAGIc6kza09IKgrMW1jBqmvB5FVCMYdYoDc"
bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text.startswith("http"))
async def handle_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text.strip())
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎵 Music", callback_data="get_music"),
            InlineKeyboardButton(text="🎬 Video", callback_data="get_video")
        ]
    ])
    await message.answer("Nimani skachat qilmoqchisiz?", reply_markup=kb)

@dp.callback_query(F.data == "get_music")
async def handle_music(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    await call.message.answer("🎧 Audio yuklab olinmoqda...")
    try:
        audio_file = download_audio_from_video(url)
        await call.message.answer_audio(audio=types.FSInputFile(audio_file))
        os.remove(audio_file)
    except Exception as e:
        await call.message.answer(f"⚠️ Xatolik: {e}")

@dp.callback_query(F.data == "get_video")
async def handle_video(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    await call.message.answer("📥 Video yuklab olinmoqda...")
    try:
        video_file = download_video(url)
        await call.message.answer_video(video=types.FSInputFile(video_file))
        os.remove(video_file)
    except Exception as e:
        await call.message.answer(f"⚠️ Xatolik: {e}")

if __name__ == "__main__":
    import asyncio
    os.makedirs("downloads", exist_ok=True)
    asyncio.run(dp.start_polling(bot))
