from fastapi import FastAPI
import uvicorn

from db.base import Base
from db.session import engine
from routers.tinkoff import router as tinkoff_router
from routers.users import router as users_router

tags_metadata = [
    {
        "name": "tinkoff",
        "description": "Operations with prices and companies' info. Information has been taken from Tinkoff API.",
        "externalDocs": {
            "description": "Tinkoff API",
            "url": "https://developer.tinkoff.ru/docs/api",
        },
    },
    {
        "name": "user",
        "description": "Operations with users.",
    },
]

Base.metadata.create_all(bind=engine)
app = FastAPI(openapi_tags=tags_metadata)

app.include_router(tinkoff_router)
app.include_router(users_router)

HOST, PORT = '127.0.0.1', 2000

if __name__ == '__main__':
    try:
        uvicorn.run(app, host=HOST, port=PORT)
    except KeyboardInterrupt:
        print('\nServer has been stopped!')
