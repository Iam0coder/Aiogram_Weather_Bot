import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, WEATHER_API_KEY

# Асинхронно создаем экземпляры бота и диспетчера
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    @dp.message(CommandStart())
    async def start_handler(message: Message):
        await message.answer("Привет! Я бот. Я могу предоставить тебе прогноз погоды. Используй команду /weather, чтобы узнать погоду.")

    @dp.message(Command("help"))
    async def help_handler(message: Message):
        await message.answer("Я могу помочь тебе узнать погоду. Используй команду /weather, чтобы получить прогноз погоды.")

    @dp.message(Command("weather"))
    async def weather_handler(message: Message):
        city = "Москва"  # Можете заменить на любой другой город
        weather_data = get_weather(city)
        await message.answer(weather_data)

    def get_weather(city: str) -> str:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return "Не удалось получить данные о погоде."

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"Погода в {city}: {temp}°C, {description}."

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
