import csv
import random

import parameters


class Calculations:
    @staticmethod
    def reader_base_file(base_file):
        """
        Чтение базового csv файла с 4-мя колонками: 'пк', 'плюс', 'H трубы', 'Н земли'.
        :return:
        """
        column_1, column_2, column_3, column_4 = [], [], [], []
        with open(base_file, 'r') as csvfile:
            base_file = csv.reader(csvfile, delimiter=";")
            for count, row in enumerate(base_file):
                if count != 0:
                    column_1.append(int(row[0]))
                    column_2.append(float(row[1]))
                    column_3.append(float(row[2]))
                    column_4.append(float(row[3]))
        return column_1, column_2, column_3, column_4

    @staticmethod
    def reader_final_file(final_file):
        """
        Чтение финального файла со всеми отметками.
        :return:
        """
        final_file_data = {
            'pk_int': [],
            'pk_float': [],
            'project_pipe': [],
            'mark_earth': [],
            'project_ditch': [],
            'actual_ditch': [],
            'project_pillow': [],
            'actual_pillow': [],
            'actual_pipe': [],
            'project_filling': [],
            'actual_filling': [],
        }

        with open(final_file, 'r') as csvfile:
            final_file = csv.reader(csvfile, delimiter=";")
            for count, row in enumerate(final_file):
                if count != 0:
                    final_file_data['pk_int'].append(int(row[0]))
                    final_file_data['pk_float'].append(float(row[1]))
                    final_file_data['project_pipe'].append(float(row[2]))
                    final_file_data['mark_earth'].append(float(row[3]))
                    final_file_data['project_ditch'].append(float(row[4]))
                    final_file_data['actual_ditch'].append(float(row[5]))
                    final_file_data['project_pillow'].append(float(row[6]))
                    final_file_data['actual_pillow'].append(float(row[7]))
                    final_file_data['actual_pipe'].append(float(row[8]))
                    final_file_data['project_filling'].append(float(row[9]))
                    final_file_data['actual_filling'].append(float(row[10]))
        return final_file_data

    @staticmethod
    def write(data, name_file):
        """
        Запись данных в сsv файл
        :param name_file: имя файла
        :param data: список с вложенными списками (колонками)
        :return:
        """
        with open(name_file, 'w') as csvfile:
            w = csv.writer(csvfile, delimiter=';', lineterminator='\n')  # delimiter=","
            w.writerows(data)

    @staticmethod
    def calc_project_marks(m_pipe, top_pipe=True):
        """
        Расчет проектных отметок по траншеи, подушке, трубе, обсыпке.
        :param m_pipe: список проектных отметок трубы,
        :param top_pipe: если значение True, то отметки по верху трубы,
        :return: список проектных отметок по траншеи, подушке, трубе, обсыпке.
        """
        print(top_pipe)
        ls_ditch, ls_pillow, ls_pipe, ls_filling = [], [], [], []
        for pipe in m_pipe:
            # вычисляем отметку дна траншеи
            m_ditch = pipe - parameters.DIAMETER_PIPE - parameters.HEIGHT_PILLOW if top_pipe else pipe - parameters.HEIGHT_PILLOW
            ls_ditch.append(round(m_ditch, parameters.DECIMAL_PLACES))
            # вычисляем отметку подушки
            m_pillow = pipe - parameters.HEIGHT_PILLOW if top_pipe else pipe
            ls_pillow.append(round(m_pillow, parameters.DECIMAL_PLACES))
            # вычисляем отметку трубы
            new_top_pipe = pipe
            ls_pipe.append(round(new_top_pipe, parameters.DECIMAL_PLACES))
            # вычисляем отметку присыпки
            m_filling = new_top_pipe + parameters.HEIGHT_FILLING if top_pipe else new_top_pipe + parameters.DIAMETER_PIPE + parameters.HEIGHT_FILLING
            ls_filling.append(round(m_filling, parameters.DECIMAL_PLACES))
        return ls_ditch, ls_pillow, ls_pipe, ls_filling

    @staticmethod
    def cacl_actual_marks(p_ditch, p_pillow, p_pipe, p_filling, method_easy=True):
        """
        Расчет фактических отметок по траншеи, подушке, трубе, обсыпке.
        :param p_ditch: проектные отметки по траншеи,
        :param p_pillow: проектные отметки по подушке,
        :param p_pipe: проектные отметки по трубе,
        :param p_filling: проектные отметки по обсыпке
        :param method_easy:
        :return: возвращает список фактических отметок по траншеи, подушке, трубе, обсыпке.
        """
        ls_actual_ditch, ls_actual_pillow, ls_actual_pipe, ls_actual_filling = [], [], [], []
        for ditch, pillow, pipe, filling in zip(p_ditch, p_pillow, p_pipe, p_filling):
            m_actual_ditch = ditch + random.randint(*parameters.VARIATION_DITCH) / 100
            if method_easy:
                m_actual_pillow = pillow + random.randint(*parameters.VARIATION_PILLOW) / 100
                m_actual_pipe = pipe + random.randint(*parameters.VARIATION_PIPE) / 1000
                m_actual_filling = filling + random.randint(*parameters.VARIATION_FILLING) / 100
            else:
                m_actual_pillow = m_actual_ditch + parameters.HEIGHT_PILLOW
                m_actual_pipe = m_actual_pillow + parameters.DIAMETER_PIPE
                m_actual_filling = filling + random.randint(*parameters.VARIATION_FILLING) / 100
            ls_actual_ditch.append(round(m_actual_ditch, parameters.DECIMAL_PLACES))
            ls_actual_pillow.append(round(m_actual_pillow, parameters.DECIMAL_PLACES))
            ls_actual_pipe.append(round(m_actual_pipe, parameters.DECIMAL_PLACES))
            ls_actual_filling.append(round(m_actual_filling, parameters.DECIMAL_PLACES))
        return ls_actual_ditch, ls_actual_pillow, ls_actual_pipe, ls_actual_filling

    @staticmethod
    def search_position_picketing(input_picketing, distance):
        """
        Определяет в каком промежутке находится введенный пикетаж.
        :param input_picketing: введенный пикетаж
        :param distance: список пикетажа в виде расстояний
        :return:
        """
        info_input_pk = {
            'one_index': 0,
            'second_index': 0,
            'one_distance': 0,
            'second_distance': 0,
            'general_distance': 0
        }
        for count, d in enumerate(distance):
            if d < input_picketing < distance[count + 1]:
                one_distance = input_picketing - d
                second_distance = distance[count + 1] - input_picketing
                general_distance = distance[count + 1] - d
                info_input_pk['one_index'], info_input_pk['second_index'] = count, count + 1
                info_input_pk['one_distance'] = one_distance
                info_input_pk['second_distance'] = second_distance
                info_input_pk['general_distance'] = general_distance
            if input_picketing == d:
                info_input_pk['one_index'], info_input_pk['second_index'] = count, count
        return info_input_pk

    @staticmethod
    def interpolation_mark(info_input_pk, ls_mark):
        """
        Интерполирует отметку.
        :param info_input_pk: информация о новой точке
        :param ls_mark: список отметок
        :return:
        """
        one_distance = info_input_pk['one_distance']
        # second_distance = info_input_pk['second_distance']
        general_distance = info_input_pk['general_distance']
        index_one = info_input_pk['one_index']
        index_second = info_input_pk['second_index']
        if index_one != index_second:
            incline = (ls_mark[index_second] - ls_mark[index_one]) / general_distance
            new_mark_1 = ls_mark[index_one] + (incline * one_distance)
            # new_mark_2 = ls_mark[index_second] - (incline * second_distance)
        else:
            new_mark_1 = ls_mark[index_one]
        return round(new_mark_1, parameters.DECIMAL_PLACES)

    @staticmethod
    def create_new_list_data(info_start, info_stop, m_start, m_stop, ls_mark):
        """
        Создает новый список отметок по указанным пикетам при старте отрисовки профиля.
        :param info_start: информация о старте профиля.
        :param info_stop: информация о конце профиля.
        :param m_start: первая отметка нового списка.
        :param m_stop: последняя отметка нового списка.
        :param ls_mark: список отметок по которому формируется новый список.
        :return:
        """
        slice_one = info_start['second_index']
        slice_second = info_stop['second_index']
        if info_start['one_index'] == info_start['second_index']:
            slice_one = info_start['one_index']
        if info_stop['one_index'] == info_stop['second_index']:
            slice_second = info_stop['one_index'] + 1

        new_list_data = ls_mark[slice_one:slice_second]

        if info_start['one_index'] != info_start['second_index']:
            new_list_data.insert(0, m_start)
        if info_stop['one_index'] != info_stop['second_index']:
            new_list_data.append(m_stop)
        # print(f'срез - {new_list_data}')
        return new_list_data

    @staticmethod
    def mark_difference(marks_one, marks_second, difference_type):
        """
        Расчет разницы
        :param difference_type:
        :param marks_one: фактические отметки траншеи,
        :param marks_second: отметки земли
        :return:
        """
        difference_list = []
        for m_1, m_2 in zip(marks_one, marks_second):
            depth = (m_2 - m_1)
            difference_list.append(depth)
        return difference_list

    @staticmethod
    def create_new_list_picketing(info_start, info_stop, pk_int, pk_float, one, second):
        """
        Формирует новые списки pk_int и pk_float, по введенным пк
        :param info_start: информация о старте профиля
        :param info_stop: информация о конце профиля
        :param pk_int: полный список pk_int
        :param pk_float: полный список pk_float
        :param one: пикетаж начала профиля
        :param second: пикетаж конца профиля
        :return: new_pk_int, new_pk_float
        """
        new_int_pk = pk_int[info_start['second_index']:info_stop['second_index']]
        new_int_float = pk_float[info_start['second_index']:info_stop['second_index']]
        if info_start['one_index'] == info_start['second_index']:
            return new_int_pk + [second // 100], new_int_float + [second % 100]
        else:
            return [one // 100] + new_int_pk + [second // 100], [one % 100] + new_int_float + [second % 100]

    @staticmethod
    def create_new_list_distance(info_start, info_stop, all_distance, one, second):
        """
        Возвращает новый список пикетажа в виде расстояний, по введенным пк,
        :param second:
        :param one:
        :param info_start: информация о старте профиля,
        :param info_stop: информация о конце профиля,
        :param all_distance: полный список пикетажа в виде расстояний,
        :return:
        """

        if info_start['one_index'] == info_start['second_index']:
            return all_distance[info_start['second_index']:info_stop['second_index']] + [second]
        else:
            return [one] + all_distance[info_start['second_index']:info_stop['second_index']] + [second]


# calc = Calculations
"""picket_int, picket_float, mark_pipe, mark_earth = calc.reader_base_file()
print(picket_int, picket_float, mark_pipe, mark_earth)

project_ditch, project_pillow, project_pipe, project_filling = calc.calc_project_marks(mark_pipe)
actual_ditch, actual_pillow, actual_pipe, actual_filling = calc.cacl_actual_marks(project_ditch, project_pillow, project_pipe, project_filling)


f_data = list(zip(picket_int, picket_float,
                  project_pipe, mark_earth,
                  project_ditch, actual_ditch,
                  project_pillow, actual_pillow,
                  actual_pipe,
                  project_filling, actual_filling))
f_data.insert(0, name_column)
calc.write(f_data)
pk_int, pk_float, project_pipe, mark_earth, project_ditch, actual_ditch, project_pillow, actual_pillow, actual_pipe, project_filling, actual_filling = calc.reader_final_file()

print(project_pipe)
f = utility.transform_pk_to_distance(pk_int, pk_float)
print(f)
p = utility.transform_pk_type_one(pk_int, pk_float)
print(p)
start_profile = calc.search_position_picketing(16.47, f)
print(start_profile)
mark_start = calc.interpolation_mark(start_profile, project_pipe)
print(mark_start)
stop_profile = calc.search_position_picketing(239.22, f)
print(stop_profile)
mark_stop = calc.interpolation_mark(stop_profile, project_pipe)
print(mark_stop)
new_data_list = calc.create_new_list_data(start_profile, stop_profile, mark_start, mark_stop, project_pipe)
print(new_data_list)
"""
