from fastapi import FastAPI
from file_converter.routes.file import router as converter_router
from ..settings import Settings
from fastapi.staticfiles import StaticFiles

settings = Settings()
app = FastAPI()

app.include_router(converter_router, prefix='', tags=['Converter'])
app.mount('/static', StaticFiles(directory='static'), 'static')
