import random
import pandas as pd
from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tinkoff.invest import CandleInterval
from tinkoff.invest.retrying.aio.client import AsyncRetryingClient
from tinkoff.invest.retrying.settings import RetryClientSettings
from tinkoff.invest.utils import now

retry_settings = RetryClientSettings(use_retry=True, max_retry_attempt=2)
with open('../../ProfiTrade_tools/tinkoff_token.txt') as file:
    TOKEN = file.read()

PRICES = {
    'yandex': 0,
    'sber': 0,
    'vk': 0,
    'qiwi': 0,
}
PRICE_LISTS = {
    'yandex': None,
    'sber': None,
    'vk': None,
    'qiwi': None,
}
FIGI = {
    'yandex': 'BBG006L8G4H1',
    'sber': 'BBG004730N88',
    'vk': 'BBG00178PGX3',
    'qiwi': 'BBG005D1WCQ1',
}


# Use this to transform object-type price to float value
def obj_to_float(obj):
    return obj.units + float(obj.nano) / 10**9


async def get_price(company):
    global PRICES, PRICE_LISTS
    candle_list = []
    async with AsyncRetryingClient(TOKEN, settings=retry_settings) as client:
        async for candle in client.get_all_candles(
            figi=FIGI[company],
            from_=now() - timedelta(minutes=60),
            interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        ):
            row = {
                'open': obj_to_float(candle.open),
                'high': obj_to_float(candle.high),
                'low': obj_to_float(candle.low),
                'close': obj_to_float(candle.close),
                'volume': candle.volume,
            }
            candle_list.append(row)
    PRICES[company] = candle_list[-1]['close']
    PRICE_LISTS[company] = pd.DataFrame(candle_list)
    print(f'Price for {company} is {PRICES[company]}')


async def job_creator():
    for company in FIGI.keys():
        await get_price(company)


async def run_scheduler():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(job_creator, 'interval', seconds=60)
    # scheduler.add_job(main, 'cron', hour=12, minute=0, second=0)
    scheduler.start()




