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

2) При запуске автоматических тестирований на Windows необходимо в get_dir.py
заменить полный путь на вашем компьютере до soffice.exe, если он был установлен нестандартно, который указывается в двойных кавычках 
**(!!Но затем вернуть всё к исходному!!)** :

```console
' && "C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf '
```

## ENV-file description

DB_DSN=

---
