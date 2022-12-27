import time

import parameters
import utility
from calculations import Calculations
from import_object_acad import ImportCadObject


class FileCsv:

    def __init__(self, start_picket):
        self.start_picket = start_picket  # начальный пикет импорта отметок и расстояний из AutoCad
        self.import_data = ImportCadObject()
        self.calculations = Calculations

    def create_base_file(self):
        """
        Запись базового csv файла с 4-мя колонками: 'пк', 'плюс', 'H трубы', 'Н земли'.
        :return:
        """
        time.sleep(1)
        project_marks_pipe = self.import_data.import_project_marks(help_text='Выдели отметки по трубе')
        project_marks_earth = self.import_data.import_project_marks(help_text='Выдели отметки по земле')
        project_distance = self.import_data.import_distance_line(help_text='Выдели отрезки расстояний')
        if (project_distance, project_marks_earth, project_distance):
            picket_int, picket_float = utility.create_pk_int_float(project_distance, self.start_picket)
            data_write_base = list(zip(picket_int, picket_float, project_marks_pipe, project_marks_earth))
            data_write_base.insert(0, parameters.NAME_COLUMN)
            name_file_base = f'ПК{self.start_picket[0]}+{"{:.2f}".format(float(self.start_picket[1]))} ' \
                             f'- ПК{picket_int[-1]}+{"{:.2f}".format(float(picket_float[-1]))}_base.csv'
            self.calculations.write(data_write_base, name_file_base)

            if picket_int:
                return name_file_base

    def create_final_file(self, base_file):
        picket_int, picket_float, project_marks_pipe, project_marks_earth = self.calculations.reader_base_file(
            base_file)
        project_ditch, project_pillow, project_pipe, project_filling = self.calculations.calc_project_marks(
            project_marks_pipe, parameters.TOP_PIPE)
        actual_ditch, actual_pillow, actual_pipe, actual_filling = self.calculations.cacl_actual_marks(project_ditch,
                                                                                                       project_pillow,
                                                                                                       project_pipe,
                                                                                                       project_filling,
                                                                                                       method_easy=False)

        data_write_final = list(zip(picket_int, picket_float,
                                    project_marks_pipe, project_marks_earth,
                                    project_ditch, actual_ditch,
                                    project_pillow, actual_pillow,
                                    actual_pipe,
                                    project_filling, actual_filling))
        data_write_final.insert(0, parameters.NAME_COLUMN)
        name_file_final = f'ПК{picket_int[0]}+{"{:.2f}".format(float(picket_float[0]))} ' \
                          f'- ПК{picket_int[-1]}+{"{:.2f}".format(float(picket_float[-1]))}_final.csv'
        self.calculations.write(data_write_final, name_file_final)
        return name_file_final
