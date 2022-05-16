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
    authentication_data = curs.fetchall()
    curs.close()
    conn.close()
    return authentication_data[0]


def selecting_database_function(phrase):
    answer = 'Ошибка работы с базой данных'
    phrase = Assistant_functions.clean_phrase(phrase,
                                              ['добавь', 'напомни', 'какой', 'пароль', 'логин'])
    if not os.path.exists(f'{DATABASE_NAME}'):
        create_database(DATABASE_NAME)

    if (phrase.find("базу") != -1) and \
            ((phrase.find("очисти") != -1) or (phrase.find("очистить") != -1)
             or (phrase.find("удали") != -1) or (phrase.find("удалить") != -1)):
        answer = 'База данных очищена'

    elif (phrase.find("добавь") != -1) and ((phrase.find("логин") != -1)
                                            or (phrase.find("пароль") != -1)
                                            or (phrase.find("сайн") != -1)
                                            or (phrase.find("данные") != -1)):
        insert_in_database(DATABASE_NAME, TABLE_NAME, ['1', '1', '1'])
        answer = f'''Данные успешно добавлены!'''

    elif (phrase.find("напомни") != -1) or (phrase.find("какой") != -1) \
            and ((phrase.find("пароль") != -1) or (phrase.find("логин") != -1)):
        answer = output_authentication_data()

    return answer


def output_authentication_data():
    authentication_data = get_from_database(DATABASE_NAME, TABLE_NAME, website)

    tmp_text_file = open('tmp.txt', 'w')
    print(f'''Ваши данные для аутентификации: 
    
    Название ресурса ----> {authentication_data[0]}
    Ваш логин ----> {authentication_data[1]}
    Ваш пароль ----> {authentication_data[2]}
    ''', file=tmp_text_file)
    tmp_text_file.close()
    os.startfile('tmp.txt')

    answer = """Вы можете посмотреть данные в открывшемся файле,\nозвучивать их я не буду."""
    return answer


website = 'you tube'
website_data = ['you tube', '0000', '1111']

# insert_in_database(DATABASE_NAME, TABLE_NAME, website_data)
# res = get_from_database(DATABASE_NAME, TABLE_NAME, website)
# print("res[0][0]", res[0][0], "\nres[0]", res[0], "\nres", res)

output_authentication_data()
