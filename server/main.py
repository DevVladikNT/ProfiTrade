from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from db.base import Base
from db.session import engine
from routers.operations import router as operations_router
from routers.tinkoff import router as tinkoff_router
from routers.users import router as users_router

description = """
This is description
"""

tags_metadata = [
    {
        "name": "tinkoff",
        "description": "Operations with prices and companies' info."
                       "Information has been taken from Tinkoff API.",
        "externalDocs": {
            "description": "Tinkoff API",
            "url": "https://developer.tinkoff.ru/docs/api",
        },
    },
    {
        "name": "user",
        "description": "Operations with users.",
    },
    {
        "name": "operation",
        "description": "Financial operations.",
    },
]

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title='ProfiTrade',
    description=description,
    version='0.0.1',
    contact={
        'name': 'Vladislav',
        'url': 'https://github.com/DevVladikNT',
    },
    openapi_tags=tags_metadata
)

app.include_router(operations_router)
app.include_router(tinkoff_router)
app.include_router(users_router)

origins = [
    'http://localhost:5173',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

HOST, PORT = '127.0.0.1', 2000

if __name__ == '__main__':
    try:
        uvicorn.run(app, host=HOST, port=PORT)
    except KeyboardInterrupt:
        print('\nServer has been stopped!')
