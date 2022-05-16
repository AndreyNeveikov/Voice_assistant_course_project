# Interface
from tkinter import *

# Functional
import sqlite3
import os

# Files
from tkinter import messagebox

import Assistant_functions


DATABASE_NAME = 'login_details.db'
TABLE_NAME = 'login_details'


def create_database(database_name):
    conn = sqlite3.connect(f'{database_name}')
    curs = conn.cursor()

    curs.execute('''CREATE TABLE login_details
    (website VARCHAR(30) PRIMARY KEY,
    login VARCHAR(30),
    password VARCHAR(30))''')

    curs.close()
    conn.close()


def insert_in_database(database_name, db_table_name, inserted_data):
    conn = sqlite3.connect(f'{database_name}')
    curs = conn.cursor()
    insert_template = f'''INSERT INTO {db_table_name} 
    (website, login, password) VALUES(?, ?, ?)'''
    curs.execute(insert_template,
                 (f'{inserted_data[0]}', f'{inserted_data[1]}', f'{inserted_data[2]}'))
    conn.commit()
    curs.close()
    conn.close()


def get_from_database(database_name, db_table_name, requested_website):
    conn = sqlite3.connect(f'{database_name}')
    curs = conn.cursor()
    curs.execute(f'''SELECT * FROM {db_table_name}
    WHERE website = "{requested_website}"''')
    authentication_data = curs.fetchall()
    curs.close()
    conn.close()
    return authentication_data[0]


def selecting_database_function(phrase):
    answer = 'Ошибка работы с базой данных'
    phrase = Assistant_functions.clean_phrase(phrase,
                                              ['баз', 'данных'])
    if not os.path.exists(f'{DATABASE_NAME}'):
        create_database(DATABASE_NAME)

    if (phrase.find("базу") != -1) and \
            ((phrase.find("очисти") != -1) or (phrase.find("очистить") != -1)
             or (phrase.find("удали") != -1) or (phrase.find("удалить") != -1)):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'login_details.db')
        os.remove(path)

        create_database(DATABASE_NAME)
        answer = 'База данных очищена'

    elif ((phrase.find("добавь") != -1) or (phrase.find("добавить") != -1)
          or (phrase.find("записать") != -1) or (phrase.find("записать") != -1))\
            and ((phrase.find("логин") != -1) or (phrase.find("пароль") != -1)
                 or (phrase.find("сайн") != -1) or (phrase.find("данные") != -1)):
        input_authentication_data()
        answer = """Данные успешно добавлены в базу,\nвы можете посмотреть ее с помощью голосовой команды."""

    elif ((phrase.find("напомни") != -1) or (phrase.find("какой") != -1)) \
            and ((phrase.find("пароль") != -1) or (phrase.find("логин") != -1)):
        output_authentication_data()
        answer = 'Готово! Помните о безопасности ваших персональных данных!!!'

    return answer


def output_authentication_data():
    root = Tk()

    def btn_click():
        site = str(site_input.get())
        print(site)
        authentication_data = get_from_database(DATABASE_NAME, TABLE_NAME, site)
        login = str(authentication_data[1])
        password = str(authentication_data[2])
        print(login, password)
        messagebox.showinfo(title='Данные', message=f'''Логин: {login}\
        Пароль: {password}''')

    root['bg'] = '#ffffff'
    root.title('Будте осторожны со свой персональной информацией')
    root.wm_attributes('-alpha', 0.99)
    root.geometry('600x500')

    root.resizable(width=False, height=False)

    canvas = Canvas(root, height=600, width=500)
    canvas.pack()

    frame = Frame(root, bg='white')
    frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    title = Label(frame, text='Непоказывайте эти данные третьим лицам', bg='white', font=40)
    title.pack()

    btn_exit = Button(frame, text='Выйти', command=root.destroy)
    btn_exit.pack()

    btn = Button(frame, text='Найти', bg='red', command=btn_click)
    btn.pack()

    site_input = Entry(frame, bg='white')
    site_input.pack()

    root.mainloop()


def input_authentication_data():

    root = Tk()

    def btn_click():
        site = site_input.get()
        login = login_input.get()
        password = password_input.get()

        insert_in_database(DATABASE_NAME, TABLE_NAME, [site, login, password])

    root['bg'] = '#ffffff'
    root.title('Будте осторожны со свой персональной информацией')
    root.wm_attributes('-alpha', 0.99)
    root.geometry('600x500')

    root.resizable(width=False, height=False)

    canvas = Canvas(root, height=600, width=500)
    canvas.pack()

    frame = Frame(root, bg='white')
    frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    title = Label(frame, text='Непоказывайте эти данные третьим лицам', bg='white', font=40)
    title.pack()

    btn_exit = Button(frame, text='Выйти', command=root.destroy)
    btn_exit.pack()

    btn = Button(frame, text='Сохранить', bg='red', command=btn_click)
    btn.pack()

    site_input = Entry(frame, bg='white')
    site_input.pack()

    login_input = Entry(frame, bg='white')
    login_input.pack()

    password_input = Entry(frame, bg='white', show='*')
    password_input.pack()

    root.mainloop()


website = 'you tube'
website_data = ['you tube', '0000', '1111']


#insert_in_database(DATABASE_NAME, TABLE_NAME, website_data)
#res = get_from_database(DATABASE_NAME, TABLE_NAME, website)

#output_authentication_data()
#print("res[0][0]", res[0][0], "\nres[0]", res[0], "\nres", res)

#input_authentication_data2()