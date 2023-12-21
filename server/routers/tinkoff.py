import re

import pandas as pd
from fastapi import APIRouter, HTTPException

from scheduler import run_scheduler, CLOSE_PRICE, PRICES

router = APIRouter()


@router.get('/close_price/{figi}',
            tags=['tinkoff'],
            summary='Last close price')
async def price(figi: str):
    """
    Returns last updated close price for company.

    - **param figi**: Company's id.
    """
    response = CLOSE_PRICE.get(figi, 'None')

    return {
        'response': response
    }


@router.get('/close_prices/{figi}',
            tags=['tinkoff'],
            summary='List of close prices')
async def price_list(figi: str):
    """
    Returns list of last close prices for company.

    - **param figi**: Company's id.
    """
    if figi in PRICES.keys():
        response = PRICES.get(figi)["close"].tolist()
    else:
        raise HTTPException(status_code=404)

    return {
        'response': response
    }


@router.get('/prices/{figi}',
            tags=['tinkoff'],
            summary='All info about company')
async def data(figi: str):
    """
    Returns list of dicts with {open, high, low, close, volume} values for company.

    - **param figi**: Company's id.
    """
    if figi in PRICES.keys():
        response = PRICES.get(figi).to_dict("records")
    else:
        raise HTTPException(status_code=404)

    return {
        'response': response
    }


@router.get('/search/{string}',
            tags=['tinkoff'],
            summary='Search company')
async def search(string: str):
    """
    Returns list of companies which match input string with their figi/ticker/name.

    - **param string**: Figi, ticker or name of company.
    """

    # Search by figi
    figi_df = pd.read_csv('server/figi_list.csv', index_col=0)
    figi_list = figi_df[figi_df['figi'] == string]

    # Search by ticker
    if len(figi_list) == 0:
        figi_list = figi_df[figi_df['ticker'] == string.upper()]

    # Search by name
    if len(string) > 0 and len(figi_list) == 0:
        index_mask = []
        for name in figi_df['name']:
            index_mask.append(
                True if re.search(string, name, flags=re.IGNORECASE)
                else False
            )
        figi_list = figi_df[index_mask]

    # If haven't been found
    if len(figi_list) == 0:
        raise HTTPException(status_code=404)
    else:
        response = figi_list.to_dict("records")

    return {
        'response': response
    }


@router.on_event("startup")
async def startup():
    print('Start scheduler...')
    await run_scheduler()
    print('Scheduler started!')
