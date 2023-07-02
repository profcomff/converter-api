run:
	source ./venv/bin/activate && uvicorn --reload --log-config logging_dev.conf file_converter.routes.base:app

configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	autoflake -r --in-place --remove-all-unused-imports ./file_converter
	isort ./file_converter
	black ./file_converter

dev-format: format
	autoflake -r --in-place --remove-all-unused-imports ./tests
	isort ./tests
	black ./tests

