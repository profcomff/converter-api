import os
import platform

if platform.system() == "Windows":

    slash = '\\'
    for root, dirs, files in os.walk('C:\Program Files'):
        if 'soffice.exe' in files:
            libre_path = os.path.join(root, 'soffice.exe')
    command = f' && "{libre_path}" --headless --convert-to pdf '


else:
    slash = '/'
    command = 'cd static; libreoffice --headless --convert-to pdf '

ext_d = os.path.abspath(" ")
cd = ext_d[:-2]+slash+'static'+slash

"""Gets a cd for soffice.exe on Windows and /static directory independently from the OS"""
