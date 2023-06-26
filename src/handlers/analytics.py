import requests
import json
import ast
from io import BytesIO

from aiogram.types import Message
from aiogram.dispatcher.filters import Command

import numpy as np
import matplotlib.pyplot as plt
from magic_filter import F

from src.bot import bot, dp

COMPANIES = ['yandex', 'sber', 'vk', 'qiwi']


@dp.message_handler(Command('price'))
async def price(message: Message):
    for company in COMPANIES:
        response = requests.get(f'http://127.0.0.1:2000/price/{company}')
        current_price = float(response.text)
        response = requests.get(f'http://127.0.0.1:2000/price_list/{company}')
        price_list = json.loads(response.text)

        mean = np.mean(price_list)
        growth = (current_price - mean) / mean
        text = f'{company.title()}: *{current_price}* ({"+" if growth >= 0 else ""}{growth * 100:.2f}%)'
        await bot.send_message(message.chat.id, text, parse_mode='markdown')


@dp.message_handler(Command('price_plot'))
async def price_plot(message: Message):
    for company in COMPANIES:
        response = requests.get(f'http://127.0.0.1:2000/price_list/{company}')
        price_list = json.loads(response.text)

        fig, ax = plt.subplots(1, 1)
        plt.plot(np.arange(len(price_list)), price_list)
        ax.xaxis.set_visible(False)
        plt.title(company.title())

        # Send plot as image
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        await bot.send_photo(message.chat.id, img)


@dp.message_handler(F.text)
async def get_info(message: Message):
    response = requests.get(f'http://127.0.0.1:2000/search/{message.text}')
    if response.text == 'Company not found':
        await bot.send_message(message.chat.id, 'Company not found')
    else:
        figi_list = ast.literal_eval(response.text)
        for figi in figi_list:
            await bot.send_message(message.chat.id, figi)
            # todo
