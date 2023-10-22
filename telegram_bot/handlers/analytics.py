import re

import requests
import json
import ast
from io import BytesIO

from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram.filters import Command

import numpy as np
import matplotlib.pyplot as plt
from aiogram import F

from telegram_bot.bot import bot, dp

COMPANIES = ['yandex', 'sber', 'vk', 'qiwi']


@dp.message(Command('price'))
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


@dp.message(Command('price_plot'))
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


@dp.message(F.text)
async def get_info(message: Message):
    if message.text.startswith('/predict'):
        figi = re.sub('/predict', '', message.text)
        request = {
            'figi': figi,
            'text': figi
        }

        response = requests.post('http://127.0.0.1:2000/search', json=request)
        companies_info = response.json()['response']
        company = json.loads(companies_info)[0]
        response = requests.post('http://127.0.0.1:2000/price_list', json=request)
        price_list = response.json()['response']
        if not price_list:
            await bot.send_message(message.chat.id, 'This company is anavailable now')
            return

        # mean = np.mean(price_list[-4:])
        growth = (price_list[-1] - price_list[-2]) / price_list[-2]

        response = requests.post('http://127.0.0.1:2000/data', json={'figi': company['figi']})
        input_data = response.json()['response']
        response = requests.post('http://127.0.0.1:3000/predict', json={'input': input_data})
        predicted_price = response.json()['response']

        predicted_growth = (predicted_price - price_list[-1]) / price_list[-1]

        text = f'*{company["name"]}* \[`{company["ticker"]}`]\n\n' +\
               f'Current price: *{price_list[-1]}* ({"+" if growth >= 0 else ""}{growth * 100:.2f}%)\n' +\
               f'Prediction: *{predicted_price}* ({"+" if predicted_growth >= 0 else ""}{predicted_growth * 100:.2f}%)'

        # Make plot
        fig, ax = plt.subplots(1, 1)
        fig.set_figheight(5)
        fig.set_figwidth(15)
        plt.plot(np.arange(len(price_list)), price_list, label='Real')
        plt.plot(np.arange(len(price_list) - 1, len(price_list) + 1),
                 [price_list[-1], predicted_price],
                 label='Prediction')
        ax.xaxis.set_visible(False)
        plt.title(company['name'])
        plt.legend()
        fig.savefig(f'{message.chat.id}.png')
        img = FSInputFile(f'{message.chat.id}.png')
        await bot.send_message(message.chat.id, text, parse_mode='markdown')
        await bot.send_photo(message.chat.id, img)
    else:
        request = {
            'text': message.text
        }
        response = requests.post('http://127.0.0.1:2000/search', json=request)
        companies_info = response.json()['response']
        if companies_info == 'Company not found':
            await bot.send_message(message.chat.id, 'Company not found')
        else:
            companies = json.loads(companies_info)
            for item in companies:
                response = requests.post('http://127.0.0.1:2000/price', json={'figi': item['figi']})
                current_price = response.json()['response']
                text = f'*{item["name"]}* \[`{item["ticker"]}`]\n\n' +\
                       f'Current price: *{current_price}*\n' +\
                       f'/predict{item["figi"]} to work with it'
                await bot.send_message(message.chat.id, text, parse_mode='markdown')
