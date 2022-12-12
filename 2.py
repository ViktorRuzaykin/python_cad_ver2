import json
import time

data = {
    'scale_width': 1 / 7,
    'conditional_horizon': 5,
    'offset_text_scale': 4,
    'rotation_angle_90': 1.57079632679,
    'offset_text_line': -1.1,
    'offset_profile': 8.5,
    'height_text': 4,
    'offset_new_profile': 40,
    'width_basement': 85.4,
    'variation_ditch': (-5, 5),
    'variation_pillow ': (-5, 5),
    'variation_pipe': (-15, 15),
    'variation_filling': (1, 5),
    'height_pillow': 0.10,
    'diameter_pipe': 0.110,
    'height_filling': 0.30,
    'top_pipe': False,
    'path_file': {
        'ditch': 'ditch.txt',
        'pillow': 'pillow.txt',
        'pipe': 'pipe.txt',
        'filling': 'filling.txt',
    },
    'step_horizontal_ditch': [14, 14, 20, 20, 20, 28, 20],
    '_step_hor': [14, 20, 20, 28, 20],
    'decimal_places': 3,
    'level_ditch_project': 126.00,
    'level_ditch_pk': 102.00,
    'level_ditch_actual': 58.00,
    'level_ditch_earth': 38.00,
    'level_ditch_diff': 20.00,
    'level_ditch_depth': 7.00,
    'level_project': 92.00,
    'level_pk': 68,
    'level_actual': 24,
    'level_diff': 7,
    'key_type': {
        'ditch': '"траншея"',
        'pillow': '"подушка"',
        'pipe': '"укладка"',
        'filling': '"обсыпка"'
    },
    'difference_type': {
        'м': 1,
        'см': 100,
        'мм': 1000,
    },

}


with open('param_test.json', 'w') as infile:
    json.dump(data, infile, indent=4)

time.sleep(1)
with open('param_test.json', 'r') as outfile:
    data = json.load(outfile)
    print(data)
