import time

import pythoncom

import parameters
import utility
from arryautocad import acad, acadModel, acadDoc
from calculations import Calculations
from profile import ProfileCad

final_data_file = None


def open_work_file():
    global final_data_file
    final_data_file = Calculations.reader_final_file('ПК0+0.00 - ПК5+0.00_final.csv')


class CreateProfile:
    def __init__(self, data_final, start_profile, end_profile, scale_vertical, scale_horizontal):
        self.acad = acad
        self.mSp = acadModel
        self.acadDoc = acadDoc
        self.profile = ProfileCad(self.mSp, self.acad, self.acadDoc)
        self.calculations = Calculations
        self.scale_vertical = 1000 / scale_vertical
        self.scale_horizontal = 1000 / scale_horizontal
        self.start_profile = start_profile  # [0, 20]
        self.end_profile = end_profile  # [2, 32]
        self.data_final = data_final

        if data_final is not None:
            # расстояния между точками

            self.distance_pk = utility.transform_pk_to_distance(self.data_final['pk_int'],
                                                                self.data_final['pk_float'])

            # определяем позицию первого ПК
            self.position_picketing_one = self.calculations.search_position_picketing(self.start_profile,
                                                                                      self.distance_pk)
            # определяем позицию второго ПК
            self.position_picketing_second = self.calculations.search_position_picketing(self.end_profile,
                                                                                         self.distance_pk)

            self.new_distance_pk = self.calculations.create_new_list_distance(self.position_picketing_one,
                                                                              self.position_picketing_second,
                                                                              self.distance_pk, self.start_profile,
                                                                              self.end_profile)

            self.axis_distance_x = utility.transform_to_difference(self.new_distance_pk)
            self.new_pk_int, self.new_pk_float = self.calculations.create_new_list_picketing(
                self.position_picketing_one,
                self.position_picketing_second,
                self.data_final['pk_int'],
                self.data_final['pk_float'],
                self.start_profile, self.end_profile)
            self.list_picketing = utility.transform_pk_type_one(self.new_pk_int, self.new_pk_float)

    def _data_for_profile_ditch(self):
        # получаем новый список отметок по траншеи проект
        mark_one_project_ditch = self.calculations.interpolation_mark(self.position_picketing_one,
                                                                      self.data_final['project_ditch'])
        mark_second_project_ditch = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                         self.data_final['project_ditch'])

        new_marks_project_ditch = self.calculations.create_new_list_data(self.position_picketing_one,
                                                                         self.position_picketing_second,
                                                                         mark_one_project_ditch,
                                                                         mark_second_project_ditch,
                                                                         self.data_final['project_ditch'])

        # получаем новый список отметок по траншеи факт
        mark_one_actual_ditch = self.calculations.interpolation_mark(self.position_picketing_one,
                                                                     self.data_final['actual_ditch'])
        mark_second_actua_ditch = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                       self.data_final['actual_ditch'])

        new_marks_actual_ditch = self.calculations.create_new_list_data(self.position_picketing_one,
                                                                        self.position_picketing_second,
                                                                        mark_one_actual_ditch,
                                                                        mark_second_actua_ditch,
                                                                        self.data_final['actual_ditch'])
        # получаем новый список отметок по земле
        mark_one_earth = self.calculations.interpolation_mark(self.position_picketing_one,
                                                              self.data_final['mark_earth'])
        mark_second_earth = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                 self.data_final['mark_earth'])

        new_marks_actual_earth = self.calculations.create_new_list_data(self.position_picketing_one,
                                                                        self.position_picketing_second,
                                                                        mark_one_earth,
                                                                        mark_second_earth,
                                                                        self.data_final['mark_earth'])
        # получаем список глубин траншеи
        list_depth = self.calculations.depth_ditch(new_marks_actual_ditch, new_marks_actual_earth)
        data_ditch = {'new_marks_project_ditch': new_marks_project_ditch,
                      'new_marks_actual_ditch': new_marks_actual_ditch,
                      'new_marks_actual_earth': new_marks_actual_earth,
                      'list_depth': list_depth,
                      }
        return data_ditch

    def profile_ditch(self, insertion_point):
        data_for_ditch = self._data_for_profile_ditch()
        try:
            time.sleep(0.1)
            self.profile.create_header(insertion_point, parameters.PATH_FILE_DITCH)  # чертим шапку подвала
            # чертим линию профиля
            conditional_horizon = utility.conditional_horizon(data_for_ditch['new_marks_project_ditch'],
                                                              data_for_ditch['new_marks_actual_earth'])
            insertion_point_line_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                      insertion_point[1] + 114,
                                      insertion_point[2]]

            self.profile.create_line_profile(insertion_point=insertion_point_line_1,
                                             difference=self.axis_distance_x,
                                             mark=data_for_ditch['new_marks_project_ditch'],
                                             scale_vertical=self.scale_vertical,
                                             scale_horizontal=self.scale_horizontal,
                                             line_type='CONTI',
                                             conditional_horizon=conditional_horizon,
                                             vertical_line=False)

            insertion_point_line_2 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                      insertion_point[1] + 114,
                                      insertion_point[2]]
            self.profile.create_line_profile(insertion_point=insertion_point_line_2,
                                             difference=self.axis_distance_x,
                                             mark=data_for_ditch['new_marks_actual_earth'],
                                             scale_vertical=self.scale_vertical,
                                             scale_horizontal=self.scale_horizontal,
                                             line_type='CONTI',
                                             conditional_horizon=conditional_horizon,
                                             vertical_line=True)

            self.profile.create_line_profile(insertion_point=insertion_point_line_2,
                                             difference=self.axis_distance_x,
                                             mark=data_for_ditch['new_marks_actual_ditch'],
                                             scale_vertical=self.scale_vertical,
                                             scale_horizontal=self.scale_horizontal,
                                             line_type='DASHED',
                                             conditional_horizon=conditional_horizon,
                                             vertical_line=False)

            # проставляем проектные отметки траншеи
            insertion_point_mark_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                      insertion_point[1] + 105.50,
                                      insertion_point[2]]
            self.profile.iter_text_cad(object_cad=data_for_ditch['new_marks_project_ditch'],
                                       difference=self.axis_distance_x,
                                       point_start=insertion_point_mark_1,
                                       height_text=4,
                                       scale_horizontal=self.scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)

            # проставляем пикетаж
            insertion_point_picketing = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                         insertion_point[1] + 86.00,
                                         insertion_point[2]]
            self.profile.iter_text_cad(object_cad=self.list_picketing,
                                       difference=self.axis_distance_x,
                                       point_start=insertion_point_picketing,
                                       height_text=4,
                                       scale_horizontal=self.scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)

            # проставляем фактические отметки траншеи
            insertion_point_ditch_actual = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                            insertion_point[1] + 54.50,
                                            insertion_point[2]]
            self.profile.iter_text_cad(object_cad=data_for_ditch['new_marks_actual_ditch'],
                                       difference=self.axis_distance_x,
                                       point_start=insertion_point_ditch_actual,
                                       height_text=4,
                                       scale_horizontal=self.scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)

            # проставляем отметки земли
            insertion_point_earth = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                     insertion_point[1] + 37.50,
                                     insertion_point[2]]
            self.profile.iter_text_cad(object_cad=data_for_ditch['new_marks_actual_earth'],
                                       difference=self.axis_distance_x,
                                       point_start=insertion_point_earth,
                                       height_text=4,
                                       scale_horizontal=self.scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)

            # проставляем глубину разработки
            insertion_point_depth = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                     insertion_point[1] + 20.50,
                                     insertion_point[2]]
            self.profile.iter_text_cad(object_cad=data_for_ditch['list_depth'],
                                       difference=self.axis_distance_x,
                                       point_start=insertion_point_depth,
                                       height_text=4,
                                       scale_horizontal=self.scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)

            # чертим горизонтальные и вертикальные лини в подвале профиля
            dd = self.end_profile - self.start_profile
            self.profile.create_horizontal_line(insertion_point, dd, parameters.OFFSET_PROFILE,
                                                parameters.STEP_HORIZONTAL_DITCH,
                                                self.scale_horizontal)
            self.profile.create_vertical_line(insertion_point, self.axis_distance_x, parameters.STEP_HORIZONTAL_DITCH)
            # чертим шкалу профиля
            insertion_point_scale = [insertion_point[0], insertion_point[1] + 114, insertion_point[2]]
            height_scale = utility.height_scale(data_for_ditch['new_marks_project_ditch'],
                                                data_for_ditch['new_marks_actual_earth'])

            self.profile.create_scale(insertion_point=insertion_point_scale,
                                      height_scale=height_scale,
                                      height_text=4,
                                      scale_vertical=self.scale_vertical,
                                      conditional_horizon=conditional_horizon,
                                      text_styles='СПДС')
            self.acadDoc.Utility.Prompt(u'Готово.\n')
        except pythoncom.com_error as f:
            print(f)
            print('error ditch')
            self.profile_ditch(insertion_point)

    def _data_for_profile_pillow(self):
        # получаем новый список отметок по подушке проект
        mark_one_project_pillow = self.calculations.interpolation_mark(self.position_picketing_one,
                                                                       self.data_final['project_pillow'])
        mark_second_project_pillow = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                          self.data_final['project_pillow'])

        new_marks_project_pillow = self.calculations.create_new_list_data(self.position_picketing_one,
                                                                          self.position_picketing_second,
                                                                          mark_one_project_pillow,
                                                                          mark_second_project_pillow,
                                                                          self.data_final['project_pillow'])

        # получаем новый список отметок по подушке факт
        mark_one_actual_pillow = self.calculations.interpolation_mark(self.position_picketing_one,
                                                                      self.data_final['actual_pillow'])
        mark_second_actual_pillow = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                         self.data_final['actual_pillow'])

        new_marks_actual_pillow = self.calculations.create_new_list_data(self.position_picketing_one,
                                                                         self.position_picketing_second,
                                                                         mark_one_actual_pillow,
                                                                         mark_second_actual_pillow,
                                                                         self.data_final['actual_pillow'])

        data_pillow = {
            'new_marks_project_pillow': new_marks_project_pillow,
            'new_marks_actual_pillow': new_marks_actual_pillow,
        }
        return data_pillow

    def profile_pillow(self, insertion_point):
        data_for_pillow = self._data_for_profile_pillow()
        try:
            conditional_horizon = utility.conditional_horizon(data_for_pillow['new_marks_project_pillow'],
                                                              data_for_pillow['new_marks_actual_pillow'])
            insertion_point_line = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                    insertion_point[1] + 97,
                                    insertion_point[2]]
            # проектная линия профиля подушки
            self.profile.create_line_profile(insertion_point=insertion_point_line,
                                             difference=self.axis_distance_x,
                                             mark=data_for_pillow['new_marks_project_pillow'],
                                             scale_vertical=self.scale_vertical,
                                             scale_horizontal=self.scale_horizontal,
                                             line_type='CONTI',
                                             conditional_horizon=conditional_horizon,
                                             vertical_line=True)
            # фактическая линия профиля подушки
            self.profile.create_line_profile(insertion_point=insertion_point_line,
                                             difference=self.axis_distance_x,
                                             mark=data_for_pillow['new_marks_actual_pillow'],
                                             scale_vertical=self.scale_vertical,
                                             scale_horizontal=self.scale_horizontal,
                                             line_type='DASHED',
                                             conditional_horizon=conditional_horizon,
                                             vertical_line=False)

            # проставляем проектные отметки подушки
            insertion_point_mark_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                      insertion_point[1] + 88.50,
                                      insertion_point[2]]
            self.profile.iter_text_cad(object_cad=data_for_pillow['new_marks_project_pillow'],
                                       difference=self.axis_distance_x,
                                       point_start=insertion_point_mark_1,
                                       height_text=4,
                                       scale_horizontal=self.scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)

            # проставляем пикетаж
            insertion_point_picketing = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                         insertion_point[1] + 69.00,
                                         insertion_point[2]]
            self.profile.iter_text_cad(object_cad=self.list_picketing,
                                       difference=self.axis_distance_x,
                                       point_start=insertion_point_picketing,
                                       height_text=4,
                                       scale_horizontal=self.scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)
            # проставляем фактические отметки подушки
            insertion_point_ditch_actual = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                            insertion_point[1] + 54.50,
                                            insertion_point[2]]
            self.profile.iter_text_cad(object_cad=data_for_pillow['new_marks_actual_pillow'],
                                       difference=self.axis_distance_x,
                                       point_start=insertion_point_ditch_actual,
                                       height_text=4,
                                       scale_horizontal=self.scale_horizontal,
                                       alignment=1,
                                       text_styles='СПДС',
                                       dx=parameters.OFFSET_TEXT_LINE)

        except pythoncom.com_error as f:
            print(f)
            print('error pillow')
            self.profile_pillow(insertion_point)


"""scale_vertical = 200
scale_horizontal = 1000
s_profile = 105
e_profile = 305
open_work_file()
new_prifile = CreateProfile(data_final=final_data_file,
                            start_profile=s_profile,
                            end_profile=e_profile,
                            scale_vertical=scale_vertical,
                            scale_horizontal=scale_horizontal)
new_prifile.profile_ditch()"""
