parameters = {}



SCALE_WIDTH = 1 / 7  # соотношение ширины шкалы, ширина к высоте
CONDITIONAL_HORIZON = 5  # значение для определения условного горизонта
OFFSET_TEXT_SCALE = 4  # отступ текста от шкалы профиля
ROTATION_ANGLE_90 = 1.57079632679  # угол 90 градусов в радианах
OFFSET_TEXT_LINE = -1.1  # отступ текста от линии в подвале
OFFSET_PROFILE = 8.5  # отступ основного профиля от шапки подвала
OFFSET_NEW_PROFILE = 40
WIDTH_BASEMENT = 100
VARIATION_DITCH = (-5, 5)  # допуск для траншеи
VARIATION_PILLOW = (-5, 5)  # допуск для подушки
VARIATION_PIPE = (-30, 30)  # допуск для трубы
VARIATION_FILLING = (1, 5)  # допуск для присыпки
HEIGHT_PILLOW = 0.20  # высота подушки
DIAMETER_PIPE = 0.325  # диаметр трубы
HEIGHT_FILLING = 0.30  # высота присыпки
TOP_PIPE = False
NAME_COLUMN = ('пк', 'плюс', 'H трубы', 'Н земли', 'Н транш', 'Н ф.транш', 'Н подуш', 'Н ф.подуш', 'Н ф.трубы',
               'Н обсып', 'Н ф.обсып')

PATH_FILE = {
    'ditch': 'траншея.txt',
    'pillow': 'подушка.txt',
    'pipe': 'труба.txt',
    'filling': 'обсыпка.txt',
}
PATH_FILE_DITCH = 'траншея.txt'
PATH_FILE_PILLOW = 'подушка.txt'
PATH_FILE_PIPE = 'труба.txt'
PATH_FILE_FILLING = 'обсыпка.txt'

STEP_HORIZONTAL_DITCH = [12, 17, 17, 17, 12, 22, 17]  # шаг горизонтальных линий подвала разработки
_step_hor = [12, 17, 17, 12, 22, 17]
STEP_HORIZONTAL_PILLOW = _step_hor  # шаг горизонтальных линий подвала подушки
STEP_HORIZONTAL_PIPE = _step_hor  # шаг горизонтальных линий подвала укладки
STEP_HORIZONTAL_FILLING = _step_hor  # шаг горизонтальных линий подвала обсыпки

DECIMAL_PLACES = 3

LEVEL_DITCH_PROJECT = 105.5
LEVEL_DITCH_PK = 86.00
LEVEL_DITCH_ACTUAL = 54.50
LEVEL_DITCH_EARTH = 37.50
LEVEL_DITCH_DEPTH = 20.50

L1 = 88.50
L2 = 69.00
L3 = 37.50
L4 = 20.50
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



