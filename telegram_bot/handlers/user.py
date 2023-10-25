from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Hello World!')


@router.message(Command('help'))
async def help_(message: Message):
    await message.answer('Some help')


@router.message(Command('get_id'))
async def get_id(message: Message):
    await message.answer(f'Your id is `{message.from_user.id}` (click to copy)',
                         parse_mode='markdown')

# цена = цена * 100, хз почему
# price = [LabeledPrice(label='Notebook', amount=100*100)]
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
