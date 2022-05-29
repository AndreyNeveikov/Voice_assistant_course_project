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


class DatabaseFunctionSelector:
    def __init__(self):
        self.error_answer = 'Ошибка работы с базой данных'

    def selecting_database_function(self, phrase):
        """
        Selecting the function of interaction with the database

        :param phrase: User command
        :return: Function Success Phrase
        """
        answer = self.error_answer
        phrase = Assistant_functions.clean_phrase(phrase,
                                                  ['база', 'баз', 'данных'])
        if not os.path.exists(f'{DATABASE_NAME}'):
            WorkingWithDatabaseUsingSQL().create_database()

        if (phrase.find("базу") != -1) and \
                ((phrase.find("очисти") != -1) or (phrase.find("очистить") != -1)
                 or (phrase.find("удали") != -1) or (phrase.find("удалить") != -1)):
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'login_details.db')
            os.remove(path)

            WorkingWithDatabaseUsingSQL().create_database()
            answer = 'База данных очищена'

        elif ((phrase.find("добавь") != -1) or (phrase.find("добавить") != -1)
              or (phrase.find("записать") != -1) or (phrase.find("записать") != -1))\
                and ((phrase.find("логин") != -1) or (phrase.find("пароль") != -1)
                     or (phrase.find("сайн") != -1) or (phrase.find("данные") != -1)):
            DatabaseUserInteraction().input_authentication_data()
            answer = """Данные успешно добавлены в базу,\nвы можете просмотреть их с помощью голосовой команды."""

        elif ((phrase.find("удали") != -1) or (phrase.find("удалить") != -1)) \
                and ((phrase.find("данные") != -1) or (phrase.find("запись") != -1) or (phrase.find("сайт") != -1)):
            DatabaseUserInteraction().delete_authentication_data()
            answer = 'Готово! Помните о безопасности ваших персональных данных!!!'

        elif ((phrase.find("напомни") != -1) or (phrase.find("какой") != -1)) \
                and ((phrase.find("пароль") != -1) or (phrase.find("логин") != -1)):
            DatabaseUserInteraction().output_authentication_data()
            answer = 'Готово! Помните о безопасности ваших персональных данных!!!'

        return answer


class WorkingWithDatabaseUsingSQL:
    def __init__(self):
        self.database_name = DATABASE_NAME
        self.db_table_name = TABLE_NAME

    def create_database(self):
        """
        Creating a database to store user authentication data

        :return: Nothing
        """
        conn = sqlite3.connect(f'{self.database_name}')
        curs = conn.cursor()

        curs.execute('''CREATE TABLE login_details
        (website VARCHAR(30) PRIMARY KEY,
        login VARCHAR(30),
        password VARCHAR(30))''')

        curs.close()
        conn.close()

    def insert_in_database(self, inserted_data):
        """
        Adds user data to the database

        :param inserted_data: User data
        :return: nothing
        """
        conn = sqlite3.connect(f'{self.database_name}')
        curs = conn.cursor()
        insert_template = f'''INSERT INTO {self.db_table_name} 
        (website, login, password) VALUES(?, ?, ?)'''
        curs.execute(insert_template,
                     (f'{inserted_data[0]}', f'{inserted_data[1]}', f'{inserted_data[2]}'))
        conn.commit()
        curs.close()
        conn.close()

    def delete_from_database(self, deleted_data):
        """
        Delete user data to the database

        :param deleted_data: User data
        :return: nothing
        """
        print(deleted_data)
        conn = sqlite3.connect(f'{self.database_name}')
        curs = conn.cursor()
        curs.execute(f'''DELETE FROM {self.db_table_name}
                WHERE website = "{deleted_data}"''')
        conn.commit()
        curs.close()
        conn.close()

    def get_from_database(self, requested_website):
        """
        Searches the required user data in the database

        :param requested_website: The site for which the data is needed
        :return: User authentication data
        """
        conn = sqlite3.connect(f'{self.database_name}')
        curs = conn.cursor()
        curs.execute(f'''SELECT * FROM {self.db_table_name}
        WHERE website = "{requested_website}"''')
        authentication_data = curs.fetchall()
        curs.close()
        conn.close()
        if not authentication_data:
            return 0
        return authentication_data[0]


class DatabaseUserInteraction:
    def __init__(self):
        self.root = Tk()

    def output_authentication_data(self):
        """
        Displaying user data in the interface

        :return: Nothing
        """

        def btn_click():
            site = str(site_input.get())
            if len(site) > 0:
                authentication_data = WorkingWithDatabaseUsingSQL().get_from_database(site)
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

        self.root['bg'] = '#ffffff'
        self.root.title('Будте осторожны со свой персональной информацией')
        self.root.wm_attributes('-alpha', 0.99)
        self.root.geometry('400x450')

        self.root.resizable(width=False, height=False)

        frame = Canvas(self.root, bg='white')
        frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

        img_png = PhotoImage(file='img/data_security.png')
        frame.create_image(200, 250, image=img_png)

        title = Label(frame, text='Введите нужный ресурс', bg='white', font=40)
        title.pack(pady=15)

        site_input = Entry(frame, bg='white')
        btn_find = Button(frame, text='Найти', bg='red', command=btn_click)
        btn_done = Button(frame, text='Готово', command=self.root.destroy)

        site_input.pack(side=TOP)
        btn_find.pack(side=TOP, pady=15)
        btn_done.pack(side=BOTTOM, pady=30)

        self.root.mainloop()

    def delete_authentication_data(self):
        """
        Deleting user data by the interface

        :return: Nothing
        """

        def btn_click():
            site = str(site_input.get())
            if len(site) > 0:
                authentication_data = WorkingWithDatabaseUsingSQL().get_from_database(site)
                if authentication_data == 0:
                    messagebox.showerror(title='Запись не найдена',
                                         message=f'''В базе не существует записи с данным ресурсом''')
                else:
                    WorkingWithDatabaseUsingSQL().delete_from_database(site)
                    messagebox.showwarning(title='Успех!', message=f'''Данные успешно удалены!''')
            else:
                messagebox.showerror(title='Поле не заолнено',
                                     message=f'''Необходимо заполнить поле: "Название ресурса"''')

        self.root['bg'] = '#ffffff'
        self.root.title('Будте осторожны со свой персональной информацией')
        self.root.wm_attributes('-alpha', 0.99)
        self.root.geometry('400x450')

        self.root.resizable(width=False, height=False)

        frame = Canvas(self.root, bg='white')
        frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

        img_png = PhotoImage(file='img/data_security.png')
        frame.create_image(200, 250, image=img_png)

        title = Label(frame, text='Введите нужный ресурс', bg='white', font=40)
        title.pack(pady=15)

        site_input = Entry(frame, bg='white')
        btn_find = Button(frame, text='Удалить', bg='red', command=btn_click)
        btn_done = Button(frame, text='Готово', command=self.root.destroy)

        site_input.pack(side=TOP)
        btn_find.pack(side=TOP, pady=15)
        btn_done.pack(side=BOTTOM, pady=30)

        self.root.mainloop()

    def input_authentication_data(self):
        """
        Displays a window for writing user data

        :return: Nothing
        """

        def btn_click():
            """
            Saves data when button is pressed

            :return: nothing
            """
            site = site_input.get()
            login = login_input.get()
            password = password_input.get()

            if len(site) > 0 and len(login) > 3 and len(password) > 3:
                unique_site_check = WorkingWithDatabaseUsingSQL().get_from_database(site)
                if unique_site_check == 0:
                    WorkingWithDatabaseUsingSQL().insert_in_database([site, login, password])
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

        self.root['bg'] = '#ffffff'
        self.root.title('Будте осторожны со свой персональной информацией')
        self.root.wm_attributes('-alpha', 0.99)
        self.root.geometry('400x450')

        self.root.resizable(width=False, height=False)

        frame = Canvas(self.root, bg='white')
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

        btn_done = Button(frame, text='Готово', command=self.root.destroy)
        btn_done.pack(side=BOTTOM, pady=20)

        self.root.mainloop()
