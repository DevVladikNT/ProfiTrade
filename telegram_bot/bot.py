from aiogram import Bot, Dispatcher

from config import Config

import asyncio


bot = Bot(token=Config.token)
dp = Dispatcher()


async def main():
    from handlers import dp
    try:
        print('Bot is working...')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        print('Bot has been stopped!')
