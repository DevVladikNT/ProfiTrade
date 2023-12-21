import pandas as pd
from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tinkoff.invest import CandleInterval
from tinkoff.invest.retrying.aio.client import AsyncRetryingClient
from tinkoff.invest.retrying.settings import RetryClientSettings
from tinkoff.invest.utils import now

retry_settings = RetryClientSettings(use_retry=True, max_retry_attempt=2)
with open('../ProfiTrade_tools/tinkoff_token.txt') as file:
    TOKEN = file.read()

CLOSE_PRICE = {}
PRICES = {}
FIGI = {
    'yandex': 'BBG006L8G4H1',
    'sber': 'BBG004730N88',
}


# Use this to transform object-type price to float value
def obj_to_float(obj):
    return obj.units + float(obj.nano) / 10**9


async def get_price(figi):
    global CLOSE_PRICE, PRICES
    candle_list = []
    async with AsyncRetryingClient(TOKEN, settings=retry_settings) as client:
        async for candle in client.get_all_candles(
            figi=figi,
            from_=now() - timedelta(hours=48),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            row = {
                'time': candle.time,
                'open': obj_to_float(candle.open),
                'high': obj_to_float(candle.high),
                'low': obj_to_float(candle.low),
                'close': obj_to_float(candle.close),
                'volume': candle.volume,
            }
            candle_list.append(row)
    CLOSE_PRICE[figi] = candle_list[-1]['close']
    PRICES[figi] = pd.DataFrame(candle_list)
    print(f'Price for {figi} is {CLOSE_PRICE[figi]}')


async def job_creator():
    for figi in FIGI.values():
        await get_price(figi)


async def run_scheduler():
    await job_creator()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(job_creator, 'interval', seconds=30)
    # scheduler.add_job(main, 'cron', hour=12, minute=0, second=0)
    scheduler.start()




