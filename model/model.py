import json
import numpy as np
import pandas as pd
import pickle

from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()
model = None


@app.post("/predict")
async def predict(request: Request):
    body = await request.json()
    text = body['input']
    input_data = json.loads(text)

    window_size = 4
    alpha = 0.5

    df = pd.DataFrame(input_data)
    df.drop('volume', axis=1, inplace=True)
    df['open_MA'] = df['open'].rolling(window=window_size).mean()
    df['high_MA'] = df['high'].rolling(window=window_size).mean()
    df['low_MA'] = df['low'].rolling(window=window_size).mean()
    df['close_MA'] = df['close'].rolling(window=window_size).mean()
    df.fillna(value=0, inplace=True)
    df['open_EW'] = df['open'].ewm(alpha=alpha).mean()
    df['high_EW'] = df['high'].ewm(alpha=alpha).mean()
    df['low_EW'] = df['low'].ewm(alpha=alpha).mean()
    df['close_EW'] = df['close'].ewm(alpha=alpha).mean()

    data_stats = np.array([df.min(axis=1), (df.max(axis=1) - df.min(axis=1))])
    df = pd.DataFrame(
        (df.to_numpy() - data_stats[0].reshape(-1, 1)) /
        data_stats[1].reshape(-1, 1)
    )

    x_list = []
    for i in range(0, len(df) - window_size):
        input_data = df.iloc[i:(i + window_size)]
        x_list.append(input_data.to_numpy())  # .reshape(-1))
    x_list = np.array(x_list)

    # prediction looks like [[0.5]]
    prediction = model.predict(x_list[-1].reshape(-1, 4, 12), verbose=0)[0][0]
    sized = prediction * data_stats[1, -1] + data_stats[0, -1]
    response = int(sized * 100) / 100

    return {
        'response': response
    }


@app.on_event("startup")
async def startup():
    global model
    print('Loading model...')
    with open('model/model.pkl', 'rb') as file:
        model = pickle.load(file)
    print('Model loaded!')


HOST, PORT = '127.0.0.1', 3000


if __name__ == '__main__':
    try:
        uvicorn.run(app, host=HOST, port=PORT)
    except KeyboardInterrupt:
        print('\nModel has been stopped!')
