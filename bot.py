import asyncio
import logging
import os
from aiohttp import web
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

async def handle(request):
    return web.Response(text="Stitch is alive! Ohana forever! 👽")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Мини-сайт запущен на порту {port}")

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Стич на связи! Охана в деле. Поставил старые добрые мозги, теперь точно полетим! 🚀👽")

@dp.message()
async def handle_message(message: types.Message):
    try:
        response = model.generate_content(message.text)
        if response and response.text:
            await message.answer(response.text)
        else:
            await message.answer("Бро, нейронка че-то застеснялась. Попробуй еще раз!")
    except Exception as e:
        logging.error(f"ОШИБКА: {e}")
        await message.answer(f"Бля, бро, чет опять связь барахлит. Ошибка: {str(e)[:50]}...")

async def main():
    await start_web_server()
    logging.info("Бот на gemini-pro стартовал...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
