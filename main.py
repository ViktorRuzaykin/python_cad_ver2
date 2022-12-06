import time
import pythoncom
import parameters
import utility
from arryautocad import acad, acadModel, acadDoc, APoint
from profile import ProfileCad

pk_int = ['0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '2', '2', '2', '2']
pk_float = ['00', '16.47', '35.97', '56.47', '75.97', '95.97', '00', '20', '40', '60', '80', '00', '19.22', '39.22',
            '59.22']
distance = ['000', '016.47', '035.97', '056.47', '075.97', '095.97', '100', '120', '140', '160', '180', '200', '219.22',
            '239.22', '259.22']

mark_1 = [909.95, 910.31, 911.66, 913.40, 915.05, 916.75, 918.42, 920.05, 921.68, 923.32, 924.95, 926.64, 928.04,
          929.51, 930.97]

mark_2 = [913.95, 915.31, 916.66, 918.40, 917.05, 919.75, 922.42, 924.05, 925.68, 927.32, 929.95, 928.64, 932.04,
          933.51, 936.20]

step_horizontal_type_1 = [12, 17, 17, 17, 12, 22, 17]  # шаг горизонтальных линий подвала разработки
scale_vertical = 1000 / 200
scale_horizontal = 1000 / 1000


class CreateProfile:
    def __init__(self):
        self.acad = acad
        self.mSp = acadModel
        self.acadDoc = acadDoc
        self.profile = ProfileCad(self.mSp, self.acad, self.acadDoc)

    def test(self):
        try:
            time.sleep(1.2)

            insertion_point = self.acadDoc.Utility.GetPoint(APoint(0, 0),
                                                            'Укажите точку вставки профиля: ')  # координата вставки профиля (правиый нижний угол подвала)
            self.profile.create_header(insertion_point, parameters.PATH_FILE_DITCH)  # чертим шапку подвала
            axis_distance_x = utility.transform_to_difference(distance)  # получаем расстояние между точками по оси X
            # чертим линию профиля
            conditional_horizon = utility.conditional_horizon(mark_1, mark_2)
            insertion_point_line_1 = [insertion_point[0] + parameters.OFFSET_PROFILE, insertion_point[1] + 114,
                                      insertion_point[2]]

            self.profile.create_line_profile(insertion_point=insertion_point_line_1,
                                             difference=axis_distance_x,
                                             mark=mark_1,
                                             scale_vertical=scale_vertical,
                                             scale_horizontal=scale_horizontal,
                                             line_type='CONTI',
                                             conditional_horizon=conditional_horizon,
                                             vertical_line=True)

            insertion_point_line_2 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                      insertion_point[1] + 114,
                                      insertion_point[2]]
            self.profile.create_line_profile(insertion_point=insertion_point_line_2,
                                             difference=axis_distance_x,
                                             mark=mark_2,
                                             scale_vertical=scale_vertical,
                                             scale_horizontal=scale_horizontal,
                                             line_type='DASHED',
                                             conditional_horizon=conditional_horizon,
                                             vertical_line=False)

            # проставляем отметки
            insertion_point_mark = [insertion_point[0] + parameters.OFFSET_PROFILE, insertion_point[1] + 105.50,
                                    insertion_point[2]]
            self.profile.iter_text_cad(object_cad=mark_1,
                                       difference=axis_distance_x,
                                       point_start=insertion_point_mark,
                                       height_text=4,
                                       scale_horizontal=scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)

            insertion_point_mark_2 = [insertion_point[0] + parameters.OFFSET_PROFILE, insertion_point[1] + 55.50,
                                      insertion_point[2]]
            self.profile.iter_text_cad(object_cad=mark_2,
                                       difference=axis_distance_x,
                                       point_start=insertion_point_mark_2,
                                       height_text=4,
                                       scale_horizontal=scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)
            # проставляем пикеты
            insertion_point_pk = [insertion_point[0] + parameters.OFFSET_PROFILE, insertion_point[1] + 86,
                                  insertion_point[2]]
            picketing_type_one = utility.transform_pk_type_one(pk_int, pk_float)
            self.profile.iter_text_cad(object_cad=picketing_type_one,
                                       difference=axis_distance_x,
                                       point_start=insertion_point_pk,
                                       height_text=4,
                                       scale_horizontal=scale_horizontal,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE,
                                       alignment=1)
            # чертим горизонтальные и вертикальные лини в подвале профиля
            dd = float(distance[-1]) - float(distance[0])
            self.profile.create_horizontal_line(insertion_point, dd, parameters.OFFSET_PROFILE, step_horizontal_type_1,
                                                scale_horizontal)
            self.profile.create_vertical_line(insertion_point, axis_distance_x, step_horizontal_type_1)
            # чертим шкалу профиля
            insertion_point_scale = [insertion_point[0], insertion_point[1] + 114, insertion_point[2]]
            height_scale = utility.height_scale(mark_1, mark_2)

            self.profile.create_scale(insertion_point=insertion_point_scale,
                                      height_scale=height_scale,
                                      height_text=4,
                                      scale_vertical=scale_vertical,
                                      conditional_horizon=conditional_horizon,
                                      text_styles='СПДС')
            self.acadDoc.Utility.Prompt(u'Готово.\n')
        except pythoncom.com_error as f:
            print(f)
            print('errrrrror')
            self.test()


p = Profile()
p.test()
