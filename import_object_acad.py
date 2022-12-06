import json
import time
import keyboard
import arryautocad
from arryautocad import acad, acadModel, acadDoc, APoint


class ImportCadObject:
    try:
        acad = acad
        mSp = acadModel
        acadDoc = acadDoc
    except OSError:
        print('AutoCad не доступен')

    def __init__(self):
        self.coord_line = {}
        self.info_text = {}
        self.bottom_right_corner_point = []

    @staticmethod
    def write_json_file(point, line, text, name_file):
        path_file = f'{name_file}.txt'
        data_for_autocad = {'bottom_right_corner_point': point,
                            'dict_line': line,
                            'dict_text': text,
                            }
        with open(path_file, 'w') as outfile:
            json.dump(data_for_autocad, outfile, indent=4)

    @staticmethod
    def read_json_file(path_file):
        # path_file = f'{path_file}.txt'
        with open(path_file, 'r') as infile:
            data_from_autocad = json.load(infile)
        return data_from_autocad['bottom_right_corner_point'], data_from_autocad['dict_line'], data_from_autocad[
            'dict_text']

    def import_basement(self, name_file):
        time.sleep(1.4)
        # импорт шапки подвала профиля: текст, мтекст, отрезки
        while len(self.coord_line) == 0:
            if keyboard.is_pressed('esc'):  # если нажата клавиша 'ESC' выходим из цикла импорта
                break
            try:
                self.bottom_right_corner_point = self.acadDoc.Utility.GetPoint(APoint(0, 0),
                                                                               'Правый нижний угол шапки подвала: \n')
                selection = arryautocad.get_selection('Выберите объекты подвала.\n')
                for cad_object in selection:
                    id_object = cad_object.ObjectID
                    if cad_object.ObjectName == 'AcDbLine':
                        start_point = cad_object.StartPoint
                        end_point = cad_object.EndPoint
                        self.coord_line[f'{id_object}'] = (start_point, end_point)

                    if cad_object.ObjectName in ('AcDbMText', 'AcDbText'):
                        self.info_text[f'{id_object}'] = {
                            'object_name': cad_object.ObjectName,
                            'rotation': cad_object.Rotation,
                            'attachment_point': cad_object.AttachmentPoint if cad_object.ObjectName == 'AcDbMText' else cad_object.TextAlignmentPoint,
                            'width': cad_object.Width if cad_object.ObjectName == 'AcDbMText' else None,
                            'height': cad_object.Height,
                            'insertion_point': cad_object.InsertionPoint,
                            'text_string': cad_object.TextString,
                            'text_styles': cad_object.StyleName,
                        }
            except:
                print('error')
                self.acadDoc.Utility.Prompt(u'error\n')
                self.coord_line.clear()

            self.write_json_file(self.bottom_right_corner_point, self.coord_line, self.info_text, name_file)
            self.acadDoc.Utility.Prompt('Импорт завершен\n')
            print(self.info_text)

    def create_basement_header(self, in_point, path_file):
        point, line, text_cad = self.read_json_file(path_file=path_file)
        dx = in_point[0] - point[0]
        dy = in_point[1] - point[1]
        # отрисовка группы линий
        time.sleep(0.5)
        for point in line:
            point_1_x, point_1_y = line[point][0][0] + dx, line[point][0][1] + dy
            point_2_x, point_2_y = line[point][1][0] + dx, line[point][1][1] + dy
            self.mSp.AddLine(APoint(point_1_x, point_1_y), APoint(point_2_x, point_2_y))

        # заполнение шапки подвала текстом
        for text in text_cad:
            time.sleep(0.1)
            point_x, point_y = text_cad[text]['insertion_point'][0] + dx, text_cad[text]['insertion_point'][1] + dy

            if text_cad[text]['object_name'] == 'AcDbMText':
                create_new_mtext = self.mSp.AddMText(APoint(point_x, point_y), 0, text_cad[text]['text_string'])
                create_new_mtext.Height = text_cad[text]['height']
                create_new_mtext.Rotation = text_cad[text]['rotation']
                create_new_mtext.StyleName = text_cad[text]['text_styles']
                create_new_mtext.Width = text_cad[text]['width']
                create_new_mtext.AttachmentPoint = text_cad[text]['attachment_point']
                point_coordinates = APoint(point_x, point_y, 0.00)
                create_new_mtext.InsertionPoint = point_coordinates

            if text_cad[text]['object_name'] == 'AcDbText':
                create_new_text = self.mSp.AddText(text_cad[text]['text_string'], APoint(point_x, point_y), 1)
                create_new_text.Height = text_cad[text]['height']
                create_new_text.Rotation = text_cad[text]['rotation']
                create_new_text.StyleName = text_cad[text]['text_styles']
        self.acadDoc.Utility.Prompt(u'Подвал создан.\n')

    @staticmethod
    def import_project_marks(help_text):
        """
        Импорт проектных отметок из AutoCad.
        :param help_text: подсказка для выбора.
        :return:
        """
        time.sleep(0.2)
        dict_mark = {}
        while len(dict_mark) == 0:
            if keyboard.is_pressed('esc'):  # если нажата клавиша 'ESC' выходим из импорта
                break
            try:
                selection_marks = arryautocad.get_selection(help_text)
                for mark in selection_marks:
                    coord = float(mark.InsertionPoint[0]) * 1000
                    dict_mark[coord] = float(mark.TextString)
            except:
                dict_mark.clear()
        dict_for_mark = dict(sorted(dict_mark.items()))
        return list(dict_for_mark.values())

    @staticmethod
    def import_distance_line(help_text):
        """
        Импорт расстояний между отрезками из AutoCAD.
        :param help_text: текст подсказки для вывода в AutoCAD
        :return: список расстояний между точками
        """
        time.sleep(0.2)
        insert_point = []
        distance_list = []
        while len(insert_point) == 0:
            if keyboard.is_pressed('esc'):  # если нажата клавиша 'ESC' выходим из импорта
                break
            try:
                selection_marks = arryautocad.get_selection(help_text)
                for point in selection_marks:
                    insert_point.append(point.EndPoint[0])  # заполнения списка координатой "Х" отрезка "расстояний"
            except:
                insert_point.clear()
        insert_point = sorted(insert_point)
        for count, dist in enumerate(insert_point):
            if count == len(insert_point) - 1:
                break
            d_var = abs(insert_point[count + 1] - dist)
            if d_var != 0:
                distance_list.append(round(d_var, 2))
        return distance_list


# main = ImportCadObject()
# main.import_basement('transh')
# main.create_basement_header([0, 0 ,0], 'transh')
# main.import_basement('проетные отметки \n')
# time.sleep(1)
# print(main.import_distance_line('проектные отметкиыдели расстояния \n'))