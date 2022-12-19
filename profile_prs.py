from import_object_acad import ImportCadObject
from arryautocad import Autocad
import utility
import parameters
from profile import ProfileCad
from calculations import Calculations

prs = ImportCadObject()

start_prs = [0, 70]
start_project = [0, 2.85]
# mark_prs = prs.import_project_marks('Отметки')
# dist_prs = prs.import_distance_line('Отрезки')
mark_prs = [1066.89, 1065.92, 1064.03, 1061.9, 1059.81, 1057.99, 1056.26, 1054.29, 1052.38, 1050.83, 1049.26, 1047.85, 1046.54, 1044.95, 1043.53, 1042.04, 1040.68, 1039.39, 1038.34, 1037.25, 1036.19, 1034.95, 1033.92, 1032.91, 1031.96, 1030.92, 1029.8, 1028.74, 1027.6, 1026.58, 1025.82, 1025.05, 1024.11, 1023.41, 1022.53, 1021.57, 1020.79, 1019.77, 1018.87, 1018.18, 1017.59, 1016.76, 1016.18, 1015.4, 1014.89, 1014.41, 1012.99, 1011.57, 1009.63, 1006.58, 1002.59, 998.61, 994.98, 990.79, 986.89, 983.24, 981.11, 979.14, 977.5, 975.87, 974.35, 972.56, 970.81, 969.18, 967.55, 965.87, 964.18, 962.49, 960.96, 959.42, 957.89, 956.35, 954.82, 953.57, 952.41, 951.25, 950.09, 948.94, 947.86, 946.78, 945.7, 944.62, 943.54, 942.25, 940.96, 939.68, 938.39, 937.1, 935.8, 934.49, 933.04, 931.56, 930.08, 928.74, 927.4, 926.05, 924.71, 923.37, 921.43, 919.45, 917.06, 915.27, 913.54, 911.1, 908.8, 906.72, 904.63, 902.64, 900.81, 898.99, 897.31, 895.99, 894.83, 893.58, 892.33, 891.02, 889.72, 888.41, 887.04, 885.66, 884.27, 882.89, 881.53, 880.01, 878.49, 876.9, 874.78, 872.65, 870.68, 868.72, 866.75, 864.77, 862.55, 860.67, 858.79, 856.57, 854.34, 851.56, 848.67, 845.77, 842.88, 839.98, 836.92, 834.01, 830.98, 827.88, 824.77, 821.67, 818.2, 814.1, 810.12, 806.15, 802.3, 799.52, 797.07, 794.69, 792.82, 791.15, 789.78, 789.53, 789.22, 788.8, 788.37, 787.74]
# picket_int_prs, picket_float_prs = utility.create_pk_int_float(dist_prs, start_prs)
# picket_prs = utility.transform_pk_to_distance(picket_int_prs, picket_float_prs)
picket_prs = [70.0, 80.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0, 320.0, 340.0, 360.0, 380.0, 400.0, 420.0, 440.0, 460.0, 480.0, 500.0, 520.0, 540.0, 560.0, 580.0, 600.0, 620.0, 640.0, 660.0, 680.0, 700.0, 720.0, 740.0, 760.0, 780.0, 800.0, 820.0, 840.0, 860.0, 880.0, 900.0, 920.0, 940.0, 960.0, 980.0, 1000.0, 1020.0, 1040.0, 1060.0, 1080.0, 1100.0, 1120.0, 1140.0, 1160.0, 1180.0, 1200.0, 1220.0, 1240.0, 1260.0, 1280.0, 1300.0, 1320.0, 1340.0, 1360.0, 1380.0, 1400.0, 1420.0, 1440.0, 1460.0, 1480.0, 1500.0, 1520.0, 1540.0, 1560.0, 1580.0, 1600.0, 1620.0, 1640.0, 1660.0, 1680.0, 1700.0, 1720.0, 1740.0, 1760.0, 1780.0, 1800.0, 1820.0, 1840.0, 1860.0, 1880.0, 1900.0, 1920.0, 1940.0, 1960.0, 1980.0, 2000.0, 2020.0, 2040.0, 2060.0, 2080.0, 2100.0, 2120.0, 2140.0, 2160.0, 2180.0, 2200.0, 2220.0, 2240.0, 2260.0, 2280.0, 2300.0, 2320.0, 2340.0, 2360.0, 2380.0, 2400.0, 2420.0, 2440.0, 2460.0, 2480.0, 2500.0, 2520.0, 2540.0, 2560.0, 2580.0, 2600.0, 2620.0, 2640.0, 2660.0, 2680.0, 2700.0, 2720.0, 2740.0, 2760.0, 2780.0, 2800.0, 2820.0, 2840.0, 2860.0, 2880.0, 2900.0, 2920.0, 2940.0, 2960.0, 2980.0, 3000.0, 3020.0, 3040.0, 3060.0, 3080.0, 3100.0, 3120.0, 3140.0, 3160.0, 3180.0, 3200.0, 3220.0, 3240.0, 3260.0, 3280.0, 3300.0, 3313.77]
# dist_project = prs.import_distance_line('Отрезки проектные')
dist_project = [0.37, 15.78, 16.0, 21.0, 23.5, 20.5, 5.64, 13.09, 18.27, 25.0, 17.5, 17.77, 2.73, 23.5, 21.0, 17.0, 15.0, 23.5, 1.86, 21.14, 17.0, 19.5, 15.0, 25.5, 11.37, 4.71, 22.42, 25.5, 15.5, 20.25, 0.25, 20.0, 21.5, 30.0, 25.76, 2.74, 23.0, 31.5, 27.5, 18.0, 26.17, 15.33, 14.0, 20.5, 9.26, 2.95, 11.79, 23.0, 24.5, 24.0, 12.5, 16.0, 15.0, 16.5, 21.0, 12.1, 8.08, 27.32, 9.0, 21.07, 13.4, 13.53, 13.0, 15.0, 15.0, 24.5, 30.0, 9.16, 8.82, 27.52, 21.0, 17.0, 19.43, 23.07, 19.5, 20.0, 22.46, 20.54, 15.5, 21.5, 20.5, 19.0, 18.0, 22.5, 20.0, 12.28, 20.72, 16.0, 26.5, 24.5, 18.5, 19.5, 28.0, 24.84, 9.16, 21.0, 20.97, 25.03, 13.5, 19.5, 23.0, 20.0, 21.5, 18.0, 17.5, 22.5, 21.0, 18.5, 20.0, 10.73, 7.27, 15.0, 23.09, 23.41, 23.0, 15.5, 7.5, 23.95, 23.05, 24.5, 21.0, 25.0, 22.0, 21.0, 21.0, 11.0, 22.0, 20.38, 28.12, 16.42, 13.08, 20.5, 23.0, 21.5, 21.0, 14.0, 13.0, 25.5, 19.0, 20.12, 22.38, 16.5, 16.5, 19.5, 26.34, 21.16, 18.0, 18.8, 23.2, 26.93, 13.07, 19.5, 18.5, 26.5, 21.5, 14.0, 12.5, 15.5, 19.5, 25.6, 26.9, 14.0, 27.54, 22.96, 19.78, 15.72, 24.0, 22.5, 20.0, 28.3, 5.2, 19.5, 18.0, 16.5, 17.0, 18.0, 11.0, 17.5]
picket_int_project, picket_float_project = utility.create_pk_int_float(dist_project, start_project)
picket_project = utility.transform_pk_to_distance(picket_int_project, picket_float_project)

# print(dist_prs)
# print(picket_int)
# print(picket_float)
# print(mark_prs)
# print(picket_prs)
# print(picket_project)
new_marks_list = []
new_list_dist = []


def calc():
    for count_prs, d_prs in enumerate(picket_prs):
        if count_prs == len(picket_prs) - 1:
            # print(count_prs, len(picket_prs))
            break
        a = picket_prs[count_prs]
        b = picket_prs[count_prs + 1]
        for count_project, d_project in enumerate(picket_project):

            if a < d_project < b:
                i = (mark_prs[count_prs+1] - mark_prs[count_prs]) / (b - a)
                h = i * (d_project - a)
                new_mark = mark_prs[count_prs] + h
                new_marks_list.append(new_mark)
                new_list_dist.append(d_project)
            if d_project == d_prs:
                new_marks_list.append(mark_prs[count_prs])
                new_list_dist.append(d_project)

    new_marks_list.append(mark_prs[-1])
    new_marks_list.insert(0, mark_prs[0])
    new_list_dist.append(picket_prs[-1])
    new_list_dist.insert(0, 70)


calc()
# print(new_marks_list)
# print(len(picket_prs), len(mark_prs))
print(len(new_marks_list), len(picket_project), len(mark_prs))
print(picket_project)
print(new_list_dist)
difference = utility.transform_to_difference(new_list_dist)
print(difference)
print(len(difference), print(len(new_marks_list)))

acad = Autocad()
mSp = acad.active_model
acadDoc = acad.active_doc
profile = ProfileCad(mSp, acadDoc)
conditional_horizon = utility.conditional_horizon(new_marks_list, new_marks_list)
insertion_point = acad.get_point(text='Укажите точку вставки профиля: ')

con_hor_text = [insertion_point[0] - 79,
                insertion_point[1] + sum(parameters.STEP_HORIZONTAL_DITCH) + 5,
                insertion_point[2]]
conditional_horizon_text = f'Условный горизонт {"{:.2f}".format(float(conditional_horizon))}м'
profile.conditional_horizon_text(text=conditional_horizon_text,
                                      text_position=con_hor_text,
                                      height_text=4,
                                      rotation=0,
                                      text_styles='СПДС',
                                      alignment=0)
insertion_point_ditch = [insertion_point[0] + parameters.OFFSET_PROFILE,
                         insertion_point[1] + sum(parameters.STEP_HORIZONTAL_DITCH),
                         insertion_point[2]]



profile.create_line_profile(insertion_point=insertion_point_ditch,
                                 difference=difference,
                                 mark=new_marks_list,
                                 scale_vertical=1000/100,
                                 scale_horizontal=1000/1000,
                                 line_type='CONTI',
                                 conditional_horizon=conditional_horizon,
                                 vertical_line=True)

profile.iter_text_cad(object_cad=new_marks_list,
                           difference=difference,
                           point_start=insertion_point,
                           height_text=4,
                           scale_horizontal=1000/1000,
                           alignment=1,
                           text_styles='СПДС',
                           dx=parameters.OFFSET_TEXT_LINE)

profile.iter_text_cad(object_cad=new_list_dist,
                           difference=difference,
                           point_start=[insertion_point[0], insertion_point[1] - 30, insertion_point[2]],
                           height_text=4,
                           scale_horizontal=1000/1000,
                           alignment=1,
                           text_styles='СПДС',
                           dx=parameters.OFFSET_TEXT_LINE)

data = zip(new_list_dist, new_marks_list)

Calculations.write(data, 'prs_profile.csv')
