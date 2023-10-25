import asyncio

from aiogram import Bot, Dispatcher

from config import Config
from handlers.user import router as router1
from handlers.analytics import router as router2


bot = Bot(token=Config.token)
dp = Dispatcher()


async def main():
    try:
        dp.include_router(router1)
        dp.include_router(router2)
        print('Bot is working...')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        print('Bot has been stopped!')
