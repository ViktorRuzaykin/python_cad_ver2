import os
import sys
import openpyxl
from tkinter import messagebox as mb, Tk, Label
import auto_cad_ver5

environ_list = ['COMPUTERNAME',
                'OS',
                'PROCESSOR_IDENTIFIER',
                'PROCESSOR_REVISION',
                'USERDOMAIN',
                'USERDOMAIN_ROAMINGPROFILE',
                'USERNAME', ]


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def environ_current_user():
    """
    :return: словарь с текущей окружающей средой
    """
    environ_current = {}
    for list_env in environ_list:
        for curr_env in os.environ:
            if list_env == curr_env:
                rt = os.environ[f'{curr_env}']
                environ_current[f'{list_env}'] = rt
    return environ_current


def verification_environ():
    """
    Проверяет изменилась ли окружающая среда
    :return: True or False
    """
    verification_environ = None
    dict_environ = environ_current_user()
    path = resource_path('user_pc.xlsx')
    wb = openpyxl.reader.excel.load_workbook(filename=path)
    sheet = wb.active
    count = 1
    for i in range(len(environ_list)):
        value = sheet[f'B{count}'].value
        if value != dict_environ[f'{environ_list[count - 1]}']:
            verification_environ = True
            break
        else:
            verification_environ = False
        count += 1
    return verification_environ


def error():
    mb.showerror(
        "Ошибка при запуске",
        f'Ошибка при запуске. Изменился компьютер. \nОбратитесь к автору продукта.')


def verification():
    if verification_environ():
        error()
    else:
        auto_cad_ver5.autocad_len()


verification()
