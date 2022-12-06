from idlelib.idle_test.test_browser import mb
from tkinter import ttk, Tk, Label, Checkbutton, Entry, Button
import os
passw = False
password = '1234'
sc = None

print(os.uname)
def password_login():

    window = Tk()
    window.title("Активация - Ленивчик")
    window.geometry('480x165')
    lbl_5 = Label(text='Ключ активации', font=('Arial Bold', 9), background="#ff9d00")
    lbl_5.grid(column=2, row=0)
    input_password = Entry(width=13, text="")
    input_password.grid(column=3, row=0)
    btn = Button(text="Активировать", width=20)
    btn.grid(column=4, row=0)
    if input_password.get() == password:
        mb.showinfo(
            "Внимание!",
            "Activ yes")
    else:
        mb.showinfo(
            "Внимание!",
            "Activ no")

    window.mainloop()


def loop():
    window = Tk()
    window.title("Ленивчик")
    window.geometry('480x165')

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Чертилка')
    tab_control.add(tab2, text='Расчет факта')
    tab_control.add(tab3, text='Импорт отметок')


    chk_ditch = Checkbutton(tab1, text='Разработка')
    chk_ditch.grid(column=2, row=2)

    lbl_5 = Label(tab2, text='Выбери файл для расчета -->', font=('Arial Bold', 9), background="#ff9d00")
    lbl_5.grid(column=2, row=0)


    lbl_start = Label(tab3, text="Стартовый ПК:", width=15, font=('Arial Bold', 10))
    lbl_start.grid(column=2, row=2)
    tab_control.pack(expand=1, fill='both')
    window.mainloop()


if passw:
    loop()
else:
    password_login()
