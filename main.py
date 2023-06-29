from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.input_file import InputFile
import requests
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')
UNSPLASH_URL = f'https://api.unsplash.com'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f'Hi, {message.from_user.first_name}! 💕 \nWhat photo do you want? ')


async def get_photo(query):
    url = f'{UNSPLASH_URL}/photos/random'
    params = {
        'query': query
    }
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_API_KEY}"
    }
    r = httpx.get(url=url, params=params, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return InputFile.from_url(data['urls']['small'])


@dp.message_handler()
async def send_answer(message: types.Message):
    photo = await get_photo(message.text)
    await bot.send_photo(message.chat.id, photo)


if __name__ == '__main__':
    executor.start_polling(dp)
