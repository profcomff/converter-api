from urllib.request import Request

import aiohttp
from fastapi import FastAPI, HTTPException
from httpx import Response
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from file_converter.routes.file import router as converter_router
from ..settings import Settings
from fastapi.staticfiles import StaticFiles

settings = Settings()
app = FastAPI()

app.include_router(converter_router, prefix='', tags=['Converter'])
app.mount('/static', StaticFiles(directory='static'), 'static')


class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method == 'POST':
            if 'content-length' not in request.headers:
                return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
            content_length = int(request.headers['content-length'])
            if content_length > self.max_upload_size:
                return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        return await call_next(request)


app.add_middleware(LimitUploadSize, max_upload_size=settings.MAX_SIZE)


@app.exception_handler(aiohttp.client_exceptions.ClientConnectorError)
async def not_found_error(request: Request, exc: aiohttp.client_exceptions.ClientConnectorError):
    raise HTTPException(
            500,
            f"request failed:  {exc} "
        )
