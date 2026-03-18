import asyncio
import logging
import os
from aiohttp import web
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Ключи из настроек Render
API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настройка Gemini (используем универсальное имя модели)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Бот и Диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# --- МИНИ-САЙТ ДЛЯ RENDER (ЧТОБЫ ОН НЕ ВЫРУБАЛ БОТА) ---
async def handle(request):
    return web.Response(text="Stitch is alive and kicking! 👽")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Мини-сайт запущен на порту {port}")

# --- ЛОГИКА БОТА ---
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Стич на связи! Охана в деле. Теперь я не засну и готов базарить! 👽🚀")

@dp.message()
async def handle_message(message: types.Message):
    try:
        # Прямой запрос к нейронке
        response = model.generate_content(message.text)
        if response and response.text:
            await message.answer(response.text)
        else:
            await message.answer("Бро, нейронка задумалась и ничего не выдала. Попробуй еще раз!")
    except Exception as e:
        logging.error(f"ОШИБКА GEMINI: {e}")
        await message.answer(f"Бля, бро, чет связь с космосом прервалась. Ошибка: {str(e)[:50]}")

async def main():
    # Запускаем сайт и бота одновременно
    await start_web_server()
    logging.info("Бот погнал в космос...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
