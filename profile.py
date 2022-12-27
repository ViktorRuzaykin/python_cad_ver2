import pythoncom
from pyacadcom import AcadPoint, aDouble

import parameters
import utility
# from arryautocad import APoint, ADouble
from import_object_acad import ImportCadObject
from method_add import AddObject


class ProfileCad:
    def __init__(self, mSp, acadDoc):
        self.add_objects = AddObject()
        self.create_basement_header = ImportCadObject()
        self.mSp = mSp
        self.acadDoc = acadDoc

    def iter_text_cad(self, object_cad, difference, point_start, height_text, scale_horizontal, alignment, rotation,
                      decimal, dx=0, text_styles='Standard', difference_type='м'):
        """
        Расставляем текстовые объекты через заданное расстояние.
        :param decimal:
        :param rotation:
        :param difference_type:
        :param alignment:
        :param scale_horizontal:
        :param text_styles:
        :param object_cad: тестовый объект AutoCad
        :param difference: расстояние между текстом
        :param point_start: точка старта
        :param height_text: высота текста
        :param dx: смещение точки от расчетной позиции
        """
        x, y = point_start[0], point_start[1]

        for item, increment in zip(object_cad, range(len(difference))):
            if object_cad == difference:
                dx = item / 2
            text_position = AcadPoint(x + dx, y, 0).coordinates
            item = utility.format_decimal(item, decimal, difference_type)
            if item != 'False':
                self.add_objects.add_text_autocad(model=self.mSp,
                                                  text=utility.transform_to_str(item),
                                                  position=text_position,
                                                  height=height_text,
                                                  rotation=rotation,
                                                  text_styles=text_styles,
                                                  alignment=alignment)
            x += difference[increment] * scale_horizontal
        if object_cad != difference:
            text_position = AcadPoint(x + dx, y, 0).coordinates
            object_num = utility.format_decimal(object_cad[-1], decimal, difference_type)
            self.add_objects.add_text_autocad(model=self.mSp,
                                              text=utility.transform_to_str(object_num),
                                              position=text_position,
                                              height=height_text,
                                              rotation=rotation,
                                              text_styles=text_styles,
                                              alignment=alignment)
        self.acadDoc.Utility.Prompt(u'Итерация завершена.\n')  # для теста

    def conditional_horizon_text(self, text, text_position, height_text, rotation, text_styles, alignment):
        """
        Подпись условного горизонта
        :param text:
        :param text_position:
        :param height_text:
        :param rotation:
        :param text_styles:
        :param alignment:
        :return:
        """
        text_position = AcadPoint(text_position[0], text_position[1], 0).coordinates
        self.add_objects.add_text_autocad(model=self.mSp,
                                          text=text,
                                          position=text_position,
                                          height=height_text,
                                          rotation=rotation,
                                          text_styles=text_styles,
                                          alignment=alignment)

    def create_header(self, insertion_point, path_file, text_style):
        """
        Создает шапку подвала
        :param text_style:
        :param path_file:
        :param insertion_point: точка вставки подвала
        :return:
        """
        self.create_basement_header.create_basement_header(insertion_point, path_file, text_style)

    def create_line_profile(self, insertion_point, difference, mark, scale_vertical, scale_horizontal, line_type,
                            conditional_horizon, vertical_line=True):
        """
        Создает линия профиля в виде полилинии.
        :param insertion_point: точка вставки линии
        :param difference: расстояние между точками по горизонтали
        :param mark: отметки
        :param scale_vertical: вертикальный масштаб
        :param scale_horizontal: горизонтальный масштаб
        :param line_type: тип линии
        :param conditional_horizon: условный горизонт
        :param vertical_line: флаг для отрисовки вертикальных линий профиля
        :return:
        """

        point_1_x = insertion_point[0]
        point_1_y = insertion_point[1] + (mark[0] - conditional_horizon) * scale_vertical
        list_point = [point_1_x, point_1_y]
        try:
            for i, dist in enumerate(difference):
                point_2_x = point_1_x + float(dist) * scale_horizontal
                point_2_y = point_1_y + ((mark[i + 1] - mark[i]) * scale_vertical)
                list_point.extend([point_2_x, point_2_y])
                if vertical_line:
                    self.mSp.AddLine(AcadPoint(point_1_x, insertion_point[1], 0).coordinates,
                                     AcadPoint(point_1_x, point_1_y, 0).coordinates)
                point_1_x = point_2_x
                point_1_y = point_2_y
            if vertical_line:
                self.mSp.AddLine(AcadPoint(point_1_x, insertion_point[1], 0).coordinates,
                                 AcadPoint(point_1_x, point_1_y, 0).coordinates)
            polyline = self.mSp.AddLightweightPolyline(aDouble(list_point))  # линия профиля
            try:
                polyline.Linetype = line_type  # 'DASHED'
            except pythoncom.com_error:
                pass
        except (AttributeError, TypeError):
            print('1_ошибка AttributeError, TypeError')
            self.create_line_profile(insertion_point, difference, mark, scale_vertical, scale_horizontal, line_type,
                                     conditional_horizon, vertical_line)

    def create_horizontal_line(self, insertion_point, distances, dx, step, scale_horizontal):
        """
        Создает горизонтальные линии в подвале профиля.
        :param scale_horizontal:
        :param step: расстояние между горизонтальными линиями,
        :param dx: длин отступа от контура шапки подвала,
        :param distances: длина профиля,
        :param insertion_point: точка вставки профиля (правый нижний угол шапки подвала)
        :return:
        """
        point_1_x, point_1_y = insertion_point[0], insertion_point[1]
        point_2_x = insertion_point[0] + distances * scale_horizontal + dx
        point_2_y = insertion_point[1]
        self.mSp.AddLine(AcadPoint(point_1_x, point_1_y, 0).coordinates, AcadPoint(point_2_x, point_2_y, 0).coordinates)
        for step_in in step:
            point_1_y += step_in
            point_2_y += step_in
            self.mSp.AddLine(AcadPoint(point_1_x, point_1_y, 0).coordinates,
                             AcadPoint(point_2_x, point_2_y, 0).coordinates)

    def create_vertical_line(self, insertion_point, distances, step, scale_horizontal):
        """
        Создает вертикальные линии в подвале профиля.
        :return:
        """
        point_1_x, point_1_y = insertion_point[0] + 8.50, insertion_point[1]
        point_2_x, point_2_y = insertion_point[0] + 8.50, insertion_point[1] + sum(step)
        self.mSp.AddLine(AcadPoint(point_1_x, point_1_y, 0).coordinates, AcadPoint(point_2_x, point_2_y, 0).coordinates)
        for value_dist in distances:
            point_1_x += value_dist * scale_horizontal
            point_2_x += value_dist * scale_horizontal
            self.mSp.AddLine(AcadPoint(point_1_x, point_1_y, 0).coordinates,
                             AcadPoint(point_2_x, point_2_y, 0).coordinates)

    def create_scale(self, insertion_point, height_scale, height_text, scale_vertical, conditional_horizon,
                     text_styles='Standard'):
        """
        Создает шкалу профиля.
        :param height_scale: высота шкалы
        :param conditional_horizon: условный горизонт профиля
        :param scale_vertical: вертикальный масштаб
        :param text_styles: текстовый стиль создаваемого текста
        :param height_text: высота создаваемого текста
        :param insertion_point: Точка вставки шакалы
        :return:
        """
        point_1_x, point_1_y = insertion_point[0], insertion_point[1] + scale_vertical
        scale_width = parameters.SCALE_WIDTH * scale_vertical

        for q in range(height_scale):
            text_position = AcadPoint(point_1_x - parameters.OFFSET_TEXT_SCALE, point_1_y, 0).coordinates
            self.add_objects.add_text_autocad(model=self.mSp,
                                              text=utility.transform_to_str(conditional_horizon + 1),
                                              position=text_position,
                                              height=height_text,
                                              rotation=0,
                                              text_styles=text_styles,
                                              alignment=11)
            self.mSp.AddLine(AcadPoint(point_1_x - scale_width, point_1_y, 0).coordinates,
                             AcadPoint(point_1_x, point_1_y, 0).coordinates)
            conditional_horizon += 1
            point_1_y += 1 * scale_vertical

        self.mSp.AddLine(AcadPoint(point_1_x, insertion_point[1], 0).coordinates,
                         AcadPoint(point_1_x, point_1_y - scale_vertical, 0).coordinates)
        self.mSp.AddLine(AcadPoint(point_1_x - scale_width, insertion_point[1], 0).coordinates,
                         AcadPoint(point_1_x - scale_width, point_1_y - scale_vertical, 0).coordinates)

    def distance_segments(self, insertion_point, difference, pk_int, pk_float):
        point_1_x = insertion_point[0] + parameters.OFFSET_PROFILE
        point_1_y = insertion_point[1] + parameters._step_hor[1]
        point_2_x = insertion_point[0] + parameters.OFFSET_PROFILE
        point_2_y = insertion_point[1] + parameters._step_hor[1] + 20

        self.mSp.AddLine(AcadPoint(point_1_x, point_1_y, 0).coordinates,
                         AcadPoint(point_2_x, point_2_y + 30, 0).coordinates)

        for count, dist in enumerate(difference):
            # print(count, dist, len(pk_int))
            point_1_x += dist
            point_2_x += dist
            if count == len(pk_int) - 2:
                self.mSp.AddLine(AcadPoint(point_1_x, point_1_y, 0).coordinates,
                                 AcadPoint(point_2_x, point_2_y + 30, 0).coordinates)
                break
            if pk_float[count + 1] == 0:
                self.mSp.AddLine(AcadPoint(point_1_x, point_1_y, 0).coordinates,
                                 AcadPoint(point_2_x, point_2_y + 30, 0).coordinates)
            else:
                self.mSp.AddLine(AcadPoint(point_1_x, point_1_y, 0).coordinates,
                                 AcadPoint(point_2_x, point_2_y, 0).coordinates)
