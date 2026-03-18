import asyncio
import logging
import os
from aiohttp import web
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Ключи берем из переменных окружения Render
API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настройка Gemini (исправлено название модели на полный путь)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Инициализация бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# --- МИНИ-СЕРВЕР ДЛЯ RENDER (ЧТОБЫ НЕ БЫЛО PORT TIMEOUT) ---
async def handle(request):
    return web.Response(text="Stitch is alive and kicking! 👽")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render сам назначит порт, если нет - берем 10000
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Мини-сайт запущен на порту {port}")

# --- ЛОГИКА ТЕЛЕГРАМ-БОТА ---
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Стич на связи! Охана в деле. Теперь я точно не засну! 👽🚀")

@dp.message()
async def handle_message(message: types.Message):
    try:
        # Генерируем ответ от нейронки
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Ошибка Gemini: {e}")
        await message.answer("Бля, бро, чет связь с космосом прервалась. Попробуй еще раз!")

async def main():
    # Запускаем и сервер для Render, и бота одновременно
    await start_web_server()
    print("Бот погнал в космос...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
