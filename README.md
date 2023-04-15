# file-converter

Конвертер файлов, основан на libre office. 

## Запуск

1) Перейдите в папку проекта

2) Создайте виртуальное окружение командой:
```console
foo@bar:~$ python3 -m venv ./venv/
```

3) Установите библиотеки 
```console
foo@bar:~$ pip install -r requirements.txt
```
4) Запускайте приложение!
```console
foo@bar:~$ python -m file_converter
```

## Тестирование и LibreOffice

1) Установка LibreOffice должна производиться в Docker, иначе при выполнении 
строки через shell возникнут проблемы с доступом к диреткории /static

2) При запуске автоматических тестирований  на Windows в случае нестандартной установки 
libreoffice - проверить директорию и добавить ее в список для поиска в get_dir:

```console
paths = ['\\Program Files', '\\Program Files (x86)', '\\ProgramData', '\\Users']
```
3) Для тестирований создать отдельно .env и прописать:

```console
STATIC_FOLDER=static
```

## ENV-file description

DB_DSN=

---
