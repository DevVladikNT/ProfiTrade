from dataclasses import dataclass


@dataclass
class Config:
    pay_token: str = ''

    with open('../../ProfiTrade_tools/token.txt') as file:
        token = file.read()

    with open('../../ProfiTrade_tools/admin_id.txt') as file:
        admin_id = int(file.read())
