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

1) Установка LibreOffice должна производиться в Docker'e, иначе при выполнении 
строки через shell возникнут проблемы с доступом к диреткории /static

2) При запуске автоматических тестирований на Windows необходимо в utils/convertable.py
заменить во всех обращениях к shell через run команды 
на соответсвующие ОС, указать полную директорию, 
которую можно удобно узнать в пайчарме, а также полный путь на вашем компьютере до soffice.exe, который указывается в двойных кавычках 
**(!!Но затем вернуть всё к исходному!!)** :
```console
run(f"del C:\Users\user\Documents\GitHub\converter-api\static\{name}")
```
```console
run(f"cd *path*; "*path*\soffice.exe" --headless --convert-to pdf {file_name}")
```

## ENV-file description

DB_DSN=

---
