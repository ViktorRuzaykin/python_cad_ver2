import json


def read_parameters():
    with open('parameters.json', 'r') as outfile:
        data = json.load(outfile)
        return data


param = read_parameters()
print(param)
SCALE_WIDTH = 1 / 7  # соотношение ширины шкалы, ширина к высоте
CONDITIONAL_HORIZON = 5  # значение для определения условного горизонта
OFFSET_TEXT_SCALE = 4  # отступ текста от шкалы профиля
ROTATION_ANGLE_90 = 1.57079632679  # угол 90 градусов в радианах
OFFSET_TEXT_LINE = -1.1  # отступ текста от линии в подвале
OFFSET_PROFILE = 8.5  # отступ основного профиля от шапки подвала
HEIGHT_TEXT = 4
OFFSET_NEW_PROFILE = 40
WIDTH_BASEMENT = 85.4
VARIATION_DITCH = (-5, 5)  # допуск для траншеи
VARIATION_PILLOW = (-5, 5)  # допуск для подушки
VARIATION_PIPE = (-15, 15)  # допуск для трубы
VARIATION_FILLING = (1, 5)  # допуск для присыпки
HEIGHT_PILLOW = 0.10  # высота подушки
DIAMETER_PIPE = 0.110  # диаметр трубы
HEIGHT_FILLING = 0.30  # высота присыпки
TOP_PIPE = False
NAME_COLUMN = ('пк', 'плюс', 'H трубы', 'Н земли', 'Н транш', 'Н ф.транш', 'Н подуш', 'Н ф.подуш', 'Н ф.трубы',
               'Н обсып', 'Н ф.обсып')

PATH_FILE = {
    'ditch': 'ditch.txt',
    'pillow': 'pillow.txt',
    'pipe': 'pipe.txt',
    'filling': 'filling.txt',
}

STEP_HORIZONTAL_DITCH = [14, 14, 20, 20, 20, 28, 20]  # шаг горизонтальных линий подвала разработки
_step_hor = [14, 20, 20, 28, 20]
STEP_HORIZONTAL_PILLOW = _step_hor  # шаг горизонтальных линий подвала подушки
STEP_HORIZONTAL_PIPE = _step_hor  # шаг горизонтальных линий подвала укладки
STEP_HORIZONTAL_FILLING = _step_hor  # шаг горизонтальных линий подвала обсыпки

DECIMAL_PLACES = 3

LEVEL_DITCH_PROJECT = 126.00
LEVEL_DITCH_PK = 102.00
LEVEL_DITCH_ACTUAL = 58.00
LEVEL_DITCH_EARTH = 38.00
LEVEL_DITCH_DIFF = 20.00
LEVEL_DITCH_DEPTH = 7.00

L1 = 92.00
L2 = 68.00
L3 = 24.00
L4 = 7.00
LEVEL_PILLOW_PROJECT, LEVEL_PIPE_PROJECT, LEVEL_FILLING_PROJECT = L1, L1, L1
LEVEL_PILLOW_PK, LEVEL_PIPE_PK, LEVEL_FILLING_PK = L2, L2, L2
LEVEL_PILLOW_ACTUAL, LEVEL_PIPE_ACTUAL, LEVEL_FILLING_ACTUAL = L3, L3, L3
LEVEL_PILLOW_DIFF, LEVEL_PIPE_DIFF, LEVEL_FILLING_DIFF = L4, L4, L4

KEY_TYPE = {
    'ditch': '"Траншея"',
    'pillow': '"Подушка"',
    'pipe': '"Укладка"',
    'filling': '"Обсыпка"'
}

DIFFERENCE_TYPE = {
    'м': 1,
    'см': 100,
    'мм': 1000,
}



