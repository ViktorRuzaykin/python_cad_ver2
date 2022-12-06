from pyautocad import Autocad, APoint
import csv
import random
from tkinter.filedialog import *
from tkinter import messagebox as mb
from tkinter.ttk import Checkbutton

acad = Autocad()
mSp = acad.model
pk_int = []
pk_float = []
mark_pipe = []
mark_earth = []
mark_pillow = []
mark_ditch = []
mark_filling = []

mark_ditch_fact = []
mark_pillow_fact = []
mark_pipe_fact = []
mark_filling_fact = []

point_start = [0, 0, 0]
h_step = 50  # шаг строк подвала(линии)

# переменные для отклонений
deflections_ditch = random.randint(1, 9) / 100
deflections_pillow = random.randint(1, 6) / 100
deflections_pipe = random.randint(1, 4) / 100
deflections_filling = random.randint(1, 4) / 100

# обработка CSV файла
with open("900-950.csv") as r_file:
    file_reader = csv.reader(r_file, delimiter=";")
    for row in file_reader:
        pk_int.append(row[0])
        pk_float.append(row[1])
        mark_pipe.append(float(row[2]))
        mark_earth.append(float(row[3]))
        mark_ditch.append(float(row[2]) - 1.62)
        mark_pillow.append(float(row[2]) - 1.42)
        mark_filling.append(float(row[2]) + 0.20)

# расчет фактиечкмх отметок по траншеии, подушке, трубе, обсыпке
for i in range(len(mark_pipe)):
    mark_ditch_fact.append(mark_ditch[i] - (random.randint(1, 9) / 100))
    mark_filling_fact.append(mark_filling[i] + (random.randint(1, 4) / 100))

    pillow_fact = mark_pillow[i] - (random.randint(1, 6) / 100)
    dx_pillow_fact_ditch = pillow_fact - mark_ditch_fact[i]

    if dx_pillow_fact_ditch < 0.20:
        mark_pillow_fact.append(pillow_fact + (0.20 - dx_pillow_fact_ditch))
    else:
        mark_pillow_fact.append(pillow_fact)
    mark_pipe_fact.append(mark_pillow_fact[i] + 1.42)

# редактируем список pk_float, заменяем '0' на '00'
for i in range(len(pk_float)):
    if pk_float[i] == '0':
        pk_float[i] = '00'



# переводим ПК в метры
distance_pk = []
for pk in range(len(pk_float)):
    if 0 < float(pk_float[pk]) < 10:
        distance_pk.append(pk_int[pk] + '0' + pk_float[pk])
    else:
        distance_pk.append(pk_int[pk] + pk_float[pk])
# текст для шапки профиля трубы
text_basement_pipe = ['Отметки земли, м', 'Проектные отметки', 'верха трубы, м', 'Фактические отметки',
                      'верха трубы, м', 'Разница в отметках, м', 'Откос',
                      'Ширина дна траншеи', 'Тип прокладки', 'Расстояние, м', 'Пикеты, м']

# текст для шапки профиля траншеи
text_basement_transh = ['Отметки земли, м', 'Проектные отметки', 'дна траншеи, м', 'Фактические отметки',
                        'дна траншеи, м', 'Разница в отметках, м', 'Глубина траншеи, м', 'Откос',
                        'Ширина дна траншеи', 'Тип прокладки', 'Расстояние, м', 'Пикеты, м']

# текст для шапки профиля подушки
text_basement_pillow = ['Фактические отметки', 'дна траншеи, м', 'Проектные отметки', 'верха подушки, м',
                        'Фактические отметки', 'верха подушки, м', 'Толщина слоя подушки, м', 'Откос',
                        'Ширина дна траншеи', 'Тип прокладки', 'Расстояние, м', 'Пикеты, м']

# текст для шапки профиля обсыпки
text_basement_filling = ['Проектные отметки', 'верха обсыпки, м', 'Фактические отметки', 'верха обсыпки, м',
                         'Фактические отметки', 'верха трубы, м', 'Толщина слоя', 'над трубой, м', 'Откос',
                         'Ширина дна траншеи', 'Тип прокладки', 'Расстояние, м', 'Пикеты, м']



# контур шапки подвала
def line_basement(height, width, dx):
    mSp.AddLine(APoint(0 + dx, 0), APoint(0 + dx, height))
    mSp.AddLine(APoint(0 + dx, height), APoint(width + dx, height))
    mSp.AddLine(APoint(width + dx, height), APoint(width + dx, 0))
    mSp.AddLine(APoint(0 + dx, 0), APoint(width + dx, 0))


# горизонтальные черты в шапке подвала
def line_basement_gorizont(h_step, number_line, dx):
    k = 0
    for line in range(0, number_line):
        th = k + h_step
        mSp.AddLine(APoint(0 + dx, th), APoint(264 + dx, th))
        k += h_step


# подпись строк в шапке подвала
def text_basement_hat(text, ditch, dx):
    for i in range(len(ditch)):
        for j in range(len(ditch[i])):
            p = APoint(float(ditch[i][0]), float(ditch[i][1]))
            mSp.AddText(text[i], p, 14)
    mSp.AddLine(APoint(41.37 + dx, 177.55), APoint(244.74 + dx, 177.55))  # дробная черта 'окос/ширина'


def line_longitudinal(s, dx_ditch):
    g = 0
    for e in range(0, s):
        th_2 = g + h_step
        mSp.AddLine(APoint(264 + dx_ditch, th_2), APoint(profile_distance_last + 264 + dx_ditch + distance_1 + distance_2, th_2))
        g += h_step
    mSp.AddLine(APoint(264 + dx_ditch, 0), APoint(264 + profile_distance_last + dx_ditch + distance_1 + distance_2, 0))


# интерполяция начала и конца профиля
def star_end_point():
    dict_start_end = {}
    data_1 = '941+65'
    input_start_pk = data_1.split('+')
    start_pk = ''.join(input_start_pk)

    data_2 = '945+21'
    input_end_pk = data_2.split('+')
    end_pk = ''.join(input_end_pk)

    dict_start_end['data_1'] = data_1
    dict_start_end['data_2'] = data_2

    for pk_st in range(len(distance_pk)):
        if start_pk == distance_pk[pk_st]:
            dict_start_end['int_st'] = True
            dict_start_end['p_start'] = pk_st

        if end_pk == distance_pk[pk_st]:
            dict_start_end['int_end'] = True
            dict_start_end['p_end'] = pk_st+1

        if distance_pk[pk_st - 1] < start_pk < distance_pk[pk_st]:
            dict_start_end['int_st'] = False
            dict_start_end['p_start'] = pk_st
            distance_1 = round(float(distance_pk[pk_st]) - float(start_pk), 2)
            dict_start_end['distance_1'] = distance_1
            first_earth = abs(round(((((mark_earth[pk_st] - mark_earth[pk_st - 1])) / (float(distance_pk[pk_st]) - float(distance_pk[pk_st - 1]))) * distance_1) - mark_earth[pk_st], 2))
            dict_start_end['first_earth'] = first_earth
            first_pipe = abs(round(((((mark_pipe[pk_st] - mark_pipe[pk_st - 1])) / (float(distance_pk[pk_st]) - float(distance_pk[pk_st - 1]))) * distance_1) - mark_pipe[pk_st], 2))
            dict_start_end['first_pipe'] = first_pipe
            first_pillow = round(first_pipe - 1.42, 2)
            dict_start_end['first_pillow'] = first_pillow
            first_filling = round(first_pipe + 0.20, 2)
            dict_start_end['first_filling'] = first_filling
            first_ditch = round(first_pipe - 1.62, 2)
            dict_start_end['first_ditch'] = first_ditch
            first_pipe_fact = round(first_pipe - 0.03, 2)
            dict_start_end['first_pipe_fact'] = first_pipe_fact
            first_pillow_fact = round(first_pillow - 0.03, 2)
            dict_start_end['first_pillow_fact'] = first_pillow_fact
            first_ditch_fact = round(first_ditch - 0.03, 2)
            dict_start_end['first_ditch_fact'] = first_ditch_fact
            first_filling_fact = round(first_filling + 0.03, 2)
            dict_start_end['first_filling_fact'] = first_filling_fact

        if distance_pk[pk_st - 1] < end_pk < distance_pk[pk_st]:
            dict_start_end['int_end'] = False
            dict_start_end['p_end'] = pk_st
            distance_2 = round(float(end_pk) - float(distance_pk[pk_st - 1]), 2)
            dict_start_end['distance_2'] = distance_2
            end_earth = abs(round(((((mark_earth[pk_st] - mark_earth[pk_st - 1])) / (float(distance_pk[pk_st]) - float(distance_pk[pk_st - 1]))) * distance_2) + mark_earth[pk_st-1], 2))
            dict_start_end['end_earth'] = end_earth
            end_pipe = abs(round(((((mark_pipe[pk_st] - mark_pipe[pk_st - 1])) / (float(distance_pk[pk_st]) - float(distance_pk[pk_st - 1]))) * distance_2) + mark_pipe[pk_st-1], 2))
            dict_start_end['end_pipe'] = end_pipe
            end_pillow = round(end_pipe - 1.42, 2)
            dict_start_end['end_pillow'] = end_pillow
            end_filling = round(end_pipe + 0.20, 2)
            dict_start_end['end_filling'] = end_filling
            end_ditch = round(end_pipe - 1.62, 2)
            dict_start_end['end_ditch'] = end_ditch
            end_pipe_fact = round(end_pipe - 0.03, 2)
            dict_start_end['end_pipe_fact'] = end_pipe_fact
            end_pillow_fact = round(end_pillow - 0.03, 2)
            dict_start_end['end_pillow_fact'] = end_pillow_fact
            end_ditch_fact = round(end_ditch - 0.03, 2)
            dict_start_end['end_ditch_fact'] = end_ditch_fact
            end_filling_fact = round(end_filling + 0.03, 2)
            dict_start_end['end_filling_fact'] = end_filling_fact
    print(dict_start_end)
    return dict_start_end


s_e_p = star_end_point()

p_start = s_e_p['p_start']
p_end = s_e_p['p_end']
if s_e_p['int_st'] == False:
    distance_1 = s_e_p['distance_1']
else:
    distance_1 = 0
if s_e_p['int_end'] == False:
    distance_2 = s_e_p['distance_2']
else:
    distance_2 = 0

new_distance_pk = distance_pk[p_start:p_end]
new_mark_earth = mark_earth[p_start:p_end]
new_mark_ditch = mark_ditch[p_start:p_end]
new_mark_ditch_fact = mark_ditch_fact[p_start:p_end]
new_mark_pillow = mark_pillow[p_start:p_end]
new_mark_pillow_fact = mark_pillow_fact[p_start:p_end]
new_mark_pipe = mark_pipe[p_start:p_end]
new_mark_pipe_fact = mark_pipe_fact[p_start:p_end]
new_mark_filling = mark_filling[p_start:p_end]
new_mark_filling_fact = mark_filling_fact[p_start:p_end]


new_pk_int = pk_int[p_start:p_end]
new_pk_float = pk_float[p_start:p_end]

# расчет длинны профиля (нач. ПК - конеч. ПК)
a = float(new_pk_int[0] + new_pk_float[0])
b = float(new_pk_int[-1] + new_pk_float[-1])
profile_distance = b - a
profile_distance_last = float(profile_distance + 40)

# расчет смещения для профилей
dx_pipe = profile_distance_last + 500
dx_ditch = dx_pipe
dx_pillow = dx_pipe + profile_distance_last + 500
dx_filling = dx_pillow + profile_distance_last + 500
dx_ditch_earth = (new_mark_earth[0] - new_mark_ditch[0]) * 25

coordinates_text_basement_pipe = [[77.17 + dx_pipe, 370.16], [61.21 + dx_pipe, 331.63],
                                  [109.57 + dx_pipe, 312.79], [41.84 + dx_pipe, 280.54],
                                  [108.31 + dx_pipe, 259.99], [33.89 + dx_pipe, 220.16],
                                  [94.81 + dx_pipe, 181.78], [47.29 + dx_pipe, 160.97],
                                  [119.41 + dx_pipe, 118.63], [116.18 + dx_pipe, 68.49],
                                  [153.10 + dx_pipe, 21.65]]

coordinates_text_basement_pillow = [[43.21 + dx_pillow, 378.69], [99.61 + dx_pillow, 359.85],
                                    [61.294 + dx_pillow, 330.54], [91.89 + dx_pillow, 309.99],
                                    [43.240 + dx_pillow, 280.54], [91.89 + dx_pillow, 259.99],
                                    [17.158 + dx_pillow, 219.802], [94.810 + dx_pillow, 181.780],
                                    [47.290 + dx_pillow, 160.970], [119.410 + dx_pillow, 118.630],
                                    [116.180 + dx_pillow, 69.180], [153.100 + dx_pillow, 18.740]]

coordinates_text_basement_filling = [[61.42 + dx_filling, 378.99], [93.90 + dx_filling, 360.15],
                                     [43.16 + dx_filling, 330.54], [93.58 + dx_filling, 309.99],
                                     [43.16 + dx_filling, 280.54], [109.30 + dx_filling, 259.99],
                                     [125.29 + dx_filling, 230.54], [117.14 + dx_filling, 209.99],
                                     [94.81 + dx_filling, 181.78], [50.32 + dx_filling, 160.97],
                                     [119.41 + dx_filling, 118.63], [116.18 + dx_filling, 69.18],
                                     [153.10 + dx_filling, 18.7]]

coordinates_text_basement_transh = [[78.50, 418.58], [61.21, 381.63],
                                    [99.61, 362.79], [41.84, 330.54],
                                    [98.35, 309.99], [33.89, 270.16],
                                    [62.96, 221.11], [94.81, 181.78],
                                    [47.29, 160.97], [119.41, 118.63],
                                    [116.18, 69.18], [153.10, 18.74]]


def basement_all_ditch():
    line_last = float(new_distance_pk[-1]) - float(new_distance_pk[0]) + distance_1 + distance_2
    # начальня риска и расстояние в строке "Растояния"
    if s_e_p['int_st'] == False:
        mSp.AddLine(APoint(304.00 + distance_1, 50.00), APoint(304.00 + distance_1, 70.00))
        mSp.AddText(format(distance_1, '.2f'), APoint(304.00 + (distance_1 / 2 + 5), 61.30), 10)

        # начальная отметка земли
        mSp.AddText(s_e_p['first_earth'], APoint(304.00, 404.75), 10)
        # начальная проектная отметка траншеии
        mSp.AddText(s_e_p['first_ditch'], APoint(304.00, 354.33), 10)
        # начальная фактическая  отметка траншеии
        mSp.AddText(s_e_p['first_ditch_fact'], APoint(304.00, 304.35), 10)
        # начальное отклонение
        mSp.AddText(round(s_e_p['first_ditch_fact'] - s_e_p['first_ditch'], 2), APoint(304.00, 256.83), 10)
        # начальная глубина разработки
        mSp.AddText(round(s_e_p['first_earth'] - s_e_p['first_ditch_fact'], 2), APoint(304.00, 209.99), 10)


    # отметка земли
    mSp.AddText(new_mark_earth[0], APoint(304.00 + distance_1, 404.75), 10)
    # начальная проектная отметка траншеии
    mSp.AddText(new_mark_ditch[0], APoint(304.00 + distance_1, 354.33), 10)
    # фактическая  отметка траншеии
    mSp.AddText(new_mark_ditch_fact[0], APoint(304.00 + distance_1, 304.35), 10)
    # отклонение
    mSp.AddText(format(float(new_mark_ditch_fact[0]) - float(new_mark_ditch[0]), '.2f'),
                APoint(304.00 + distance_1, 256.83), 10)
    # глубина разработки
    mSp.AddText(round(new_mark_earth[0] - new_mark_ditch_fact[0], 2), APoint(304.00 + distance_1, 209.99), 10)
    # начальный ПК в строке "Пикеты"
    mSp.AddText(s_e_p['data_1'], APoint(278.00, 32), 10)
    mSp.AddLine(APoint(304.00, 50.00), APoint(304.00, 70.00))



    p = 304.00 + distance_1
    for i in range(len(new_distance_pk) - 1):
        pk_dist = round(float(new_distance_pk[i + 1]) - float(new_distance_pk[i]), 2)
        dh_x = p + pk_dist
        mSp.AddLine(APoint(dh_x, 70.00), APoint(dh_x, 50.00))
        # подпись расстояния
        otstup_text = pk_dist - (pk_dist / 2 + 5)
        mSp.AddText(format(pk_dist, '.2f'), APoint(dh_x - otstup_text, 61.30), 10)
        p += pk_dist
        # отметки верха земли
        mSp.AddText(format(float(new_mark_earth[i + 1]), '.2f'), APoint(dh_x, 404.75), 10)
        # проектные отметки дна траншеии
        mSp.AddText(format(float(new_mark_ditch[i + 1]), '.2f'), APoint(dh_x, 354.33), 10)
        # фактические отметки дна траншеи
        mSp.AddText(format(new_mark_ditch_fact[i + 1], '.2f'), APoint(dh_x, 304.35), 10)
        # отклонения от проекта по дну трашеи
        mSp.AddText(round(new_mark_ditch_fact[i + 1] - new_mark_ditch[i + 1], 2), APoint(dh_x, 256.83), 10)
        # глубина разработки траншеи
        development_depth = format(round(new_mark_earth[i + 1] - new_mark_ditch_fact[i + 1], 2), '.2f')
        mSp.AddText(development_depth, APoint(dh_x, 209.99), 10)
        piket = new_pk_int[i + 1]
        cutoff = len(piket[1])-(len(piket[1])-2)
        if new_pk_float[i + 1] == '00':
            mSp.AddLine(APoint(dh_x, 100.00), APoint(dh_x, 50.00))
            if piket[cutoff:] == '0' or piket[cutoff:] == '5':
                mSp.AddText(piket, APoint(dh_x - 15, 32), 10)
            else:
                mSp.AddText(piket[cutoff:], APoint(dh_x - 3.24, 32), 10)
    f = new_distance_pk[0]
    if f[-2:] == '00':
        mSp.AddLine(APoint(304.00 + distance_1, 100.00), APoint(304.00 + distance_1, 50.00))

    if s_e_p['int_end'] == False:
        # конечная отметка земли
        mSp.AddText(format(s_e_p['end_earth'], '.2f'), APoint(304.00 + line_last, 404.75), 10)
        # конечная проектная отметка траншеии
        mSp.AddText(format(s_e_p['end_ditch'], '.2f'), APoint(304.00 + line_last, 354.33), 10)
        # конечная фактическая  отметка траншеии
        mSp.AddText(format(s_e_p['end_ditch_fact'], '.2f'), APoint(304.00 + line_last, 304.35), 10)
        # конечное отклонение
        mSp.AddText(format(round(s_e_p['end_ditch_fact'] - s_e_p['end_ditch'], 2), '.2f'), APoint(304.00 + line_last, 256.83), 10)
        # конечная глубина разработки
        mSp.AddText(format(round(s_e_p['end_earth'] - s_e_p['end_ditch_fact'], 2), '.2f'), APoint(304.00 + line_last, 209.99), 10)
        # конечная риска и расстояние в строке "Растояния"
        mSp.AddLine(APoint(304.00 + line_last, 50.00), APoint(304.00 + line_last, 70.00))
        mSp.AddText(format(distance_2, '.2f'), APoint(304.00 + line_last - (distance_2 / 2 - 5), 61.30), 10)
        
    # конечный ПК в строке "Пикеты"
    mSp.AddText(s_e_p['data_2'], APoint(304.00 + line_last, 32), 10)


def basement_all_pillow():
    line_last = float(new_distance_pk[-1]) - float(new_distance_pk[0]) + distance_1 + distance_2

    if s_e_p['int_st'] == False:
        # начальня риска в строке "Растояния"
        mSp.AddLine(APoint(304.00 + dx_pillow + distance_1, 50.00), APoint(304.00 + dx_pillow + distance_1, 70.00))
        mSp.AddText(format(distance_1, '.2f'), APoint(304.00 + dx_pillow + (distance_1 / 2 + 5), 61.30), 10)
        # начальная фактическая отметка дна траншеии
        mSp.AddText(s_e_p['first_ditch_fact'], APoint(304.00 + dx_pillow, 354.33), 10)
        # начальная проектная отметка верха подушки
        mSp.AddText(s_e_p['first_pillow'], APoint(304.00 + dx_pillow, 304.35), 10)
        # начальная фактическая отметка верха подушки
        mSp.AddText(round(s_e_p['first_pillow_fact'], 2), APoint(304.00 + dx_pillow, 254.35), 10)
        # начальная толщина подушки
        mSp.AddText(format(round(s_e_p['first_pillow_fact'] - s_e_p['first_ditch_fact'], 2), '.2f'), APoint(304.00 + dx_pillow, 210.00), 10)


    # фактическая отметка дна траншеии
    mSp.AddText(new_mark_ditch_fact[0], APoint(304.00 + dx_pillow + distance_1, 354.33), 10)
    # проектная отметка верха подушки
    mSp.AddText(new_mark_pillow[0], APoint(304.00 + dx_pillow + distance_1, 304.35), 10)
    # фактическая отметка верха подушки
    mSp.AddText(round(new_mark_pillow_fact[0], 2), APoint(304.00 + dx_pillow + distance_1, 254.35), 10)
    # толщина подушки
    mSp.AddText(format(round(float(new_mark_pillow_fact[0]) - float(new_mark_ditch_fact[0]), 2), '.2f'),
                APoint(304.00 + dx_pillow + distance_1, 210.00), 10)
    # начальный ПК в строке "Пикеты"
    mSp.AddText(s_e_p['data_1'], APoint(278.00 + dx_pillow, 32), 10)
    mSp.AddLine(APoint(304.00 + dx_pillow, 50.00), APoint(304.00 + dx_pillow, 70.00))


    p = 304.00 + distance_1
    for i in range(len(new_distance_pk) - 1):
        pk_dist = round(float(new_distance_pk[i + 1]) - float(new_distance_pk[i]), 2)
        # проставка рисок в строке "Растояния"
        dh_x = p + pk_dist
        mSp.AddLine(APoint(dh_x + dx_pillow, 70.00), APoint(dh_x + dx_pillow, 50.00))
        # подпись расстояния
        otstup_text = pk_dist - (pk_dist / 2 + 5)
        mSp.AddText(format(pk_dist, '.2f'), APoint(dh_x - otstup_text + dx_pillow, 61.30), 10)
        p += pk_dist
        # фактическая отметка дна траншеии
        mSp.AddText(format(float(new_mark_ditch_fact[i + 1]), '.2f'), APoint(dh_x + dx_pillow, 354.33), 10)
        # проектная отметка верха подушки
        mSp.AddText(format(float(new_mark_pillow[i + 1]), '.2f'), APoint(dh_x + dx_pillow, 304.35), 10)
        # фактические отметки верха подушки
        mSp.AddText(format(new_mark_pillow_fact[i + 1], '.2f'), APoint(dh_x + dx_pillow, 254.35), 10)
        # толщина слоя подушки
        mSp.AddText(format(round(new_mark_pillow_fact[i + 1] - new_mark_ditch_fact[i + 1], 2), '.2f'), APoint(dh_x + dx_pillow, 210.00), 10)

        piket = new_pk_int[i + 1]
        cutoff = len(piket[1]) - (len(piket[1]) - 2)
        if new_pk_float[i + 1] == '00':
            mSp.AddLine(APoint(dh_x + dx_pillow, 100.00), APoint(dh_x + dx_pillow, 50.00))
            if piket[cutoff:] == '0' or piket[cutoff:] == '5':
                mSp.AddText(piket, APoint(dh_x - 15 + dx_pillow, 32), 10)
            else:
                mSp.AddText(piket[cutoff:], APoint(dh_x - 3.24 + dx_pillow, 32), 10)
    f = new_distance_pk[0]
    if f[-2:] == '00':
        mSp.AddLine(APoint(304.00 + distance_1 + dx_pillow, 100.00), APoint(304.00 + distance_1 + dx_pillow, 50.00))

    if s_e_p['int_end'] == False:
        # конечная фактическая отметка дна траншеии
        mSp.AddText(s_e_p['end_ditch_fact'], APoint(304.00 + dx_pillow + line_last, 354.33), 10)
        # конечная проектная отметка верха подушки
        mSp.AddText(s_e_p['end_pillow'], APoint(304.00 + dx_pillow + line_last, 304.35), 10)
        # конечная фактическая отметка верха подушки
        mSp.AddText(round(s_e_p['end_pillow_fact'], 2), APoint(304.00 + dx_pillow + line_last, 254.35), 10)
        # конечная толщина подушки
        mSp.AddText(format(round(s_e_p['end_pillow_fact'] - s_e_p['end_ditch_fact'], 2), '.2f'),
                    APoint(304.00 + dx_pillow + line_last, 210.00), 10)
        # конечная риска и расстояние в строке "Растояния"
        mSp.AddLine(APoint(304.00 + dx_pillow + line_last, 50.00), APoint(304.00 + dx_pillow + line_last, 70.00))
        mSp.AddText(format(distance_2, '.2f'), APoint(304.00 + dx_pillow + line_last - (distance_2 / 2 - 5), 61.30), 10)

    # конечный ПК в строке "Пикеты"
    mSp.AddText(s_e_p['data_2'], APoint(304.00 + line_last + dx_pillow, 32), 10)


def basement_all_pipe():
    line_last = float(new_distance_pk[-1]) - float(new_distance_pk[0]) + distance_1 + distance_2

    if s_e_p['int_st'] == False:
        # начальня риска в строке "Растояния"
        mSp.AddText(format(distance_1, '.2f'), APoint(304.00 + dx_pipe + (distance_1 / 2 + 5), 61.30), 10)
        mSp.AddLine(APoint(304.00 + dx_pipe + distance_1, 50.00), APoint(304.00 + dx_pipe + distance_1, 70.00))
        # начальная отметка земли
        mSp.AddText(s_e_p['first_earth'], APoint(304.00 + dx_pipe, 404.33), 10)
        # начальная проектная отметка трубы
        mSp.AddText(s_e_p['first_pipe'], APoint(304.00 + dx_pipe, 354.35), 10)
        # начальная фактическая отметка трубы
        mSp.AddText(s_e_p['first_pipe_fact'], APoint(304.00 + dx_pipe, 303.42), 10)
        # начальное отклонение (-0,03)
        mSp.AddText(round(s_e_p['first_pipe_fact'] - s_e_p['first_pipe'], 2), APoint(304.00 + dx_pipe, 255.35), 10)


    # отметка земли
    mSp.AddText(new_mark_earth[0], APoint(304.00 + dx_pipe + distance_1, 404.33), 10)
    # проектная отметка трубы
    mSp.AddText(new_mark_pipe[0], APoint(304.00 + dx_pipe + distance_1, 354.35), 10)
    # фактическая отметка трубы
    mSp.AddText(new_mark_pipe_fact[0], APoint(304.00 + dx_pipe + distance_1, 303.42), 10)
    # отклонение (-0,03)
    mSp.AddText(round(new_mark_pipe_fact[0] - new_mark_pipe[0], 2), APoint(304.00 + dx_pipe + distance_1, 255.35),
                10)
    # начальный ПК в строке "Пикеты"
    mSp.AddText(s_e_p['data_1'], APoint(280.00 + dx_pipe, 32), 10)
    mSp.AddLine(APoint(304.00 + dx_pipe, 50.00), APoint(304.00 + dx_pipe, 70.00))



    p = 304.00 + distance_1
    for i in range(len(new_distance_pk) - 1):
        pk_dist = round(float(new_distance_pk[i + 1]) - float(new_distance_pk[i]), 2)
        # проставка рисок в строке "Растояния"
        dh_x = p + pk_dist
        mSp.AddLine(APoint(dh_x + dx_pipe, 70.00), APoint(dh_x + dx_pipe, 50.00))
        # подпись расстояния
        otstup_text = pk_dist - (pk_dist / 2 + 5)
        mSp.AddText(format(pk_dist, '.2f'), APoint(dh_x - otstup_text + dx_pipe, 61.30), 10)
        p += pk_dist
        # отметки верха земли
        mSp.AddText(format(float(new_mark_earth[i + 1]), '.2f'), APoint(dh_x + dx_pipe, 404.33), 10)
        # проектные отметки трубы
        mSp.AddText(format(float(new_mark_pipe[i + 1]), '.2f'), APoint(dh_x + dx_pipe, 354.35), 10)
        # фактические отметки трубы
        mSp.AddText(format(new_mark_pipe_fact[i + 1], '.2f'), APoint(dh_x + dx_pipe, 303.42), 10)
        # отклонения от проекта по трубе
        mSp.AddText(round(new_mark_pipe_fact[i + 1] - new_mark_pipe[i + 1], 2), APoint(dh_x + dx_pipe, 255.35), 10)

        piket = new_pk_int[i + 1]
        cutoff = len(piket[1]) - (len(piket[1]) - 2)
        if new_pk_float[i + 1] == '00':
            mSp.AddLine(APoint(dh_x + dx_pipe, 100.00), APoint(dh_x + dx_pipe, 50.00))
            if piket[cutoff:] == '0' or piket[cutoff:] == '5':
                mSp.AddText(piket, APoint(dh_x - 15 + dx_pipe, 32), 10)
            else:
                mSp.AddText(piket[cutoff:], APoint(dh_x - 3.24 + dx_pipe, 32), 10)
    f = new_distance_pk[0]
    if f[-2:] == '00':
        mSp.AddLine(APoint(304.00 + distance_1 + dx_pipe, 100.00), APoint(304.00 + distance_1 + dx_pipe, 50.00))

    if s_e_p['int_end'] == False:
        # конечная отметка земли
        mSp.AddText(s_e_p['end_earth'], APoint(304.00 + dx_pipe + line_last, 404.33), 10)
        # конечная проектная отметка трубы
        mSp.AddText(s_e_p['end_pipe'], APoint(304.00 + dx_pipe + line_last, 354.35), 10)
        # конечная фактическая отметка трубы
        mSp.AddText(s_e_p['end_pipe_fact'], APoint(304.00 + dx_pipe + line_last, 303.42), 10)
        # конечное отклонение (-0,03)
        mSp.AddText(round(s_e_p['end_pipe_fact'] - s_e_p['end_pipe'], 2), APoint(304.00 + dx_pipe + line_last, 255.35), 10)
        mSp.AddText(s_e_p['data_2'], APoint(304.00 + line_last + dx_pipe, 32), 10)
        # конечная риска и расстояние в строке "Растояния"
        mSp.AddLine(APoint(304.00 + dx_pipe + line_last, 50.00), APoint(304.00 + dx_pipe + line_last, 70.00))
        mSp.AddText(format(distance_2, '.2f'), APoint(304.00 + dx_pipe + line_last - (distance_2 / 2 - 5), 61.30), 10)


def basement_all_filling():
    line_last = float(new_distance_pk[-1]) - float(new_distance_pk[0]) + distance_1 + distance_2
    if s_e_p['int_st'] == False:
        # начальня риска в строке "Растояния"
        mSp.AddLine(APoint(304.00 + distance_1 + dx_filling, 50.00), APoint(304.00 + distance_1 + dx_filling, 70.00))
        mSp.AddText(format(distance_1, '.2f'), APoint(304.00 + dx_filling + (distance_1 / 2 + 5), 61.30), 10)
        # начальная проектная отметка верха обсыпки
        mSp.AddText(s_e_p['first_filling'], APoint(304.00 + dx_filling, 354.33), 10)
        # начальная фактическая отметка верха обсыпки
        mSp.AddText(s_e_p['first_filling_fact'], APoint(304.00 + dx_filling, 303.86), 10)
        # начальная фактическая отметка верха трубы
        mSp.AddText(s_e_p['first_pipe_fact'], APoint(304.00 + dx_filling, 253.88), 10)
        # начальная толщина обсыпки
        mSp.AddText(format(round(s_e_p['first_filling_fact'] - s_e_p['first_pipe_fact'], 2), '.2f'), APoint(304.00 + dx_filling, 210.80), 10)


    mSp.AddText(new_mark_filling[0], APoint(304.00 + dx_filling + distance_1, 354.33), 10)
    # фактическая отметка верха обсыпки
    mSp.AddText(new_mark_filling_fact[0], APoint(304.00 + dx_filling + distance_1, 303.86), 10)
    # фактическая отметка верха трубы
    mSp.AddText(new_mark_filling_fact[0], APoint(304.00 + dx_filling + distance_1, 253.88), 10)
    # толщина обсыпки
    mSp.AddText(format(round(float(new_mark_filling_fact[0]) - float(new_mark_pipe_fact[0]), 2), '.2f'),
                APoint(304.00 + dx_filling + distance_1, 210.80), 10)
    # начальный ПК в строке "Пикеты"

    mSp.AddText(s_e_p['data_1'], APoint(280.00 + dx_filling, 32), 10)
    mSp.AddLine(APoint(304.00 + dx_filling, 50.00), APoint(304.00 + dx_filling, 70.00))



    p = 304.00  + distance_1
    for i in range(len(new_distance_pk) - 1):
        pk_dist = round(float(new_distance_pk[i + 1]) - float(new_distance_pk[i]), 2)
        # проставка рисок в строке "Растояния"
        dh_x = p + pk_dist
        mSp.AddLine(APoint(dh_x + dx_filling, 70.00), APoint(dh_x + dx_filling, 50.00))
        # подпись расстояния
        otstup_text = pk_dist - (pk_dist / 2 + 5)
        mSp.AddText(format(pk_dist, '.2f'), APoint(dh_x - otstup_text + dx_filling, 61.30), 10)
        p += pk_dist
        # проектная отметка верха обсыпки
        mSp.AddText(format(float(new_mark_filling[i + 1]), '.2f'), APoint(dh_x + dx_filling, 354.33), 10)
        # фактическая отметка верха обсыпки
        mSp.AddText(format(float(new_mark_filling_fact[i + 1]), '.2f'), APoint(dh_x + dx_filling, 303.86), 10)
        # фактические отметки верха трубы
        mSp.AddText(format(new_mark_pipe_fact[i + 1], '.2f'), APoint(dh_x + dx_filling, 253.88), 10)
        # толщина слоя обсыпки
        mSp.AddText(format(round(new_mark_filling_fact[i + 1] - new_mark_pipe_fact[i + 1], 2), '.2f'),
                    APoint(dh_x + dx_filling, 210.80), 10)

        piket = new_pk_int[i + 1]
        cutoff = len(piket[1]) - (len(piket[1]) - 2)
        if new_pk_float[i + 1] == '00':
            mSp.AddLine(APoint(dh_x + dx_filling, 100.00), APoint(dh_x + dx_filling, 50.00))
            if piket[cutoff:] == '0' or piket[cutoff:] == '5':
                mSp.AddText(piket, APoint(dh_x - 15 + dx_filling, 32), 10)
            else:
                mSp.AddText(piket[cutoff:], APoint(dh_x - 3.24 + dx_filling, 32), 10)
    f = new_distance_pk[0]
    if f[-2:] == '00':
        mSp.AddLine(APoint(304.00 + distance_1 + dx_filling, 100.00), APoint(304.00 + distance_1 + dx_filling, 50.00))

    if s_e_p['int_end'] == False:
        # конечная проектная отметка верха обсыпки
        mSp.AddText(s_e_p['end_filling'], APoint(304.00 + dx_filling + line_last, 354.33), 10)
        # конечная фактическая отметка верха обсыпки
        mSp.AddText(s_e_p['end_filling_fact'], APoint(304.00 + dx_filling + line_last, 303.86), 10)
        # конечная фактическая отметка верха трубы
        mSp.AddText(s_e_p['end_pipe_fact'], APoint(304.00 + dx_filling + line_last, 253.88), 10)
        # конечная толщина обсыпки
        mSp.AddText(format(round(s_e_p['end_filling_fact'] - s_e_p['end_pipe_fact'], 2), '.2f'),
                    APoint(304.00 + dx_filling + line_last, 210.80), 10)
        # конечная риска и расстояние в строке "Растояния"
        mSp.AddLine(APoint(304.00 + dx_filling + line_last, 50.00), APoint(304.00 + dx_filling + line_last, 70.00))
        mSp.AddText(format(distance_2, '.2f'), APoint(304.00 + dx_filling + line_last - (distance_2 / 2 - 5), 61.30), 10)

    # конечный ПК в строке "Пикеты"
    mSp.AddText(s_e_p['data_2'], APoint(304.00 + line_last + dx_filling, 32), 10)


def height_scale(dx, r1, data_1, data_2):
    min_mark_pipe = int(round(min(data_1) - 2))
    max_mark_pipe = int(round(max(data_2) + 2))
    r = r1 + 20
    for q in range(max_mark_pipe - min_mark_pipe):
        t_505 = APoint((264 - 33) + dx, r)
        mSp.AddText(min_mark_pipe, t_505, 10)
        min_mark_pipe += 1
        r += 25
    mSp.AddLine(APoint(264 + dx, r1), APoint(264 + dx, r - 20))


def profile_line(g, dx, list_1, list_2, dx_transh_earth):
    min_mark = int(round(min(list_1)) - 2)
    x_1 = 264 + 40 + dx
    y_1 = g + (list_1[0] - min_mark) * 25 + 25

    for lp in range(len(list_1) - 1):
        x_2 = x_1 + (float(new_distance_pk[lp + 1]) - float(new_distance_pk[lp]))
        y_2 = y_1 + ((list_1[lp + 1] - list_1[lp]) * 25)
        mSp.AddLine(APoint(x_1, y_1), APoint(x_2, y_2))
        mSp.AddLine(APoint(x_1, g), APoint(x_1, y_1))
        x_1 = x_2
        y_1 = y_2
    mSp.AddLine(APoint(x_1, g), APoint(x_1, y_1, ))

    x_1 = 264 + 40 + dx
    y_1 = g + (list_1[0] - min_mark) * 25 + 25 + dx_transh_earth
    for lp in range(len(list_2) - 1):
        x_2 = x_1 + (float(new_distance_pk[lp + 1]) - float(new_distance_pk[lp]))
        y_2 = y_1 + ((list_2[lp + 1] - list_2[lp]) * 25)
        mSp.AddLine(APoint(x_1, y_1), APoint(x_2, y_2))
        x_1 = x_2
        y_1 = y_2


def ditch():
    # простроение подвала разработки
    line_basement(450, 264, 0)  # контур шапки подвала (разработка)
    line_basement_gorizont(h_step, 8, 0)  # горизонтальные черты в шапке подвала (разработка)
    #text_basement_hat(text_basement_transh, coordinates_text_basement_transh, 0)  # подпись строк в шапке подвала (разработка)
    line_longitudinal(9, 0)  # продольные линии подвара (разработка)
    basement_all_ditch()  # запонение строк подвала (разработка)
    height_scale(0, 450, new_mark_ditch, new_mark_earth)  # шкала (разработка)
    profile_line(450, 0, new_mark_ditch, new_mark_earth, dx_ditch_earth)


def pillow():
    line_basement(400, 264, dx_pillow)
    line_basement_gorizont(h_step, 7, dx_pillow)
   # text_basement_hat(text_basement_pillow, coordinates_text_basement_pillow, dx_pillow)
    line_longitudinal(8, dx_pillow)
    basement_all_pillow()
    height_scale(dx_pillow, 400, new_mark_ditch, new_mark_pillow)
    dx_pillow_ditch = (new_mark_pillow_fact[0] - new_mark_ditch_fact[0]) * 25
    #profile_line(400, dx_pillow, new_mark_ditch, new_mark_pillow, dx_pillow_ditch)


def pipe():
    # простроение подвала укладки
    line_basement(450, 264, dx_pipe)  # контур шапки подвала (укладка)
    line_basement_gorizont(h_step, 8, dx_pipe)  # горизонтальные черты в шапке подвала (укладка)
    #text_basement_hat(text_basement_pipe, coordinates_text_basement_pipe, dx_pipe)  # подпись строк в шапке подвала (укладка)
    line_longitudinal(9, dx_pipe)  # продольные линии подвара (укладка)
    basement_all_pipe()
    height_scale(dx_pipe, 450, new_mark_pipe, new_mark_earth)  # шкала (разработка)
    dx_pipe_earth = (new_mark_earth[0] - new_mark_pipe[0]) * 25
    #profile_line(450, dx_pipe, new_mark_pipe, new_mark_earth, dx_pipe_earth)


def filling():
    line_basement(400, 264, dx_filling)
    line_basement_gorizont(h_step, 7, dx_filling)
    #text_basement_hat(text_basement_filling, coordinates_text_basement_filling, dx_filling)
    line_longitudinal(8, dx_filling)
    basement_all_filling()
    height_scale(dx_filling, 400, new_mark_pipe, new_mark_filling)
    dx_filling_pipe = (new_mark_filling[0] - new_mark_pipe[0]) * 25
    #profile_line(400, dx_filling, new_mark_pipe, new_mark_filling, dx_filling_pipe)


ditch()
#pillow()
#pipe()
#filling()

print(new_distance_pk)

'''
def test():
    if chk_state_ditch.get() == True:

        print('Aktiv')
'''


window = Tk()
window.title("Ленивчик")
window.geometry('500x150')

start_pk = Label(window, text="Начальный ПК:", font=('Arial Bold', 9))
start_pk.grid(column=0, row=2)

input_start_pk = Entry(window, width=10, text="15151")
input_start_pk.grid(column=1, row=2)

end_pk = Label(window, text="Конечный ПК:", font=('Arial Bold', 9))
end_pk.grid(column=0, row=3)

input_end_pk = Entry(window, width=10, text="1")
input_end_pk.grid(column=1, row=3)

btn = Button(window, text="  Облениться совсем ", width=20)
btn.grid(column=2, row=7)

end_pk = Label(window, text="Запусти AutoCAD", font=('Arial Bold', 9))
end_pk.grid(column=2, row=6)

btn_1 = Button(window, text="Открыть")
btn_1.grid(column=3, row=0)

lbl_1 = Label(window, text='Выбери файл для работы -->', font=('Arial Bold', 9), foreground="white",
              background="#ff9d00")
lbl_1.grid(column=2, row=0)

chk_state_ditch = IntVar()
chk_state_ditch.set(0)
chk_ditch = Checkbutton(window, text='Разработка', var=chk_state_ditch)
chk_ditch.grid(column=2, row=2)

chk_state_pillow = IntVar()
chk_state_pillow.set(0)
chk_pillow = Checkbutton(window, text='Подушка', var=chk_state_pillow)
chk_pillow.grid(column=3, row=2)

chk_state_pipe = IntVar()
chk_state_pipe.set(0)
chk_pipe = Checkbutton(window, text='Укладка      ', var=chk_state_pipe)
chk_pipe.grid(column=2, row=3)

chk_state_filling = IntVar()
chk_state_filling.set(0)
chk = Checkbutton(window, text='Обсыпка', var=chk_state_filling)
chk.grid(column=3, row=3)



window.mainloop()
