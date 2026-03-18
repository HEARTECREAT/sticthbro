import asyncio
import logging
import os
from aiohttp import web
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Ключи берем из настроек
API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настройка Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Бот и Диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# --- МИНИ-САЙТ ДЛЯ RENDER (ЧТОБЫ ОН НЕ ВЫРУБАЛ БОТА) ---
async def handle(request):
    return web.Response(text="Stitch is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render дает порт в переменной окружения PORT
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Веб-сервер запущен на порту {port}")

# --- ЛОГИКА БОТА ---
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Стич на связи! Охана в деле. Теперь я не засну! 👽🚀")

@dp.message()
async def handle_message(message: types.Message):
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Бля, бро, чет связь с космосом прервалась. Попробуй еще раз!")

async def main():
    # Запускаем сайт и бота одновременно
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
