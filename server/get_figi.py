import pandas as pd
from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService


# TICKER = "QIWI"
with open('../../ProfiTrade_tools/tinkoff_token.txt') as file:
    TOKEN = file.read()


def run():
    with Client(TOKEN) as cl:
        instruments: InstrumentsService = cl.instruments

        list_ = []
        # shares - акции
        # bonds - облигации
        # etfs - фонды
        # currencies - валюты
        # futures - фьючерсы
        for method in ['shares']:  # , 'bonds', 'etfs']:  # , 'currencies', 'futures']:
            for item in getattr(instruments, method)().instruments:
                list_.append({
                    'ticker': item.ticker,
                    'figi': item.figi,
                    'type': method,
                    'name': item.name,
                })

        df = pd.DataFrame(list_)
        df.to_csv('figi_list.csv')


if __name__ == '__main__':
    run()
