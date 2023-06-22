from aiogram.types import LabeledPrice, Message, PreCheckoutQuery, ContentType
from aiogram.dispatcher.filters import Command

from src.bot import bot, dp


@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(message.chat.id, 'Hello World!')


@dp.message_handler(Command('help'))
async def start(message: Message):
    await bot.send_message(message.chat.id, 'Some help')


@dp.message_handler(Command('get_id'))
async def start(message: Message):
    await bot.send_message(message.chat.id, f'Your id is: {message.from_user.id}')

# price = [LabeledPrice(label='Notebook', amount=100*100)]  # цена = цена * 100, хз почему
#
#
# @dp.message_handler(Command('buy'))
# async def buy_process(message: Message):
#     await bot.send_invoice(message.chat.id,
#                            title='Laptop',
#                            description='whatever',
#                            provider_token=Config.pay_token,
#                            currency='rub',
#                            need_email=True,
#                            prices=price,
#                            start_parameter='example',
#                            payload='some_invoice')
#
#
# @dp.pre_checkout_query_handler(lambda query: True)
# async def pre_checkout_process(pre_checkout: PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)
#
#
# @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
# async def successful_payment(message: Message):
#     await bot.send_message(message.chat.id, 'Payment has been done!')
