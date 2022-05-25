# Interface
from tkinter import messagebox
from tkinter import *

# Functional
import sqlite3
import os

# Files
import Assistant_functions


DATABASE_NAME = 'login_details.db'
TABLE_NAME = 'login_details'


def create_database(database_name):
    """
    Creating a database to store user authentication data

    :param database_name: The name of the database to be created
    :return: Nothing
    """
    conn = sqlite3.connect(f'{database_name}')
    curs = conn.cursor()

    curs.execute('''CREATE TABLE login_details
    (website VARCHAR(30) PRIMARY KEY,
    login VARCHAR(30),
    password VARCHAR(30))''')

    curs.close()
    conn.close()


def insert_in_database(database_name, db_table_name, inserted_data):
    """
    Adds user data to the database

    :param database_name: The name of the database
    :param db_table_name: The name of the table in this database
    :param inserted_data: User data
    :return:
    """
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
    """
    Searches the required user data in the database

    :param database_name: The name of the database
    :param db_table_name: The name of the table in this database
    :param requested_website: The site for which the data is needed
    :return: User authentication data
    """
    conn = sqlite3.connect(f'{database_name}')
    curs = conn.cursor()
    curs.execute(f'''SELECT * FROM {db_table_name}
    WHERE website = "{requested_website}"''')
    authentication_data = curs.fetchall()
    curs.close()
    conn.close()
    print(authentication_data)
    if not authentication_data:
        return 0
    return authentication_data[0]


def selecting_database_function(phrase):
    """
    Selecting the function of interaction with the database

    :param phrase: User command
    :return: Function Success Phrase
    """
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
    """
    Displaying user data in the interface

    :return: Nothing
    """
    root = Tk()

    def btn_click():
        site = str(site_input.get())
        if len(site) > 0:
            authentication_data = get_from_database(DATABASE_NAME, TABLE_NAME, site)
            if authentication_data == 0:
                messagebox.showerror(title='Запись не найдена',
                                     message=f'''В базе не существует записи с данным ресурсом''')
            else:
                login = str(authentication_data[1])
                password = str(authentication_data[2])
                messagebox.showwarning(title='Данные', message=f'''Логин: {login}\
                Пароль: {password}''')
        else:
            messagebox.showerror(title='Поле не заолнено',
                                 message=f'''Необходимо заполнить поле: "Название ресурса"''')

    root['bg'] = '#ffffff'
    root.title('Будте осторожны со свой персональной информацией')
    root.wm_attributes('-alpha', 0.99)
    root.geometry('400x450')

    root.resizable(width=False, height=False)

    frame = Canvas(root, bg='white')
    frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    img_png = PhotoImage(file='img/data_security.png')
    frame.create_image(200, 250, image=img_png)

    title = Label(frame, text='Введите нужный ресурс', bg='white', font=40)
    title.pack(pady=15)

    site_input = Entry(frame, bg='white')
    btn_find = Button(frame, text='Найти', bg='red', command=btn_click)
    btn_done = Button(frame, text='Готово', command=root.destroy)

    site_input.pack(side=TOP)
    btn_find.pack(side=TOP, pady=15)
    btn_done.pack(side=BOTTOM, pady=30)

    root.mainloop()


def input_authentication_data():
    """
    Displays a window for writing user data

    :return: Nothing
    """
    root = Tk()

    def btn_click():
        """
        Saves data when button is pressed

        :return: nothing
        """
        site = site_input.get()
        login = login_input.get()
        password = password_input.get()

        if len(site) > 0 and len(login) > 3 and len(password) > 3:
            unique_site_check = get_from_database(DATABASE_NAME, TABLE_NAME, site)
            if len(unique_site_check) == 0:
                insert_in_database(DATABASE_NAME, TABLE_NAME, [site, login, password])
            else:
                messagebox.showerror(title='Ошибка уникальности',
                                     message=f'''Запись с таким названием ресурса уже существует и содержит данные:
                                      
                            Название: {unique_site_check[0]}
                            Логин: {unique_site_check[1]}
                            Пароль: {unique_site_check[2]}''')
        else:
            fields = [site, login, password]
            fields_names = ['Название ресурса', 'Логин', 'Пароль']

            fields_that_must_be_filled = [fields_names[x] for x in range(len(fields)) if len(fields[x]) < 4]
            messagebox.showerror(title='Поля не заолнены',
                                 message=f'''Необходимо заполнить поле: {fields_that_must_be_filled}''')

    root['bg'] = '#ffffff'
    root.title('Будте осторожны со свой персональной информацией')
    root.wm_attributes('-alpha', 0.99)
    root.geometry('400x450')

    root.resizable(width=False, height=False)

    frame = Canvas(root, bg='white')
    frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    img_png = PhotoImage(file='img/data_security.png')
    frame.create_image(200, 270, image=img_png)

    title = Label(frame, text='Введите данные', bg='white', font=40)
    title.pack()

    site_input = Entry(frame, bg='white')
    site_input.pack(pady=4)

    user_label_site = Label(bg='white')
    user_label_site.pack(anchor=NW, padx=25, pady=5)

    user_label_site = Label(text="Название ресурса:", bg="white")
    user_label_site.pack(anchor=NW, padx=25, pady=1)

    login_input = Entry(frame, bg='white')
    login_input.pack(pady=3)

    user_label_login = Label(text="Логин:", bg="white")
    user_label_login.pack(anchor=NW, padx=88, pady=4)

    password_input = Entry(frame, bg='white', show='*')
    password_input.pack(pady=3)

    user_label_password = Label(text="Пароль:", bg="white")
    user_label_password.pack(anchor=NW, padx=79, pady=1)

    btn = Button(frame, text='Сохранить', bg='red', command=btn_click)
    btn.pack(pady=3)

    btn_done = Button(frame, text='Готово', command=root.destroy)
    btn_done.pack(side=BOTTOM, pady=20)

    root.mainloop()


website = 'you tube'
website_data = ['you tube', '0000', '1111']


#insert_in_database(DATABASE_NAME, TABLE_NAME, website_data)
#res = get_from_database(DATABASE_NAME, TABLE_NAME, website)

#output_authentication_data()
#print("res[0][0]", res[0][0], "\nres[0]", res[0], "\nres", res)

#input_authentication_data()
