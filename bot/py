import asyncio
import logging
import os
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Берем ключи из секретных настроек (Environments)
API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настройка Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Инициализация бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Логирование, чтобы видеть, если что-то пойдет не так
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Стич на связи! Охана в деле. О чем попиздим, бро? 👽🚀")

@dp.message()
async def handle_message(message: types.Message):
    try:
        # Отправляем текст пользователя в Gemini
        response = model.generate_content(message.text)
        # Отвечаем пользователю текстом от нейронки
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Бля, бро, чет связь с космосом прервалась. Попробуй еще раз!")

async def main():
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
