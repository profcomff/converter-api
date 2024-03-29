FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
ENV APP_NAME=file_converter
ENV APP_MODULE=${APP_NAME}.routes.base:app

COPY ./requirements.txt /app/
COPY ./logging_prod.conf /app/
COPY ./logging_test.conf /app/

RUN pip install -U -r /app/requirements.txt

COPY ./static /app/static/
COPY ./${APP_NAME} /app/${APP_NAME}

RUN apt-get update && \
	apt-get -y -q install \
		libreoffice \
