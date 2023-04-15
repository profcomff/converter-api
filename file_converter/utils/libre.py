import os
import platform

from file_converter.exceptions import ConvertError
from file_converter.utils.commands import run


def find(name: str, paths: list):
    for path in paths:
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)


# Поиск по базовым катологам, куда мог быть установлен soffice


def get_command():
    OS = platform.system()
    ext_d = os.path.abspath(" ")

    if OS == "Windows":
        paths = ['\\Program Files', '\\Program Files (x86)', '\\ProgramData', '\\Users']
        slash = '\\'
        cd = f'{ext_d[:-2]}{slash}static{slash}'
        libre_path = find('soffice.exe', paths)
        command = f'cd {cd} && "{libre_path}" --headless --convert-to pdf'

    else:
        slash = '/'
        cd = f'{ext_d[:-2]}{slash}static{slash}'
        command = f'cd {cd}; libreoffice --headless --convert-to pdf'

    async def command_exec(filename: str, _new_filename: str):
        await run(f'{command} {filename}')
        os.remove(f'{cd}{filename}')  # Удаляет старый файл после конвертации
        if not os.path.exists(f'{cd}{_new_filename}'):  # Проверка на успешность конвертации
            raise ConvertError()

    return command_exec


# Функция выполняет команду и получает директорию для файла, независимо от ОС
