import pickle

import numpy as np
import pandas as pd
from tensorflow import keras
from keras import layers


window_size = 4
alpha = 0.5

df = pd.read_csv('data_1hour.csv')
df.drop(['date', 'isoformat', 'volume'], axis=1, inplace=True)
df['open_MA'] = df['open'].rolling(window=window_size).mean()
df['high_MA'] = df['high'].rolling(window=window_size).mean()
df['low_MA'] = df['low'].rolling(window=window_size).mean()
df['close_MA'] = df['close'].rolling(window=window_size).mean()
df.fillna(value=0, inplace=True)
df['open_EW'] = df['open'].ewm(alpha=alpha).mean()
df['high_EW'] = df['high'].ewm(alpha=alpha).mean()
df['low_EW'] = df['low'].ewm(alpha=alpha).mean()
df['close_EW'] = df['close'].ewm(alpha=alpha).mean()
df = df.iloc[3:-1]
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)

data_stats = np.array([df.min(axis=1), (df.max(axis=1) - df.min(axis=1))])
df = pd.DataFrame(
    (df.to_numpy() - data_stats[0].reshape(-1, 1)) /
    data_stats[1].reshape(-1, 1)
)

x_list = []
y_list = []
for i in range(0, len(df) - window_size):
    input_data = df.iloc[i:(i + window_size)]
    output_data = df[3].iloc[i + window_size]  # 3 - close column
    x_list.append(input_data.to_numpy())  #.reshape(-1))
    y_list.append(output_data)
x_list = np.array(x_list)
y_list = np.array(y_list)

inputs = keras.Input(shape=(window_size, 12))
x = layers.LSTM(16)(inputs)
x = layers.Dense(8, activation='elu')(x)
x = layers.Dense(6, activation='elu')(x)
outputs = layers.Dense(1)(x)
model = keras.Model(inputs, outputs)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-3),
              loss=keras.losses.MeanAbsoluteError())
model.fit(x_list,
          y_list,
          epochs=100)

with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)
