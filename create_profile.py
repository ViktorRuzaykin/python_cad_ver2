from tkinter import messagebox as mb

import pythoncom
# from arryautocad import Autocad
from pyacadcom import AutoCAD

import parameters
import utility
from calculations import Calculations
from profile import ProfileCad


class CreateProfile:
    def __init__(self, data_final, start_profile, end_profile, scale_vertical, scale_horizontal, text_style, scale_line):
        try:
            self.acad = AutoCAD()
            self.acadDoc = self.acad.ActiveDocument
            self.mSp = self.acadDoc.ModelSpace
        except pythoncom.com_error as f:
            mb.showerror(getattr(f, 'strerror'), getattr(f, 'strerror'))
        self.profile = ProfileCad(mSp=self.mSp, acadDoc=self.acadDoc)
        self.calculations = Calculations
        self.scale_vertical = 1000 / scale_vertical
        self.scale_horizontal = 1000 / scale_horizontal
        self.start_profile = start_profile  # [0, 20]
        self.end_profile = end_profile  # [2, 32]
        self.distance_profile = self.end_profile - self.start_profile
        self.data_final = data_final
        self.text_style = text_style
        self.scale_line = scale_line
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

            self.list_picketing = utility.transform_pk_type_second(self.new_pk_int, self.new_pk_float)

    def _data_for_profile_type_1(self):
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
        list_depth = self.calculations.mark_difference(new_marks_actual_ditch, new_marks_actual_earth)
        # получаем отклонений
        list_difference = self.calculations.mark_difference(new_marks_project_ditch, new_marks_actual_ditch)

        data_ditch = {'new_marks_project': new_marks_project_ditch,
                      'new_marks_actual_1': new_marks_actual_ditch,
                      'new_marks_actual_2': new_marks_actual_earth,
                      'list_depth': list_depth,
                      'list_difference': list_difference,
                      }
        return data_ditch

    def profile_type_1(self, insertion_point, key_type, difference_type):
        data_for_type_1 = self._data_for_profile_type_1()
        self.profile.create_header(insertion_point, parameters.PATH_FILE[key_type],
                                   self.text_style)  # чертим шапку подвала
        # чертим линию профиля
        conditional_horizon = utility.conditional_horizon(data_for_type_1['new_marks_project'],
                                                          data_for_type_1['new_marks_actual_2'])

        insertion_point_ditch = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                 insertion_point[1] + sum(parameters.STEP_HORIZONTAL_DITCH),
                                 insertion_point[2]]

        self.profile.create_line_profile(insertion_point=insertion_point_ditch,
                                         difference=self.axis_distance_x,
                                         mark=data_for_type_1['new_marks_project'],
                                         scale_vertical=self.scale_vertical,
                                         scale_horizontal=self.scale_horizontal,
                                         line_type='CONTI',
                                         conditional_horizon=conditional_horizon,
                                         vertical_line=True)

        self.profile.create_line_profile(insertion_point=insertion_point_ditch,
                                         difference=self.axis_distance_x,
                                         mark=data_for_type_1['new_marks_actual_2'],
                                         scale_vertical=self.scale_vertical,
                                         scale_horizontal=self.scale_horizontal,
                                         line_type='CONTI',
                                         conditional_horizon=conditional_horizon,
                                         vertical_line=False)

        # проставляем проектные отметки траншеи
        insertion_point_mark_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                  insertion_point[1] + parameters.LEVEL_DITCH_PROJECT,
                                  insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_1['new_marks_project'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_mark_1,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем пикетаж
        insertion_point_picketing = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                     insertion_point[1] + parameters.LEVEL_DITCH_PK,
                                     insertion_point[2]]
        self.profile.iter_text_cad(object_cad=self.list_picketing,
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_picketing,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=4,
                                   text_styles=self.text_style,
                                   rotation=0,
                                   decimal=0)

        # проставляем фактические отметки траншеи
        insertion_point_ditch_actual = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                        insertion_point[1] + parameters.LEVEL_DITCH_ACTUAL,
                                        insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_1['new_marks_actual_1'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_ditch_actual,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем отметки земли
        insertion_point_earth = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                 insertion_point[1] + parameters.LEVEL_DITCH_EARTH,
                                 insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_1['new_marks_actual_2'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_earth,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=parameters.OFFSET_TEXT_LINE,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем глубину разработки
        insertion_point_depth = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                 insertion_point[1] + parameters.LEVEL_DITCH_DEPTH,
                                 insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_1['list_depth'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_depth,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем отклонения
        insertion_point_depth = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                 insertion_point[1] + parameters.LEVEL_DITCH_DIFF,
                                 insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_1['list_difference'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_depth,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=parameters.OFFSET_TEXT_LINE,
                                   difference_type=difference_type,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        self.profile.create_horizontal_line(insertion_point, self.distance_profile, parameters.OFFSET_PROFILE,
                                            parameters.STEP_HORIZONTAL_DITCH,
                                            self.scale_horizontal)
        # черточки расстояний
        self.profile.distance_segments(insertion_point=insertion_point,
                                       difference=self.axis_distance_x,
                                       pk_int=self.new_pk_int,
                                       pk_float=self.new_pk_float)

        # проставляем текст 'расстояния'
        insertion_point_depth = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                 insertion_point[1] + parameters.LEVEL_DITCH_DISTANCE,
                                 insertion_point[2]]
        self.profile.iter_text_cad(object_cad=self.axis_distance_x,
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_depth,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=4,
                                   text_styles=self.text_style,
                                   difference_type=difference_type,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # чертим шкалу профиля

        if self.scale_line:
            insertion_point_scale = [insertion_point[0], insertion_point[1] + sum(parameters.STEP_HORIZONTAL_DITCH),
                                     insertion_point[2]]
            height_scale = utility.height_scale(data_for_type_1['new_marks_project'],
                                                data_for_type_1['new_marks_actual_2'])

            self.profile.create_scale(insertion_point=insertion_point_scale,
                                      height_scale=height_scale,
                                      height_text=parameters.HEIGHT_TEXT,
                                      scale_vertical=self.scale_vertical,
                                      conditional_horizon=conditional_horizon,
                                      text_styles=self.text_style)

        self.acadDoc.Utility.Prompt(f'Готово - {parameters.KEY_TYPE[key_type]}.\n')

    def _data_for_profile_type_2(self, key_type_1, key_type_2):
        # получаем новый список проектных отметок
        mark_one_project = self.calculations.interpolation_mark(self.position_picketing_one,
                                                                self.data_final[f'project_{key_type_1}'])
        mark_second_project = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                   self.data_final[f'project_{key_type_1}'])

        marks_project = self.calculations.create_new_list_data(self.position_picketing_one,
                                                               self.position_picketing_second,
                                                               mark_one_project,
                                                               mark_second_project,
                                                               self.data_final[f'project_{key_type_1}'])

        # получаем новый список фактических отметок key_type_1
        mark_one_actual_1 = self.calculations.interpolation_mark(self.position_picketing_one,
                                                                 self.data_final[f'actual_{key_type_1}'])
        mark_second_actual_1 = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                    self.data_final[f'actual_{key_type_1}'])

        marks_actual_1 = self.calculations.create_new_list_data(self.position_picketing_one,
                                                                self.position_picketing_second,
                                                                mark_one_actual_1,
                                                                mark_second_actual_1,
                                                                self.data_final[f'actual_{key_type_1}'])

        # получаем новый список фактических отметок key_type_2
        mark_one_actual_2 = self.calculations.interpolation_mark(self.position_picketing_one,
                                                                 self.data_final[f'actual_{key_type_2}'])
        mark_second_actual_2 = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                    self.data_final[f'actual_{key_type_2}'])

        marks_actual_2 = self.calculations.create_new_list_data(self.position_picketing_one,
                                                                self.position_picketing_second,
                                                                mark_one_actual_2,
                                                                mark_second_actual_2,
                                                                self.data_final[f'actual_{key_type_2}'])

        #  список отклонений
        mark_difference = self.calculations.mark_difference(marks_actual_2, marks_project)

        data_type_2 = {
            'marks_project': marks_project,
            'marks_actual_1': marks_actual_1,
            'marks_actual_2': marks_actual_2,
            'mark_difference': mark_difference,
        }
        return data_type_2

    def profile_type_2(self, insertion_point, key_type_1, key_type_2, difference_type):
        data_for_type_2 = self._data_for_profile_type_2(key_type_1=key_type_1, key_type_2=key_type_2)
        self.profile.create_header(insertion_point, parameters.PATH_FILE[key_type_1],
                                   self.text_style)  # чертим шапку подвала
        conditional_horizon = utility.conditional_horizon(data_for_type_2['marks_project'],
                                                          data_for_type_2['marks_actual_2'])

        # проектная линия профиля
        insertion_point_line = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                insertion_point[1] + sum(parameters._step_hor),
                                insertion_point[2]]
        self.profile.create_line_profile(insertion_point=insertion_point_line,
                                         difference=self.axis_distance_x,
                                         mark=data_for_type_2['marks_project'],
                                         scale_vertical=self.scale_vertical,
                                         scale_horizontal=self.scale_horizontal,
                                         line_type='CONTI',
                                         conditional_horizon=conditional_horizon,
                                         vertical_line=True)
        # фактическая линия профиля
        self.profile.create_line_profile(insertion_point=insertion_point_line,
                                         difference=self.axis_distance_x,
                                         mark=data_for_type_2['marks_actual_2'],
                                         scale_vertical=self.scale_vertical,
                                         scale_horizontal=self.scale_horizontal,
                                         line_type='CONTI',
                                         conditional_horizon=conditional_horizon,
                                         vertical_line=False)

        # проставляем проектные отметки
        insertion_point_mark_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                  insertion_point[1] + parameters.LEVEL_PROJECT,
                                  insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_2['marks_project'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_mark_1,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем пикетаж
        insertion_point_picketing = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                     insertion_point[1] + parameters.LEVEL_PK,
                                     insertion_point[2]]
        self.profile.iter_text_cad(object_cad=self.list_picketing,
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_picketing,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=4,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=0,
                                   decimal=0)

        # проставляем фактические отметки actual_1
        insertion_point_ditch_actual_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                          insertion_point[1] + parameters.LEVEL_ACTUAL_1,
                                          insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_2['marks_actual_1'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_ditch_actual_1,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем фактические отметки actual_2
        insertion_point_ditch_actual_2 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                          insertion_point[1] + parameters.LEVEL_ACTUAL_2,
                                          insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_2['marks_actual_2'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_ditch_actual_2,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем отклонения
        insertion_point_difference = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                      insertion_point[1] + parameters.LEVEL_DIFF,
                                      insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_2['mark_difference'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_difference,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   difference_type=difference_type,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # черточки расстояний
        self.profile.distance_segments(insertion_point=insertion_point,
                                       difference=self.axis_distance_x,
                                       pk_int=self.new_pk_int,
                                       pk_float=self.new_pk_float)

        # проставляем текст 'расстояния'
        insertion_point_dist = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                insertion_point[1] + parameters.LEVEL_DISTANCE,
                                insertion_point[2]]
        self.profile.iter_text_cad(object_cad=self.axis_distance_x,
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_dist,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=4,
                                   text_styles=self.text_style,
                                   difference_type=difference_type,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        self.profile.create_horizontal_line(insertion_point, self.distance_profile, parameters.OFFSET_PROFILE,
                                            parameters._step_hor,
                                            self.scale_horizontal)
        # чертим шкалу профиля
        if self.scale_line:
            insertion_point_scale = [insertion_point[0], insertion_point[1] + sum(parameters._step_hor),
                                     insertion_point[2]]
            height_scale = utility.height_scale(data_for_type_2['marks_project'],
                                                data_for_type_2['marks_actual_2'])

            self.profile.create_scale(insertion_point=insertion_point_scale,
                                      height_scale=height_scale,
                                      height_text=parameters.HEIGHT_TEXT,
                                      scale_vertical=self.scale_vertical,
                                      conditional_horizon=conditional_horizon,
                                      text_styles=self.text_style)

        self.acadDoc.Utility.Prompt(f'Готово - {parameters.KEY_TYPE[key_type_1]}.\n')

    def _data_for_profile_type_3(self, key_type_1, key_type_2=None):
        # получаем новый список проектных отметок
        mark_one_project = self.calculations.interpolation_mark(self.position_picketing_one,
                                                                self.data_final[f'project_{key_type_1}'])
        mark_second_project = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                   self.data_final[f'project_{key_type_1}'])

        marks_project = self.calculations.create_new_list_data(self.position_picketing_one,
                                                               self.position_picketing_second,
                                                               mark_one_project,
                                                               mark_second_project,
                                                               self.data_final[f'project_{key_type_1}'])

        # получаем новый список фактических отметок
        mark_one_actual = self.calculations.interpolation_mark(self.position_picketing_one,
                                                               self.data_final[f'actual_{key_type_1}'])
        mark_second_actual = self.calculations.interpolation_mark(self.position_picketing_second,
                                                                  self.data_final[f'actual_{key_type_1}'])

        marks_actual = self.calculations.create_new_list_data(self.position_picketing_one,
                                                              self.position_picketing_second,
                                                              mark_one_actual,
                                                              mark_second_actual,
                                                              self.data_final[f'actual_{key_type_1}'])

        #  список отклонений
        mark_difference = self.calculations.mark_difference(marks_project, marks_actual)

        data_type_3 = {
            'marks_project': marks_project,
            'marks_actual': marks_actual,
            'mark_difference': mark_difference,
        }
        return data_type_3

    def profile_type_3(self, insertion_point, key_type_1, key_type_2, difference_type):
        data_for_type_3 = self._data_for_profile_type_3(key_type_1=key_type_1, key_type_2=key_type_2)
        self.profile.create_header(insertion_point, parameters.PATH_FILE[key_type_1],
                                   self.text_style)  # чертим шапку подвала
        conditional_horizon = utility.conditional_horizon(data_for_type_3['marks_project'],
                                                          data_for_type_3['marks_actual'])

        # проектная линия профиля
        insertion_point_line = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                insertion_point[1] + sum(parameters._step_hor),
                                insertion_point[2]]
        self.profile.create_line_profile(insertion_point=insertion_point_line,
                                         difference=self.axis_distance_x,
                                         mark=data_for_type_3['marks_project'],
                                         scale_vertical=self.scale_vertical,
                                         scale_horizontal=self.scale_horizontal,
                                         line_type='CONTI',
                                         conditional_horizon=conditional_horizon,
                                         vertical_line=True)

        # проставляем проектные отметки
        insertion_point_mark_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                  insertion_point[1] + parameters.LEVEL_PIPE_PROJECT,
                                  insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_3['marks_project'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_mark_1,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем пикетаж
        insertion_point_picketing = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                     insertion_point[1] + parameters.LEVEL_PIPE_PK,
                                     insertion_point[2]]
        self.profile.iter_text_cad(object_cad=self.list_picketing,
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_picketing,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=4,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=0,
                                   decimal=0)

        # проставляем фактические отметки actual
        insertion_point_ditch_actual_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                          insertion_point[1] + parameters.LEVEL_PIPE_ACTUAL,
                                          insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_3['marks_actual'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_ditch_actual_1,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем отклонения
        insertion_point_difference = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                      insertion_point[1] + parameters.LEVEL_PIPE_DIFF,
                                      insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_3['mark_difference'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_difference,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   difference_type=difference_type,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # черточки расстояний
        self.profile.distance_segments(insertion_point=insertion_point,
                                       difference=self.axis_distance_x,
                                       pk_int=self.new_pk_int,
                                       pk_float=self.new_pk_float)

        # проставляем текст 'расстояния'
        insertion_point_dist = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                insertion_point[1] + parameters.LEVEL_PIPE_DISTANCE,
                                insertion_point[2]]
        self.profile.iter_text_cad(object_cad=self.axis_distance_x,
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_dist,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=4,
                                   text_styles=self.text_style,
                                   difference_type=difference_type,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        self.profile.create_horizontal_line(insertion_point, self.distance_profile, parameters.OFFSET_PROFILE,
                                            parameters._step_hor,
                                            self.scale_horizontal)

        # чертим шкалу профиля
        if self.scale_line:
            insertion_point_scale = [insertion_point[0], insertion_point[1] + sum(parameters._step_hor),
                                     insertion_point[2]]
            height_scale = utility.height_scale(data_for_type_3['marks_project'],
                                                data_for_type_3['marks_actual'])

            self.profile.create_scale(insertion_point=insertion_point_scale,
                                      height_scale=height_scale,
                                      height_text=parameters.HEIGHT_TEXT,
                                      scale_vertical=self.scale_vertical,
                                      conditional_horizon=conditional_horizon,
                                      text_styles=self.text_style)

        self.acadDoc.Utility.Prompt(f'Готово - {parameters.KEY_TYPE[key_type_1]}.\n')

    def profile_type_4(self, insertion_point, key_type_1, key_type_2, difference_type):
        data_for_type_2 = self._data_for_profile_type_2(key_type_1=key_type_1, key_type_2=key_type_2)
        self.profile.create_header(insertion_point, parameters.PATH_FILE[key_type_1],
                                   self.text_style)  # чертим шапку подвала
        conditional_horizon = utility.conditional_horizon(data_for_type_2['marks_project'],
                                                          data_for_type_2['marks_actual_2'])

        # проектная линия профиля
        insertion_point_line = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                insertion_point[1] + sum(parameters._step_hor),
                                insertion_point[2]]
        self.profile.create_line_profile(insertion_point=insertion_point_line,
                                         difference=self.axis_distance_x,
                                         mark=data_for_type_2['marks_project'],
                                         scale_vertical=self.scale_vertical,
                                         scale_horizontal=self.scale_horizontal,
                                         line_type='CONTI',
                                         conditional_horizon=conditional_horizon,
                                         vertical_line=True)
        # фактическая линия профиля
        self.profile.create_line_profile(insertion_point=insertion_point_line,
                                         difference=self.axis_distance_x,
                                         mark=data_for_type_2['marks_actual_2'],
                                         scale_vertical=self.scale_vertical,
                                         scale_horizontal=self.scale_horizontal,
                                         line_type='CONTI',
                                         conditional_horizon=conditional_horizon,
                                         vertical_line=False)

        # проставляем проектные отметки обсыпки
        insertion_point_mark_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                  insertion_point[1] + parameters.LEVEL_ACTUAL_2,
                                  insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_2['marks_project'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_mark_1,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем пикетаж
        insertion_point_picketing = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                     insertion_point[1] + parameters.LEVEL_PK,
                                     insertion_point[2]]
        self.profile.iter_text_cad(object_cad=self.list_picketing,
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_picketing,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=4,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=0,
                                   decimal=0)

        # проставляем фактические отметки обсыпки
        insertion_point_ditch_actual_1 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                          insertion_point[1] + parameters.LEVEL_PROJECT,
                                          insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_2['marks_actual_1'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_ditch_actual_1,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем фактические отметки трубы
        insertion_point_ditch_actual_2 = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                          insertion_point[1] + parameters.LEVEL_ACTUAL_1,
                                          insertion_point[2]]
        self.profile.iter_text_cad(object_cad=data_for_type_2['marks_actual_2'],
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_ditch_actual_2,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # проставляем отклонения
        mark_difference = self.calculations.mark_difference(data_for_type_2['marks_actual_2'],
                                                            data_for_type_2['marks_actual_1'])
        insertion_point_difference = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                      insertion_point[1] + parameters.LEVEL_DIFF,
                                      insertion_point[2]]
        self.profile.iter_text_cad(object_cad=mark_difference,
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_difference,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=1,
                                   text_styles=self.text_style,
                                   dx=0,
                                   difference_type=difference_type,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        # черточки расстояний
        self.profile.distance_segments(insertion_point=insertion_point,
                                       difference=self.axis_distance_x,
                                       pk_int=self.new_pk_int,
                                       pk_float=self.new_pk_float)

        # проставляем текст 'расстояния'
        insertion_point_dist = [insertion_point[0] + parameters.OFFSET_PROFILE,
                                insertion_point[1] + parameters.LEVEL_DISTANCE,
                                insertion_point[2]]
        self.profile.iter_text_cad(object_cad=self.axis_distance_x,
                                   difference=self.axis_distance_x,
                                   point_start=insertion_point_dist,
                                   height_text=parameters.HEIGHT_TEXT,
                                   scale_horizontal=self.scale_horizontal,
                                   alignment=4,
                                   text_styles=self.text_style,
                                   difference_type=difference_type,
                                   rotation=parameters.ROTATION_ANGLE_90,
                                   decimal=parameters.DECIMAL_PLACES)

        self.profile.create_horizontal_line(insertion_point, self.distance_profile, parameters.OFFSET_PROFILE,
                                            parameters._step_hor,
                                            self.scale_horizontal)
        # чертим шкалу профиля
        if self.scale_line:
            insertion_point_scale = [insertion_point[0], insertion_point[1] + sum(parameters._step_hor),
                                     insertion_point[2]]
            height_scale = utility.height_scale(data_for_type_2['marks_project'],
                                                data_for_type_2['marks_actual_2'])

            self.profile.create_scale(insertion_point=insertion_point_scale,
                                      height_scale=height_scale,
                                      height_text=parameters.HEIGHT_TEXT,
                                      scale_vertical=self.scale_vertical,
                                      conditional_horizon=conditional_horizon,
                                      text_styles=self.text_style)

        self.acadDoc.Utility.Prompt(f'Готово - {parameters.KEY_TYPE[key_type_1]}.\n')
