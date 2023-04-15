FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV APP_NAME=file_converter
ENV APP_MODULE=${APP_NAME}.routes.base:app

COPY ./requirements.txt /app/
RUN pip install -U -r /app/requirements.txt

COPY ./static /app/static/
COPY ./logging_prod.conf /app/
COPY ./logging_test.conf /app/

COPY ./${APP_NAME} /app/${APP_NAME}

RUN apt-get update && \
	apt-get -y -q install \
		libreoffice \
