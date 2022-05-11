# Functional
import sqlite3


# Files
import Assistant_functions
import Assistant_main_file


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


website = 'you tube5'
website_data = ['you tube5', '0000', '0000']
#create_database(login_details.db)
insert_in_database(DATABASE_NAME, TABLE_NAME, website_data)
get_from_database(DATABASE_NAME, TABLE_NAME, website)
