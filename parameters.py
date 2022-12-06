SCALE_WIDTH = 1 / 5  # соотношение ширины шкалы, ширина к высоте
CONDITIONAL_HORIZON = 5  # значение для определения условного горизонта
OFFSET_TEXT_SCALE = 4  # отступ текста от шкалы профиля
ROTATION_ANGLE_90 = 1.57079632679  # угол 90 градусов в радианах
OFFSET_TEXT_LINE = -1.4  # отступ текста от линии в подвале
OFFSET_PROFILE = 8.5  # отступ основного профиля от шапки подвала
OFFSET_NEW_PROFILE = 40
WIDTH_BASEMENT = 100
VARIATION_DITCH = (-5, 5)  # допуск для траншеи
VARIATION_PILLOW = (-5, 5)  # допуск для подушки
VARIATION_PIPE = (-3, 3)  # допуск для трубы
VARIATION_FILLING = (1, 5)  # допуск для присыпки
HEIGHT_PILLOW = 0.20  # высота подушки
DIAMETER_PIPE = 0.325  # диаметр трубы
HEIGHT_FILLING = 0.30  # высота присыпки
NAME_COLUMN = ('пк', 'плюс', 'H трубы', 'Н земли', 'Н транш', 'Н ф.транш', 'Н подуш', 'Н ф.подуш', 'Н ф.трубы',
               'Н обсып', 'Н ф.обсып')

PATH_FILE_DITCH = 'траншея.txt'
PATH_FILE_PILLOW = 'подушка.txt'
PATH_FILE_PIPE = 'труба.txt'
PATH_FILE_FILLING = 'обсыпка.txt'

STEP_HORIZONTAL_DITCH = [12, 17, 17, 17, 12, 22, 17]  # шаг горизонтальных линий подвала разработки
STEP_HORIZONTAL_PILLOW = [12, 17, 17, 12, 22, 17]  # шаг горизонтальных линий подвала разработки
DECIMAL_PLACES = 3
