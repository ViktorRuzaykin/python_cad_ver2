from pyautocad import Autocad, APoint
import csv
import random

acad = Autocad()
mSp = acad.model
pk_int = []
pk_float = []
mark_pipe = []
mark_earth = []
mark_pillow = []
mark_ditch = []
mark_filling = []
point_start = [0, 0, 0]
h_step = 50  # шаг строк подвала(линии)


# переменные для отклонений
deflections_ditch = random.randint(1, 9) / 100
deflections_pillow = random.randint(1, 6) / 100
deflections_pipe = random.randint(1, 4) / 100
deflections_filling = random.randint(1, 4) / 100

# обработка CSV файла
with open("1650-1700.csv") as r_file:
    file_reader = csv.reader(r_file, delimiter=";")
    for row in file_reader:
        pk_int.append(row[0])
        pk_float.append(row[1])
        mark_pipe.append(float(row[2]))
        mark_earth.append(float(row[3]))
        mark_ditch.append(float(row[2]) - 1.62)
        mark_pillow.append(float(row[2]) - 1.42)
        mark_filling.append(float(row[2]) + 0.20)

mark_ditch_fact = []
mark_pillow_fact = []
mark_pipe_fact = []
mark_filling_fact = []

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

# расчет длинны профиля (нач. ПК - конеч. ПК)
a = float(pk_int[0] + pk_float[0])
b = float(pk_int[-1] + pk_float[-1])
profile_distance = b - a
profile_distance_last = float(profile_distance + 40)

# расчет смещения для профилей
dx_pipe = profile_distance_last + 500
dx_ditch = dx_pipe
dx_pillow = dx_pipe + profile_distance_last + 500
dx_filling = dx_pillow + profile_distance_last + 500
dx_ditch_earth = (mark_earth[0] - mark_ditch[0]) * 25

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
coordinates_text_basement_pipe = [[77.17 + dx_pipe, 370.16], [61.21 + dx_pipe, 331.63],
                                  [109.57 + dx_pipe, 312.79], [41.84 + dx_pipe, 280.54],
                                  [108.31 + dx_pipe, 259.99], [33.89 + dx_pipe, 220.16],
                                  [94.81 + dx_pipe, 181.78], [47.29 + dx_pipe, 160.97],
                                  [119.41 + dx_pipe, 118.63], [116.18 + dx_pipe, 68.49],
                                  [153.10 + dx_pipe, 21.65]]
# текст для шапки профиля траншеи
text_basement_transh = ['Отметки земли, м', 'Проектные отметки', 'дна траншеи, м', 'Фактические отметки',
                        'дна траншеи, м', 'Разница в отметках, м', 'Глубина траншеи, м', 'Откос',
                        'Ширина дна траншеи', 'Тип прокладки', 'Расстояние, м', 'Пикеты, м']
coordinates_text_basement_transh = [[78.50, 418.58], [61.21, 381.63],
                                    [99.61, 362.79], [41.84, 330.54],
                                    [98.35, 309.99], [33.89, 270.16],
                                    [62.96, 221.11], [94.81, 181.78],
                                    [47.29, 160.97], [119.41, 118.63],
                                    [116.18, 69.18], [153.10, 18.74]]
# текст для шапки профиля подушки
text_basement_pillow = ['Фактические отметки', 'дна траншеи, м', 'Проектные отметки', 'верха подушки, м',
                        'Фактические отметки', 'верха подушки, м', 'Толщина слоя подушки, м', 'Откос',
                        'Ширина дна траншеи', 'Тип прокладки', 'Расстояние, м', 'Пикеты, м']
coordinates_text_basement_pillow = [[43.21 + dx_pillow, 378.69], [99.61 + dx_pillow, 359.85],
                                    [61.294 + dx_pillow, 330.54], [91.89 + dx_pillow, 309.99],
                                    [43.240 + dx_pillow, 280.54], [91.89 + dx_pillow, 259.99],
                                    [17.158 + dx_pillow, 219.802], [94.810 + dx_pillow, 181.780],
                                    [47.290 + dx_pillow, 160.970], [119.410 + dx_pillow, 118.630],
                                    [116.180 + dx_pillow, 69.180], [153.100 + dx_pillow, 18.740]]
# текст для шапки профиля обсыпки
text_basement_filling = ['Проектные отметки', 'верха обсыпки, м', 'Фактические отметки', 'верха обсыпки, м',
                         'Фактические отметки', 'верха трубы, м', 'Толщина слоя', 'над трубой, м', 'Откос',
                         'Ширина дна траншеи', 'Тип прокладки', 'Расстояние, м', 'Пикеты, м']
coordinates_text_basement_filling = [[61.42 + dx_filling, 378.99], [93.90 + dx_filling, 360.15],
                                     [43.16 + dx_filling, 330.54], [93.58 + dx_filling, 309.99],
                                     [43.16 + dx_filling, 280.54], [109.30 + dx_filling, 259.99],
                                     [125.29 + dx_filling, 230.54], [117.14 + dx_filling, 209.99],
                                     [94.81 + dx_filling, 181.78], [50.32 + dx_filling, 160.97],
                                     [119.41 + dx_filling, 118.63], [116.18 + dx_filling, 69.18],
                                     [153.10 + dx_filling, 18.7]]


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
        mSp.AddLine(APoint(264 + dx_ditch, th_2), APoint(profile_distance_last + 264 + dx_ditch, th_2))
        g += h_step
    mSp.AddLine(APoint(264 + dx_ditch, 0), APoint(264 + profile_distance_last + dx_ditch, 0))


def basement_all_ditch():
    # начальня риска в строке "Растояния"
    mSp.AddLine(APoint(304.00, 50.00), APoint(304.00, 70.00))
    # начальная отметка земли
    mSp.AddText(mark_earth[0], APoint(304.00, 404.75), 10)
    # начальная проектная отметка траншеии
    mSp.AddText(mark_ditch[0], APoint(304.00, 354.33), 10)
    # начальная фактическая отметка траншеии
    mSp.AddText(round(mark_ditch_fact[0], 2), APoint(304.00, 304.35), 10)
    # начальное отклонение
    mSp.AddText(round(mark_ditch_fact[0]-mark_ditch[0], 2), APoint(304.00, 256.83), 10)
    # начальная глубина разработки
    mSp.AddText(round(float(mark_earth[0]) - float(mark_ditch_fact[0]), 2), APoint(304.00, 209.99), 10)
    # начальный ПК в строке "Пикеты"
    pk_start = pk_int[0] + '+' + pk_float[0]
    mSp.AddText(pk_start, APoint(280.00, 32), 10)
    p = 304.00
    for i in range(len(distance_pk) - 1):
        pk_dist = round(float(distance_pk[i + 1]) - float(distance_pk[i]), 2)
        dh_x = p + pk_dist
        mSp.AddLine(APoint(dh_x, 70.00), APoint(dh_x, 50.00))
        # подпись расстояния
        otstup_text = pk_dist - (pk_dist / 2 + 5)
        mSp.AddText(format(pk_dist, '.2f'), APoint(dh_x - otstup_text, 61.30), 10)
        p += pk_dist
        # отметки верха земли
        mSp.AddText(format(float(mark_earth[i + 1]), '.2f'), APoint(dh_x, 404.75), 10)
        # проектные отметки дна траншеии
        mSp.AddText(format(float(mark_ditch[i + 1]), '.2f'), APoint(dh_x, 354.33), 10)
        # фактические отметки дна траншеи
        mSp.AddText(format(mark_ditch_fact[i + 1], '.2f'), APoint(dh_x, 304.35), 10)
        # отклонения от проекта по дну трашеи
        mSp.AddText(round(mark_ditch_fact[i + 1] - mark_ditch[i + 1], 2), APoint(dh_x, 256.83), 10)
        # глубина разработки траншеи
        development_depth = format(round(mark_earth[i + 1] - mark_ditch_fact[i + 1], 2), '.2f')
        mSp.AddText(development_depth, APoint(dh_x, 209.99), 10)
        piket = pk_int[i + 1]
        if pk_float[i + 1] == '00':
            mSp.AddLine(APoint(dh_x, 100.00), APoint(dh_x, 50.00))
            if piket[3:] == '0' or piket[3:] == '5':
                mSp.AddText(piket, APoint(dh_x - 15, 32), 10)
            else:
                mSp.AddText(piket[3:], APoint(dh_x - 3.24, 32), 10)


def basement_all_pillow():
    # начальня риска в строке "Растояния"
    mSp.AddLine(APoint(304.00 + dx_pillow, 50.00), APoint(304.00 + dx_pillow, 70.00))
    # начальная фактическая отметка дна траншеии
    coord_text_13 = APoint(304.00 + dx_pillow, 354.33)
    mSp.AddText(mark_ditch_fact[0], coord_text_13, 10)
    # начальная проектная отметка верха подушки
    coord_text_14 = APoint(304.00 + dx_pillow, 304.35)
    mSp.AddText(mark_pillow[0], coord_text_14, 10)
    # начальная фактическая отметка верха подушки
    coord_text_12 = APoint(304.00 + dx_pillow, 254.35)
    mSp.AddText(round(mark_pillow_fact[0], 2), coord_text_12, 10)
    # начальная толщина подушки
    coord_text_11 = APoint(304.00 + dx_pillow, 210.00)
    mSp.AddText(round(mark_pillow_fact[0] - mark_ditch_fact[0], 2), coord_text_11, 10)
    # начальный ПК в строке "Пикеты"
    pk_start = pk_int[0] + '+' + pk_float[0]
    t_102 = APoint(280.00 + dx_pillow, 32)
    mSp.AddText(pk_start, t_102, 10)
    p = 304.00
    for i in range(len(distance_pk) - 1):
        pk_dist = round(float(distance_pk[i + 1]) - float(distance_pk[i]), 2)
        # проставка рисок в строке "Растояния"
        dh_x = p + pk_dist
        mSp.AddLine(APoint(dh_x + dx_pillow, 70.00), APoint(dh_x + dx_pillow, 50.00))
        # подпись расстояния
        otstup_text = pk_dist - (pk_dist / 2 + 5)
        coord_text_1 = APoint(dh_x - otstup_text + dx_pillow, 61.30)
        mSp.AddText(format(pk_dist, '.2f'), coord_text_1, 10)
        p += pk_dist
        # фактическая отметка дна траншеии
        coord_text_2 = APoint(dh_x + dx_pillow, 354.33)
        mSp.AddText(format(float(mark_ditch_fact[i + 1]), '.2f'), coord_text_2, 10)
        # проектная отметка верха подушки
        coord_text_3 = APoint(dh_x + dx_pillow, 304.35)
        mSp.AddText(format(float(mark_pillow[i + 1]), '.2f'), coord_text_3, 10)
        # фактические отметки верха подушки
        coord_text_4 = APoint(dh_x + dx_pillow, 254.35)
        mSp.AddText(format(mark_pillow_fact[i + 1], '.2f'), coord_text_4, 10)
        # толщина слоя подушки
        coord_text_5 = APoint(dh_x + dx_pillow, 210.00)
        mSp.AddText(format(round(mark_pillow_fact[i + 1] - mark_ditch_fact[i + 1], 2), '.2f'), coord_text_5, 10)

        piket = pk_int[i + 1]
        if pk_float[i + 1] == '00':
            mSp.AddLine(APoint(dh_x + dx_pillow, 100.00), APoint(dh_x + dx_pillow, 50.00))
            if piket[3:] == '0' or piket[3:] == '5':
                mSp.AddText(piket, APoint(dh_x - 15 + dx_pillow, 32), 10)
            else:
                mSp.AddText(piket[3:], APoint(dh_x - 3.24 + dx_pillow, 32), 10)


def basement_all_pipe():
    # начальня риска в строке "Растояния"
    mSp.AddLine(APoint(304.00 + dx_pipe, 50.00), APoint(304.00 + dx_pipe, 70.00))
    # начальная отметка земли
    mSp.AddText(mark_earth[0], APoint(304.00 + dx_pipe, 354.33), 10)
    # начальная проектная отметка трубы
    mSp.AddText(mark_pipe[0], APoint(304.00 + dx_pipe, 304.35), 10)
    # начальная фактическая отметка трубы
    mSp.AddText(round(mark_pipe_fact[0], 2), APoint(304.00 + dx_pipe, 253.42), 10)
    # начальное отклонение (-0,03)
    mSp.AddText('-0.03', APoint(304.00 + dx_pipe, 205.35), 10)
    # начальный ПК в строке "Пикеты"
    pk_start = pk_int[0] + '+' + pk_float[0]
    mSp.AddText(pk_start, APoint(280.00 + dx_pipe, 32), 10)
    p = 304.00
    for i in range(len(distance_pk) - 1):
        pk_dist = round(float(distance_pk[i + 1]) - float(distance_pk[i]), 2)
        # проставка рисок в строке "Растояния"
        dh_x = p + pk_dist
        mSp.AddLine(APoint(dh_x + dx_pipe, 70.00), APoint(dh_x + dx_pipe, 50.00))
        # подпись расстояния
        otstup_text = pk_dist - (pk_dist / 2 + 5)
        mSp.AddText(format(pk_dist, '.2f'), APoint(dh_x - otstup_text + dx_pipe, 61.30), 10)
        p += pk_dist
        # отметки верха земли
        mSp.AddText(format(float(mark_earth[i + 1]), '.2f'), APoint(dh_x + dx_pipe, 354.33), 10)
        # проектные отметки трубы
        mSp.AddText(format(float(mark_pipe[i + 1]), '.2f'), APoint(dh_x + dx_pipe, 304.35), 10)
        # фактические отметки трубы
        mSp.AddText(format(mark_pipe_fact[i + 1], '.2f'), APoint(dh_x + dx_pipe, 253.42), 10)
        # отклонения от проекта по трубе
        mSp.AddText(round(mark_pipe_fact[i + 1] - mark_pipe[i + 1], 2), APoint(dh_x + dx_pipe, 205.35), 10)

        piket = pk_int[i + 1]
        if pk_float[i + 1] == '00':
            mSp.AddLine(APoint(dh_x + dx_pipe, 100.00), APoint(dh_x + dx_pipe, 50.00))
            if piket[3:] == '0' or piket[3:] == '5':
                mSp.AddText(piket, APoint(dh_x - 15 + dx_pipe, 32), 10)
            else:
                mSp.AddText(piket[3:], APoint(dh_x - 3.24 + dx_pipe, 32), 10)


def basement_all_filling():
    # начальня риска в строке "Растояния"
    mSp.AddLine(APoint(304.00 + dx_filling, 50.00), APoint(304.00 + dx_filling, 70.00))
    # начальная проектная отметка верха обсыпки
    mSp.AddText(mark_filling[0], APoint(304.00 + dx_filling, 354.33), 10)
    # начальная фактическая отметка верха обсыпки
    mSp.AddText(mark_filling_fact[0], APoint(304.00 + dx_filling, 303.86), 10)
    # начальная фактическая отметка верха трубы
    mSp.AddText(round(mark_pipe_fact[0], 2), APoint(304.00 + dx_filling, 253.88), 10)
    # начальная толщина обсыпки
    mSp.AddText(round(mark_filling_fact[0] - mark_pipe_fact[0], 2), APoint(304.00 + dx_filling, 210.80), 10)
    # начальный ПК в строке "Пикеты"
    pk_start = pk_int[0] + '+' + pk_float[0]
    mSp.AddText(pk_start, APoint(280.00 + dx_filling, 32), 10)
    p = 304.00
    for i in range(len(distance_pk) - 1):
        pk_dist = round(float(distance_pk[i + 1]) - float(distance_pk[i]), 2)
        # проставка рисок в строке "Растояния"
        dh_x = p + pk_dist
        mSp.AddLine(APoint(dh_x + dx_filling, 70.00), APoint(dh_x + dx_filling, 50.00))
        # подпись расстояния
        otstup_text = pk_dist - (pk_dist / 2 + 5)
        mSp.AddText(format(pk_dist, '.2f'), APoint(dh_x - otstup_text + dx_filling, 61.30), 10)
        p += pk_dist
        # проектная отметка верха обсыпки
        mSp.AddText(format(float(mark_filling[i + 1]), '.2f'), APoint(dh_x + dx_filling, 354.33), 10)
        # фактическая отметка верха обсыпки
        mSp.AddText(format(float(mark_filling_fact[i + 1]), '.2f'), APoint(dh_x + dx_filling, 303.86), 10)
        # фактические отметки верха трубы
        mSp.AddText(format(mark_pipe_fact[i + 1], '.2f'), APoint(dh_x + dx_filling, 253.88), 10)
        # толщина слоя обсыпки
        mSp.AddText(format(round(mark_filling_fact[i + 1] - mark_pipe_fact[i + 1], 2), '.2f'),
                    APoint(dh_x + dx_filling, 210.80), 10)

        piket = pk_int[i + 1]
        if pk_float[i + 1] == '00':
            mSp.AddLine(APoint(dh_x + dx_filling, 100.00), APoint(dh_x + dx_filling, 50.00))
            if piket[3:] == '0' or piket[3:] == '5':
                mSp.AddText(piket, APoint(dh_x - 15 + dx_filling, 32), 10)
            else:
                mSp.AddText(piket[3:], APoint(dh_x - 3.24 + dx_filling, 32), 10)


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
        x_2 = x_1 + (float(distance_pk[lp + 1]) - float(distance_pk[lp]))
        y_2 = y_1 + ((list_1[lp + 1] - list_1[lp]) * 25)
        mSp.AddLine(APoint(x_1, y_1), APoint(x_2, y_2))
        mSp.AddLine(APoint(x_1, g), APoint(x_1, y_1))
        x_1 = x_2
        y_1 = y_2
    mSp.AddLine(APoint(x_1, g), APoint(x_1, y_1, ))

    x_1 = 264 + 40 + dx
    y_1 = g + (list_1[0] - min_mark) * 25 + 25 + dx_transh_earth
    for lp in range(len(list_2) - 1):
        x_2 = x_1 + (float(distance_pk[lp + 1]) - float(distance_pk[lp]))
        y_2 = y_1 + ((list_2[lp + 1] - list_2[lp]) * 25)
        mSp.AddLine(APoint(x_1, y_1), APoint(x_2, y_2))
        x_1 = x_2
        y_1 = y_2


def ditch():
    # простроение подвала разработки
    line_basement(450, 264, 0)  # контур шапки подвала (разработка)
    line_basement_gorizont(h_step, 8, 0)  # горизонтальные черты в шапке подвала (разработка)
    text_basement_hat(text_basement_transh, coordinates_text_basement_transh,
                      0)  # подпись строк в шапке подвала (разработка)
    line_longitudinal(9, 0)  # продольные линии подвара (разработка)
    basement_all_ditch()  # запонение строк подвала (разработка)
    height_scale(0, 450, mark_ditch, mark_earth)  # шкала (разработка)
    profile_line(450, 0, mark_ditch, mark_earth, dx_ditch_earth)


def pillow():
    line_basement(400, 264, dx_pillow)
    line_basement_gorizont(h_step, 7, dx_pillow)
    text_basement_hat(text_basement_pillow, coordinates_text_basement_pillow, dx_pillow)
    line_longitudinal(8, dx_pillow)
    basement_all_pillow()
    height_scale(dx_pillow, 400, mark_ditch, mark_pillow)
    dx_pillow_ditch = (mark_pillow_fact[0] - mark_ditch_fact[0]) * 25
    profile_line(400, dx_pillow, mark_ditch, mark_pillow, dx_pillow_ditch)


def pipe():
    # простроение подвала укладки
    line_basement(400, 264, dx_pipe)  # контур шапки подвала (укладка)
    line_basement_gorizont(h_step, 7, dx_pipe)  # горизонтальные черты в шапке подвала (укладка)
    text_basement_hat(text_basement_pipe, coordinates_text_basement_pipe,
                      dx_pipe)  # подпись строк в шапке подвала (укладка)
    line_longitudinal(8, dx_pipe)  # продольные линии подвара (укладка)
    basement_all_pipe()
    height_scale(dx_pipe, 400, mark_pipe, mark_earth)  # шкала (разработка)
    dx_pipe_earth = (mark_earth[0] - mark_pipe[0]) * 25
    profile_line(400, dx_pipe, mark_pipe, mark_earth, dx_pipe_earth)


def filling():
    line_basement(400, 264, dx_filling)
    line_basement_gorizont(h_step, 7, dx_filling)
    text_basement_hat(text_basement_filling, coordinates_text_basement_filling, dx_filling)
    line_longitudinal(8, dx_filling)
    basement_all_filling()
    height_scale(dx_filling, 400, mark_pipe, mark_filling)
    dx_filling_pipe = (mark_filling[0] - mark_pipe[0]) * 25
    profile_line(400, dx_filling, mark_pipe, mark_filling, dx_filling_pipe)


ditch()
pillow()
pipe()
filling()
