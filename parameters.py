import json
from tkinter import messagebox as mb


def read_parameters():
    try:
        with open('parameters.json', 'r', encoding='utf-8') as outfile:
            data = json.load(outfile)
            return data
    except json.decoder.JSONDecodeError as f:
        mb.showerror('Ошибка!', f'Файл "parameters.json" не читается. Не пользуйтесь приложением.\n'
                                f'{f}')
        return None
    except FileNotFoundError as d:
        mb.showerror('Ошибка!', f'Файл "parameters.json" отсутствует. Не пользуйтесь приложением.\n'
                                f'{d}')
        return None


param = read_parameters()
if param is not None:
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

    LEVEL_PIPE_PROJECT = param['level_pipe_project'],
    LEVEL_PIPE_ACTUAL = param['level_pipe_actual'],
    LEVEL_PIPE_DIFF = param['level_pipe_diff'],
    LEVEL_PIPE_DISTANCE = param['level_pipe_distance'],
    LEVEL_PIPE_PK = param['level_pipe_pk'],

    LEVEL_ACTUAL_1 = param['level_actual_1'],
    LEVEL_PROJECT = param['level_project'],
    LEVEL_ACTUAL = param['level_actual'],
    LEVEL_DIFF = param['level_diff'],
    LEVEL_DISTANCE = param['level_distance'],
    LEVEL_PK = param['level_pk'],

    KEY_TYPE = {
        'ditch': param['key_type']['ditch'],
        'pillow': param['key_type']['pillow'],
        'pipe': param['key_type']['pipe'],
        'filling': param['key_type']['filling']
    }

    DIFFERENCE_TYPE = {
        'м': param['difference_type']['м'],
        'см': param['difference_type']['см'],
        'мм': param['difference_type']['мм'],
    }
