import re
import asyncio
import pandas as pd
from urllib.parse import unquote  # Декодировать крокозябры %D1%D2 обратно на русский

from scheduler import run_scheduler, PRICES, PRICE_LISTS


async def handle_connection(reader, writer):
    addr = writer.get_extra_info('peername')
    path_list = []
    print('Connected by', addr)

    # Receive data
    try:
        data = await reader.read(1024)
        # url is like 127.0.0.1:2000/command/param
        # path is like /command/param
        path = data.decode().split(" ")[1][1:]
        path_list = path.split('/')
        print(f'Request {path_list[0]} for {unquote(path_list[1])}')
    except ConnectionError:
        print(f'Client suddenly closed while receiving from {addr}')

    # Make response
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    #
    if path_list[0] == 'price':
        data = f'{PRICES[path_list[1]]}'
    elif path_list[0] == 'price_list':
        data = f'{PRICE_LISTS[path_list[1]].close.tolist()}'
    # localhost:port/search/company will use "company" as ticker
    # if "company" is not ticker, it'll search "company" in name
    # returns relevant figi
    elif path_list[0] == 'search':
        figi_df = pd.read_csv('figi_list.csv', index_col=0)
        figi_list = figi_df[figi_df['ticker'] == path_list[1].upper()]
        if len(figi_list) == 0:
            index_list = []
            for name in figi_df['name']:
                index_list.append(True if re.search(unquote(path_list[1]), name, flags=re.IGNORECASE) else False)
            figi_list = figi_df[index_list]
        if len(figi_list) == 0:
            data = 'Company not found'
        else:
            data = f'{figi_list["figi"].tolist()}'
    else:
        data = 'Unknown path'
    query = header.encode('utf-8') + data.encode('utf-8')

    # Send data
    # print(f'Send: "{data}" to: {addr}')
    try:
        writer.write(query)
        await writer.drain()
    except ConnectionError:
        print(f'Client suddenly closed, cannot send')

    writer.close()
    await writer.wait_closed()
    print('Disconnected by', addr)


async def main(host, port):
    server = await asyncio.start_server(handle_connection, host, port)
    # print('Start scheduler...')
    # await run_scheduler()
    print('Start server...')
    async with server:
        await server.serve_forever()

HOST, PORT = '127.0.0.1', 2000

if __name__ == "__main__":
    try:
        asyncio.run(main(HOST, PORT))
    except KeyboardInterrupt:
        print('\nServer has been stopped!')
