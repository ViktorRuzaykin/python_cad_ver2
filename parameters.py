import json


def read_parameters():
    with open('parameters.json', 'r') as outfile:
        data = json.load(outfile)
        return data


param = read_parameters()

SCALE_WIDTH = param['scale_width']  # соотношение ширины шкалы, ширина к высоте
CONDITIONAL_HORIZON = param['conditional_horizon']  # значение для определения условного горизонта
OFFSET_TEXT_SCALE = param['offset_text_scale']  # отступ текста от шкалы профиля
ROTATION_ANGLE_90 = param['rotation_angle_90']  # угол 90 градусов в радианах
OFFSET_TEXT_LINE = param['offset_text_line']  # отступ текста от линии в подвале
OFFSET_PROFILE = param['offset_profile']  # отступ основного профиля от шапки подвала
HEIGHT_TEXT = param['height_text']
OFFSET_NEW_PROFILE = param['offset_new_profile']
WIDTH_BASEMENT = param['width_basement']
VARIATION_DITCH = param['variation_ditch']  # допуск для траншеи
VARIATION_PILLOW = param['variation_pillow']  # допуск для подушки
VARIATION_PIPE = param['variation_pipe']  # допуск для трубы
VARIATION_FILLING = param['variation_filling']  # допуск для присыпки
HEIGHT_PILLOW = param['height_pillow']  # высота подушки
DIAMETER_PIPE = param['diameter_pipe']  # диаметр трубы
HEIGHT_FILLING = param['height_filling']  # высота присыпки
TOP_PIPE = param['top_pipe']
NAME_COLUMN = ('пк', 'плюс', 'H трубы', 'Н земли', 'Н транш', 'Н ф.транш', 'Н подуш', 'Н ф.подуш', 'Н ф.трубы',
               'Н обсып', 'Н ф.обсып')

PATH_FILE = {
    'ditch': param['path_file']['ditch'],
    'pillow': param['path_file']['pillow'],
    'pipe': param['path_file']['pipe'],
    'filling': param['path_file']['filling'],
}

STEP_HORIZONTAL_DITCH = param['step_horizontal_ditch']  # шаг горизонтальных линий подвала разработки
_step_hor = param['_step_hor']
STEP_HORIZONTAL_PILLOW = _step_hor  # шаг горизонтальных линий подвала подушки
STEP_HORIZONTAL_PIPE = _step_hor  # шаг горизонтальных линий подвала укладки
STEP_HORIZONTAL_FILLING = _step_hor  # шаг горизонтальных линий подвала обсыпки

DECIMAL_PLACES = param['decimal_places']

LEVEL_DITCH_PROJECT = param['level_ditch_project']
LEVEL_DITCH_PK = param['level_ditch_pk']
LEVEL_DITCH_ACTUAL = param['level_ditch_actual']
LEVEL_DITCH_EARTH = param['level_ditch_earth']
LEVEL_DITCH_DIFF = param['level_ditch_diff']
LEVEL_DITCH_DEPTH = param['level_ditch_depth']

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
