import asyncio

from scheduler import run_scheduler, PRICES, PRICE_LISTS


async def handle_connection(reader, writer):
    addr = writer.get_extra_info('peername')
    company = ''
    path_list = []
    print('Connected by', addr)

    # Receive
    try:
        data = await reader.read(1024)
        # url is like 127.0.0.1:2000/company/command
        path = data.decode().split(" ")[1][1:]
        path_list = path.split('/')
        print(f'Request for {path_list[0]}')
    except ConnectionError:
        print(f'Client suddenly closed while receiving from {addr}')

    # Make response
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    if path_list[1] == 'price':
        data = f'{PRICES[path_list[0]]}'
    elif path_list[1] == 'price_list':
        data = f'{PRICE_LISTS[path_list[0]].close.tolist()}'
    else:
        data = f'Unknown path'
    query = header.encode('utf-8') + data.encode('utf-8')

    # Send
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
    print('Start scheduler...')
    await run_scheduler()
    print('Start server...')
    async with server:
        await server.serve_forever()

HOST, PORT = '127.0.0.1', 2000

if __name__ == "__main__":
    try:
        asyncio.run(main(HOST, PORT))
    except KeyboardInterrupt:
        print('\nServer has been stopped!')
