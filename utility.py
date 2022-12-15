import os
import sys

import parameters


def transform_to_difference(distances):
    """
    Находит разницу между пикетами.
    :return: список расстояний между точками по разнице пикетов.
    """
    difference_dx = []
    len_list = len(distances) - 1
    for j in range(len_list):
        if j < len_list:
            difference_dx.append(round(float(distances[j + 1]) - float(distances[j]), 2))
    return difference_dx


def transform_to_str(text_int):
    """
    Преобразует числа в строку. Заменяет знак запятой на точку.
    :param text_int: число
    :return:
    """
    return str(text_int).replace(',', '.')


def transform_pk_type_one(pk_integer, pk_float):
    """
    Формируют пикетаж по типу 1+0.00, 2+25.00
    :param pk_integer:
    :param pk_float:
    :return:
    """
    pk = []
    for pk_1, pk_2 in zip(pk_integer, pk_float):
        if 0 < pk_2 < 10 or pk_2 == 0:
            new_pk = f'{int(pk_1)}+0{"{:.2f}".format(float(pk_2))}'
        else:
            new_pk = f'{int(pk_1)}+{"{:.2f}".format(float(pk_2))}'
        pk.append(new_pk)
    return pk


def conditional_horizon(*mark):
    """
    Вычисляет условный горизонт профиля.
    :param mark: список отметок.
    :return:
    """
    mark_w = []
    for i in mark:
        mark_w.extend(i)
    return int(round(min(mark_w) - parameters.CONDITIONAL_HORIZON))


def height_scale(*mark):
    """
    Вычисляет высоту шкалы профиля.
    :param mark: список отметок.
    :return:
    """
    mark_w = []
    for i in mark:
        mark_w.extend(i)
    min_mark = int(round(min(mark_w) - parameters.CONDITIONAL_HORIZON))
    max_mark = int(round(max(mark_w) + parameters.CONDITIONAL_HORIZON))
    return max_mark - min_mark


def transform_pk_to_distance(pk_integer, pk_float):
    """
    Переводит пикетаж в расстояние.
    :param pk_integer: целый пикетаж
    :param pk_float: плюсовой пикетаж
    :return:
    """
    distance_pk = []
    for pk in range(len(pk_float)):
        if 0 < float(pk_float[pk]) < 10 or float(pk_float[pk]) == 0:
            distance = str(int(pk_integer[pk])) + '0' + str(pk_float[pk])
        else:
            distance = str(int(pk_integer[pk])) + str(pk_float[pk])
        distance_pk.append(float(distance))
    return distance_pk


def create_pk_int_float(distance, start_picket):
    """
    Создает два списка с целым пикетажем и плюсовым.
    :param distance: список расстояний между точками
    :param start_picket: стартовый ПК [1, 25]
    :return:
    """
    list_pk_int, list_pk_float = [int(start_picket[0])], [float(start_picket[1])]
    str_pk_int, str_pk_float = list_pk_int[0], list_pk_float[0]
    for d in distance:
        t = str_pk_float + d
        str_pk_float += d
        if round(t, 2) >= 100:
            str_pk_int += 1
            str_pk_float = 0
            list_pk_int.append(int(str_pk_int))
            list_pk_float.append(0)
        else:
            list_pk_float.append(t)
            list_pk_int.append(int(str_pk_int))
    return list_pk_int, list_pk_float


def list_point_insert(chk_state_list, insert_point_start, distance_profile):
    """
    Формирует список начала координат для профилей.
    :param chk_state_list: список кнопок проверок,
    :param insert_point_start: точка вставки профилей
    :param distance_profile: длина профиля
    :return:
    """
    chk_state_list = [i for i in chk_state_list if i == 1]
    x, y = insert_point_start[0], insert_point_start[1]
    result_point_start = [[x, y, 0]]
    len_state_chk_list = len(chk_state_list)

    def _for_append(len_list, new_x):
        for i in range(1, len_list):
            new_x += distance_profile + parameters.OFFSET_NEW_PROFILE + parameters.WIDTH_BASEMENT
            result_point_start.append([new_x, y, 0])

    if len_state_chk_list == 2:
        _for_append(len_state_chk_list, x)
    if len_state_chk_list == 3:
        _for_append(len_state_chk_list, x)
    if len_state_chk_list == 4:
        _for_append(len_state_chk_list, x)
    return result_point_start


def format_decimal(number, decimal_places, difference_type):
    try:
        if difference_type == 'м':
            return "{:.{}f}".format(float(number), decimal_places)
        if difference_type == 'см' or difference_type == 'мм':
            return "{:.{}f}".format(float(number * parameters.DIFFERENCE_TYPE[difference_type]), 0)
    except ValueError:
        return number


def list_styles(acad_doc):
    """
    Определяет список доступны текстовых стилей в текущем чертеже.
    :return:
    """
    try:
        return [style.name for style in acad_doc.TextStyles if style.name]
    except:
        return []


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        p = os.path.join(sys._MEIPASS, relative)
        p = os.path.dirname(p)
        if relative == 'verification.py':
            return p
        else:
            return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
