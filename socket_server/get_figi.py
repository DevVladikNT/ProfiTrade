from pandas import DataFrame
from tinkoff.invest import Client, InstrumentStatus, SharesResponse, InstrumentIdType
from tinkoff.invest.services import InstrumentsService, MarketDataService

import pandas as pd

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)

# TICKER = "QIWI"
with open('../../ProfiTrade_tools/tinkoff_token.txt') as file:
    TOKEN = file.read()


def run():
    with Client(TOKEN) as cl:
        instruments: InstrumentsService = cl.instruments
        market_data: MarketDataService = cl.market_data

        # r = instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id="BBG004S683W7")
        # print(r)

        l = []
        # shares - акции
        # bonds - облигации
        # etfs - фонды
        # currencies - валюты
        # futures - фьючерсы
        for method in ['shares', 'bonds', 'etfs']:  # , 'currencies', 'futures']:
            for item in getattr(instruments, method)().instruments:
                l.append({
                    'ticker': item.ticker,
                    'figi': item.figi,
                    'type': method,
                    'name': item.name,
                })

        df = DataFrame(l)
        # df.to_json()

        # df = df[df['ticker'] == TICKER]
        # if df.empty:
        #     print(f"Нет тикера {TICKER}")
        #     return
        #
        # # print(df.iloc[0])
        # print(df['figi'].iloc[0])

        # print(df)
        df.to_csv('figi_list.csv')


if __name__ == '__main__':
    run()
