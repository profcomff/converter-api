FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV APP_NAME=file_converter
ENV APP_MODULE=${APP_NAME}.routes.base:app

COPY ./requirements.txt /app/
RUN pip install -U -r /app/requirements.txt
RUN sudo apt install tesseract-ocr
RUN sudo apt install libtesseract-dev

COPY ./static /app/static/
COPY ./migrations /migrations/

COPY ./${APP_NAME} /app/${APP_NAME}



