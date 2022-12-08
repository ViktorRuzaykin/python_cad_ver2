import sys
from tkinter import Label, Tk, Entry, Button
from tkinter import messagebox as mb, IntVar, ttk
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Checkbutton, Progressbar, Combobox
import pythoncom
from win32ctypes.pywin32 import pywintypes
import win32api
import utility
from arryautocad import Autocad
from calculations import Calculations
from create_profile import CreateProfile

final_data_file = None
pk_int_1 = 0
pk_float_1 = 0
pk_int_2 = 0
pk_float_2 = 0

try:
    acad = Autocad()
    a_doc = acad.active_doc
    list_styles = utility.list_styles(a_doc)
except pythoncom.com_error:
    list_styles = []
print(list_styles)


def open_work_file():
    global final_data_file
    global pk_int_1
    global pk_float_1
    global pk_int_2
    global pk_float_2
    final_data_file = Calculations.reader_final_file(askopenfilename())
    pk_int_1 = int(final_data_file["pk_int"][0])
    pk_float_1 = ("{:.2f}".format(float(final_data_file["pk_float"][0])))
    pk_int_2 = int(final_data_file["pk_int"][-1])
    pk_float_2 = "{:.2f}".format(float(final_data_file["pk_float"][-1]))
    name_file_final = f'ПК{pk_int_1}+{pk_float_1} - ПК{pk_int_2}+{pk_float_2}'

    open_file_lb.configure(text=name_file_final, background="#47fa41")


def stat_draw():
    start_pk = float(''.join(start_pk_en.get().split('+')))
    stop_pk = float(''.join(end_pk_en.get().split('+')))
    new_profile = CreateProfile(data_final=final_data_file,
                                start_profile=start_pk,
                                end_profile=stop_pk,
                                scale_vertical=float(scale_vertical_en.get()),
                                scale_horizontal=float(scale_horizontal_en.get()),
                                text_style=font_combo.get())

    chk_state_list = [chk_state_ditch.get(), chk_state_pillow.get(), chk_state_pipe.get(), chk_state_filling.get()]
    if not final_data_file:
        return mb.showerror('Ошибка!', 'Не выбран файл для работы!')
    if start_pk == stop_pk:
        return mb.showerror('Ошибка!', 'Введенные пикеты не должны быть равны.')
    if start_pk > stop_pk:
        return mb.showerror('Ошибка!', 'Конечный пикет больше начального.')
    if 1 in chk_state_list:
        try:
            acad = Autocad()
        except pythoncom.com_error as f:
            return mb.showerror(getattr(f, 'strerror'), getattr(f, 'strerror'))
        chk_state_list = [chk_state_ditch.get(), chk_state_pillow.get(), chk_state_pipe.get(),
                          chk_state_filling.get()]
        acad = Autocad()
        insertion_point = acad.get_point(text='Укажите точку вставки профиля: ')

        list_point_insert = utility.list_point_insert(chk_state_list=chk_state_list,
                                                      insert_point_start=insertion_point,
                                                      distance_profile=stop_pk - start_pk)

        if chk_state_ditch.get():
            new_profile.profile_type_1(insertion_point=list_point_insert[0], key_type='ditch', difference_type='м')
            list_point_insert.pop(0)

        if chk_state_pillow.get():
            new_profile.profile_type_2(insertion_point=list_point_insert[0], key_type='pillow', difference_type='см')
            list_point_insert.pop(0)

        if chk_state_pipe.get():
            new_profile.profile_type_2(insertion_point=list_point_insert[0], key_type='pipe', difference_type='мм')
            list_point_insert.pop(0)

        if chk_state_filling.get():
            new_profile.profile_type_2(insertion_point=list_point_insert[0], key_type='filling', difference_type='см')
            list_point_insert.pop(0)
    else:
        print('error, work')
        return mb.showerror('Ошибка!', 'Не выбраны виды работ!')




window = Tk()
window.title('Ленивчик')
window.geometry('400x240')
# path_ico = resource_path('kl.ico')
window.resizable(width=True, height=True)
# window.iconbitmap(path_ico)

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Рисовалка')
tab_control.add(tab2, text='Расчет факта')
tab_control.add(tab3, text='Импорт отметок')

# ----------------------------------------- Вкладка 'Рисовалка' ------
open_file_btn = Button(tab1, text='Открыть', command=open_work_file)  # command=file
open_file_btn.place(x=220, y=0)
open_file_lb = Label(tab1, text='Выбери файл для чертилки -->', font=('Arial Bold', 9), background="#ff9d00")
open_file_lb.place(x=20, y=3)

# список доступных шрифтов
styles_font_lb = Label(tab1, text='Шрифт:', font=('Arial Bold', 9))

styles_font_combo = Combobox(tab1, width=10)  # список доступных шрифтов
styles_font_combo['values'] = ['СПДС', 'Standard']
styles_font_combo.current(0)  # установите вариант по умолчанию

# начальный ПК
start_pk_lb = Label(tab1, text='Начало ПК:', font=('Arial Bold', 9))
start_pk_lb.place(x=5, y=30)
start_pk_en = Entry(tab1, width=13)
start_pk_en.place(x=85, y=30)
start_pk_en.insert(0, "2+00.00")

# конечный ПК
end_pk_lb = Label(tab1, text='Конец ПК:  ', font=('Arial Bold', 9))
end_pk_lb.place(x=190, y=30)
end_pk_en = Entry(tab1, width=13)
end_pk_en.place(x=260, y=30)
end_pk_en.insert(0, "3+00.00")

# масштаб отрисовки профиля
scale_lb = Label(tab1, text='Масштаб профиля -', font=('Arial Bold', 9))
scale_lb.place(x=5, y=55)
scale_vertical_lb = Label(tab1, text='В:', font=('Arial Bold', 9))
scale_vertical_lb.place(x=130, y=55)
scale_vertical_en = Entry(tab1, width=6)
scale_vertical_en.insert(0, '200')
scale_vertical_en.place(x=150, y=55)
scale_horizontal_lb = Label(tab1, text='Г:', font=('Arial Bold', 9))
scale_horizontal_lb.place(x=200, y=55)
scale_horizontal_en = Entry(tab1, width=6)
scale_horizontal_en.insert(0, '1000')
scale_horizontal_en.place(x=220, y=55)

# виды работ
scale_lb = Label(tab1, text='Виды работ', font=('Arial Bold', 9))
scale_lb.place(x=110, y=75)
# кнопка выбора 'Разработка'
chk_state_ditch = IntVar()
chk_state_ditch.set(0)
chk_ditch = Checkbutton(tab1, text='Разработка', variable=chk_state_ditch)
chk_ditch.place(x=50, y=95)
# кнопка выбора 'Подушка'
chk_state_pillow = IntVar()
chk_state_pillow.set(0)
chk_pillow = Checkbutton(tab1, text='Подушка', variable=chk_state_pillow)
chk_pillow.place(x=170, y=95)
# кнопка выбора 'Укладка'
chk_state_pipe = IntVar()
chk_state_pipe.set(0)
chk_pipe = Checkbutton(tab1, text='Укладка      ', variable=chk_state_pipe)
chk_pipe.place(x=50, y=115)
# кнопка выбора 'Обсыпка'
chk_state_filling = IntVar()
chk_state_filling.set(0)
chk_filling = Checkbutton(tab1, text='Обсыпка', variable=chk_state_filling)
chk_filling.place(x=170, y=115)
# список шрифтов
font_lb = Label(tab1, text='Шрифт:', font=('Arial Bold', 9))
font_lb.place(x=5, y=140)
font_combo = Combobox(tab1, width=23)
font_combo['values'] = list_styles
font_combo.set('СПДС')
font_combo.place(x=60, y=140)
# кнопка старта отрисовки профиля
start_draw = Button(tab1, text='Забабахать разом!', width=40, command=stat_draw)  # command=calc
start_draw.place(x=30, y=170)

# статус выполнения команды
style = ttk.Style()
progressbar = Progressbar(tab1, length=380, style='black.Horizontal.TProgressbar', mode='determinate', value=0,
                          maximum=100)
progressbar.place(x=10, y=200)
progressbar.start()

# ----------------------------------------- Вкладка 'Расчет факта' ------
btn_1 = Button(tab2, text="Открыть", )  # command=calc_file
btn_1.grid(column=3, row=4)

lbl_5 = Label(tab2, text='Выбери файл для расчета -->', font=('Arial Bold', 9), background="#ff9d00")
lbl_5.grid(column=2, row=4)

lbl_pass1 = Label(tab2, width=15)
lbl_pass1.grid(column=1, row=3)
lbl_pass2 = Label(tab2, width=15)
lbl_pass2.grid(column=2, row=2)

# ----------------------------------------- Вкладка 'Импорт отметок' ------
btn_1_3 = Button(tab3, text='Импорт', width=12, )  # command=add_mark_in_excel
btn_1_3.grid(column=4, row=2)

text_info = 'Выбери данные в последовательности:\n1 - отметки по трубе\n2 - отметки по земле' \
            '\n3 - отрезки по расстоянию. \n!Внимание! \nГоризонтальный масштаб должеть быть 1:1'
lbl_info = Label(tab3, text=text_info, font=('Arial Bold', 10))
lbl_info.grid(column=2, row=4, columnspan=4)

lbl_start = Label(tab3, text='Стартовый ПК:', width=15, font=('Arial Bold', 10))
lbl_start.grid(column=2, row=2)

input_start_import = Entry(tab3, width=15)
input_start_import.grid(column=3, row=2)

lbl_pass = Label(tab3, text='             ', font=('Arial Bold', 10))
lbl_pass.grid(column=1, row=2)

tab_control.pack(expand=1, fill='both')
window.mainloop()
