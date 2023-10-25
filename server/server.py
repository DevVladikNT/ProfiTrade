import re
import pandas as pd

from fastapi import FastAPI, Request
import uvicorn

from scheduler import run_scheduler, PRICES, PRICE_LISTS

app = FastAPI()


@app.post("/price")
async def price(request: Request):
    body = await request.json()

    response = PRICES.get(body['figi'], 'None')

    return {
        'response': response
    }


@app.post("/price_list")
async def price_list(request: Request):
    body = await request.json()

    if body['figi'] in PRICE_LISTS.keys():
        response = PRICE_LISTS.get(body['figi'])["close"].tolist()
    else:
        response = []

    return {
        'response': response
    }


@app.post("/data")
async def data(request: Request):
    body = await request.json()

    if body['figi'] in PRICE_LISTS.keys():
        response = PRICE_LISTS.get(body['figi']).to_json(orient="records")
    else:
        response = []

    return {
        'response': response
    }


@app.post("/search")
async def search(request: Request):
    body = await request.json()

    # Search by figi
    figi_df = pd.read_csv('server/figi_list.csv', index_col=0)
    figi_list = figi_df[figi_df['figi'] == body['text']]

    # Search by ticker
    if len(figi_list) == 0:
        figi_list = figi_df[figi_df['ticker'] == body['text'].upper()]

    # Search by name
    if len(body['text']) > 0 and len(figi_list) == 0:
        index_mask = []
        for name in figi_df['name']:
            index_mask.append(
                True if re.search(body['text'], name, flags=re.IGNORECASE)
                else False
            )
        figi_list = figi_df[index_mask]

    # If haven't been found
    if len(figi_list) == 0:
        response = 'Company not found'
    else:
        response = figi_list.to_json(orient="records")

    return {
        'response': response
    }


@app.on_event("startup")
async def startup():
    print('Start scheduler...')
    await run_scheduler()
    print('Scheduler started!')


HOST, PORT = '127.0.0.1', 2000


if __name__ == '__main__':
    try:
        uvicorn.run(app, host=HOST, port=PORT)
    except KeyboardInterrupt:
        print('\nServer has been stopped!')
