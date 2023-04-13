import os
import platform


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
        comm = f'cd {cd} && "{libre_path}" --headless --convert-to pdf'

    else:
        slash = '/'
        cd = f'{ext_d[:-2]}{slash}static{slash}'
        comm = f'cd {cd}; libreoffice --headless --convert-to pdf'

    def command(filename: str):
        return {'command': f'{comm} {filename}', 'direct': f'{cd}{filename}'}

    return command

# Функция выдает команду и директорию для файла, независимо от ОС
