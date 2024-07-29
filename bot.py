import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from config import TOKEN, WEATHER_API_KEY

# Определяем состояния для конечного автомата
class WeatherStates(StatesGroup):
    waiting_for_city = State()

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
    async def weather_handler(message: Message, state: FSMContext):
        await message.answer("Введите название города для получения прогноза погоды:")
        await state.set_state(WeatherStates.waiting_for_city)

    @dp.message(WeatherStates.waiting_for_city)
    async def city_received(message: Message, state: FSMContext):
        city = message.text
        weather_data = get_weather(city)
        await message.answer(weather_data)
        await state.clear()

    def get_weather(city: str) -> str:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] != 200:
                return "Не удалось получить данные о погоде."

            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"Погода в {city}: {temp}°C, {description}."
        except requests.exceptions.RequestException as e:
            return f"Ошибка при получении данных о погоде: {e}"

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
