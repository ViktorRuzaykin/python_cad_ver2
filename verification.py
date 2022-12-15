import json
import os
import sys
import platform
import time
from tkinter import messagebox as mb
import utility


def file_user():
    if hasattr(sys, "_MEIPASS"):
        p = utility.resource_path('verification.py')
    else:
        p = os.getcwd()
    for file in os.listdir(p):
        if file.startswith('user_') and file.endswith('.json'):
            return file


def read_file_environ():
    """
    dw
    :return:
    """
    path_file = utility.resource_path(file_user())
    with open(path_file, 'r') as outfile:
        data_user = json.load(outfile)
    return data_user


def write_environ_user():
    current_environ = os.environ
    platform_user = platform.platform()
    environ_user = {
        'computer_name': current_environ.get('COMPUTERNAME'),
        'os': current_environ.get('OS'),
        'processor_identifier': current_environ.get('processor_identifier'),
        'processor_revision': current_environ.get('processor_revision'),
        'user_domain': current_environ.get('userdomain'),
        'user_domain_roaming_profile': current_environ.get('userdomain_roamingprofile'),
        'username': current_environ.get('username'),
        'processor_architecture': current_environ.get('processor_architecture'),
        'platform': platform_user
    }
    path_file = utility.resource_path(f'user_{environ_user["computer_name"]}.json')
    with open(path_file, 'w') as outfile:
        json.dump(environ_user, outfile, indent=4)


def verification_environ():
    verification = False
    current_environ = os.environ
    user_environ_last = read_file_environ()
    platform_user = platform.platform()
    environ_user_actual = {
        'computer_name': current_environ.get('COMPUTERNAME'),
        'os': current_environ.get('OS'),
        'processor_identifier': current_environ.get('processor_identifier'),
        'processor_revision': current_environ.get('processor_revision'),
        'user_domain': current_environ.get('userdomain'),
        'user_domain_roaming_profile': current_environ.get('userdomain_roamingprofile'),
        'username': current_environ.get('username'),
        'processor_architecture': current_environ.get('processor_architecture'),
        'platform': platform_user
    }
    if (tuple(user_environ_last.values())) == (tuple(environ_user_actual.values())):
        verification = True
    return verification


if verification_environ():
    import visual_tkinter
else:
    mb.showerror(
        "Ошибка при запуске",
        f'Ошибка при запуске. Изменился компьютер. \nОбратитесь к автору продукта.')
