import uvicorn

from file_converter.routes.base import app


if __name__ == '__main__':
    uvicorn.run(app)
