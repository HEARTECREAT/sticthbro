import asyncio
import logging
import os
from aiohttp import web
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Ключи
API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настройка Gemini (упростили название модели)
genai.configure(api_key=API_KEY)
# Попробуем самое прямое название
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# --- ЗАГЛУШКА ДЛЯ RENDER ---
async def handle(request):
    return web.Response(text="Stitch is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# --- ЛОГИКА ---
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Стич на связи! Охана в деле. Базарим, бро! 👽")

@dp.message()
async def handle_message(message: types.Message):
    try:
        # Просим нейронку ответить
        response = model.generate_content(message.text)
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("Бро, нейронка почему-то промолчала...")
    except Exception as e:
        # Выводим РЕАЛЬНУЮ ошибку в логи Render
        logging.error(f"ПОЛНАЯ ОШИБКА: {e}")
        await message.answer(f"Бля, бро, чет связь с космосом прервалась. Ошибка: {str(e)[:50]}...")

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
