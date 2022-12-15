import time

import keyboard

from arryautocad import Autocad

acad = Autocad()
mSp = acad.active_model
acadDoc = acad.active_doc

def import_project_marks(help_text):
    """
    Импорт проектных отметок из AutoCad.
    :param help_text: подсказка для выбора.
    :return:
    """
    time.sleep(2)
    dict_mark = {}
    selection_marks = acad.get_selection(help_text)
    time.sleep(0.3)
    for mark in selection_marks:
        coord = float(mark.InsertionPoint[0]) * 1000
        dict_mark[coord] = float(mark.TextString.replace(',', '.'))
        # str(text_int).replace(',', '.')
    dict_for_mark = dict(sorted(dict_mark.items()))
    return list(dict_for_mark.values())


def import_distance_line(help_text):
    """
    Импорт расстояний между отрезками из AutoCAD.
    :param help_text: текст подсказки для вывода в AutoCAD
    :return: список расстояний между точками
    """
    # time.sleep(0.2)
    insert_point = []
    distance_list = []
    while len(insert_point) == 0:
        if keyboard.is_pressed('esc'):  # если нажата клавиша 'ESC' выходим из импорта
            break
        try:
            selection_marks = acad.get_selection(help_text)
            time.sleep(0.3)
            for point in selection_marks:
                # insert_point.append(point.EndPoint[0])  # заполнения списка координатой "Х" отрезка "расстояний"
                insert_point.append(point.StartPoint[0])  # заполнения списка координатой "Х" отрезка "расстояний"
        except:
            insert_point.clear()
    insert_point = sorted(insert_point)
    for count, dist in enumerate(insert_point):
        if count == len(insert_point) - 1:
            break
        d_var = abs(insert_point[count + 1] - dist)
        if d_var != 0:
            distance_list.append(round(d_var, 2))
    return distance_list


print(import_project_marks('Выдели!\n'))
