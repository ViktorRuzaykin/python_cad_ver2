import time
import parameters
import utility
from arryautocad import APoint, aDouble
from import_object_acad import ImportCadObject
from method_add import AddObject


class ProfileCad:
    def __init__(self, profile, acad, acadDoc):
        self.add_objects = AddObject()
        self.create_basement_header = ImportCadObject()
        self.mSp = profile
        self.acad = acad
        self.acadDoc = acadDoc

    def iter_text_cad(self, object_cad, difference, point_start, height_text, scale_horizontal, alignment, dx=0,
                      text_styles='Standard'):
        """
        Расставляем текстовые объекты через заданное расстояние.
        :param alignment:
        :param scale_horizontal:
        :param text_styles:
        :param object_cad: тестовый объект AutoCad
        :param difference: расстояние между текстом
        :param point_start: точка старта
        :param height_text: высота текста
        :param dx: смещение точки от расчетной позиции
        """
        time.sleep(0.1)
        x, y = point_start[0], point_start[1]

        for item, increment in zip(object_cad, range(len(difference))):
            text_position = APoint(x + dx, y)
            item = utility.format_decimal(item, parameters.DECIMAL_PLACES)
            self.add_objects.add_text_autocad(model=self.mSp,
                                              text=utility.transform_to_str(item),
                                              position=text_position,
                                              height=height_text,
                                              rotation=parameters.ROTATION_ANGLE_90,
                                              text_styles=text_styles,
                                              alignment=alignment)
            x += difference[increment] * scale_horizontal
        text_position = APoint(x + dx, y)
        object_num = utility.format_decimal(object_cad[-1], parameters.DECIMAL_PLACES)
        self.add_objects.add_text_autocad(model=self.mSp,
                                          text=utility.transform_to_str(object_num),
                                          position=text_position,
                                          height=height_text,
                                          rotation=parameters.ROTATION_ANGLE_90,
                                          text_styles=text_styles,
                                          alignment=alignment)
        self.acadDoc.Utility.Prompt(u'Итерация завершена.\n')  # для теста

    def create_header(self, insertion_point, path_file):
        """
        Создает шапку подвала
        :param path_file:
        :param insertion_point: точка вставки подвала
        :return:
        """
        time.sleep(0.1)
        self.create_basement_header.create_basement_header(insertion_point, path_file)

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
        print(insertion_point[1])
        print(mark[0])
        print(conditional_horizon)
        print(scale_vertical)
        point_1_x = insertion_point[0]
        point_1_y = insertion_point[1] + (mark[0] - conditional_horizon) * scale_vertical

        list_point = [point_1_x, point_1_y]
        print(mark)
        try:
            print(difference)
            for i, dist in enumerate(difference):
                print(i, dist, len(difference), len(mark))
                point_2_x = point_1_x + float(dist) * scale_horizontal
                point_2_y = point_1_y + ((mark[i + 1] - mark[i]) * scale_vertical)
                list_point.extend([point_2_x, point_2_y])
                if vertical_line:
                    self.mSp.AddLine(APoint(point_1_x, insertion_point[1]), APoint(point_1_x, point_1_y))
                point_1_x = point_2_x
                point_1_y = point_2_y
                list_point.extend([point_1_x, point_1_y])
            if vertical_line:
                self.mSp.AddLine(APoint(point_1_x, insertion_point[1]), APoint(point_1_x, point_1_y))
            polyline = self.mSp.AddLightweightPolyline(aDouble(list_point))  # линия профиля
            polyline.Linetype = line_type  # 'DASHED'
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
        point_2_x = insertion_point[0] + distances + dx
        point_2_y = insertion_point[1]
        self.mSp.AddLine(APoint(point_1_x, point_1_y), APoint(point_2_x, point_2_y))
        for step_in in step:
            point_1_y += step_in * scale_horizontal
            point_2_y += step_in * scale_horizontal
            self.mSp.AddLine(APoint(point_1_x, point_1_y), APoint(point_2_x, point_2_y))

    def create_vertical_line(self, insertion_point, distances, step):
        """
        Создает вертикальные линии в подвале профиля.
        :return:
        """
        point_1_x, point_1_y = insertion_point[0] + 8.50, insertion_point[1]
        point_2_x, point_2_y = insertion_point[0] + 8.50, insertion_point[1] + sum(step)
        self.mSp.AddLine(APoint(point_1_x, point_1_y), APoint(point_2_x, point_2_y))
        for value_dist in distances:
            point_1_x += value_dist
            point_2_x += value_dist
            self.mSp.AddLine(APoint(point_1_x, point_1_y), APoint(point_2_x, point_2_y))

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
            text_position = APoint(point_1_x - parameters.OFFSET_TEXT_SCALE, point_1_y)
            self.add_objects.add_text_autocad(model=self.mSp,
                                              text=utility.transform_to_str(conditional_horizon + 1),
                                              position=text_position,
                                              height=height_text,
                                              rotation=0,
                                              text_styles=text_styles,
                                              alignment=11)
            self.mSp.AddLine(APoint(point_1_x - scale_width, point_1_y), APoint(point_1_x, point_1_y))
            conditional_horizon += 1
            point_1_y += 1 * scale_vertical

        self.mSp.AddLine(APoint(point_1_x, insertion_point[1]), APoint(point_1_x, point_1_y - scale_vertical))
        self.mSp.AddLine(APoint(point_1_x - scale_width, insertion_point[1]),
                         APoint(point_1_x - scale_width, point_1_y - scale_vertical))

    def list_styles(self):
        """
        Определяет список доступны текстовых стилей в текущем чертеже.
        :return:
        """
        try:
            return [style.name for style in self.mSp.TextStyles]
        except:
            pass
