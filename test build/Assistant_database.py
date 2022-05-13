# Functional
import sqlite3
import os


# Files
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
    print(curs.fetchall())
    curs.close()
    conn.close()


def selecting_database_function(phrase):
    answer = 'Ошибка работы с базой данных'
    phrase = Assistant_functions.clean_phrase(phrase,
                                              ['добавь', 'напомни', 'какой', 'пароль', 'логин'])

    if (phrase.find("создай") != -1) or (phrase.find("создать") != -1) \
            or (phrase.find("сделай") != -1) or (phrase.find("сделать") != -1):
        answer = 'База данных уже существует'
        if not os.path.exists(f'{DATABASE_NAME}'):
            create_database(DATABASE_NAME)
            answer = 'База данных создана'

    elif (phrase.find("добавь") != -1) and ((phrase.find("логин") != -1)
                                            or (phrase.find("пароль") != -1)
                                            or (phrase.find("сайн") != -1)
                                            or (phrase.find("данные") != -1)):
        insert_in_database(DATABASE_NAME, TABLE_NAME, ['1', '1', '1'])
        answer = f'''
        Для сайта {0} добавлен логин {1} и пароль {2}
        '''

    elif (phrase.find("напомни") != -1) or (phrase.find("какой") != -1) \
            and ((phrase.find("пароль") != -1) or (phrase.find("логин") != -1)):

        answer = f'''
        Для сайта {0} ваш логин {1} и пароль {2}
        '''

    return answer


def write_authentication_data():
    tmp_text_file = open('tmp.txt', 'w')
    print(f'''Пожалуйста заполните данные о веб-сайте! 
    
    Как вы будете к нему обращаться ---->
    Ваш логин ---->
    Ваш пароль ---->''', file=tmp_text_file)
    tmp_text_file.close()
    os.startfile('tmp.txt')

    try:
        with open("tmp.txt", "r") as file:
            # Распечатать сообщение об успешном завершении
            print("Файл открыт для чтения.")
    # Вызовите ошибку, если файл был открыт раньше
    except IOError:
        print("Файл уже открыт")




website = 'you tube'
website_data = ['you tube', '0000', '0000']

write_authentication_data()
# insert_in_database(DATABASE_NAME, TABLE_NAME, website_data)
get_from_database(DATABASE_NAME, TABLE_NAME, website)
