import sqlite3
from typing import List


conn = sqlite3.connect('car_dealership.db')
cur = conn.cursor()

def create_table(*args, **kwargs) -> None:
    '''Функция create_table Помогает создавать таблицу
    необходимо заполнить словарь с названием таблицы (name_table: str)
    и данными в таблице (column_table: list)
    
    ИСПОЛЬЗУЕТСЯ ДЛЯ АДМИН ПАНЕЛИ'''
    try:
        name_table = kwargs['name_table']
        column_in_table = kwargs['column_table']
        space = ((', '.join(('%s',) * len(column_in_table))))
        cur.execute(f'CREATE TABLE IF NOT EXISTS {name_table} ({space});' % (*column_in_table, ))
    except sqlite3.Error as e:
        print('WRONG!!! ERROR CREATE!!!')
        print(e)
    
def drop_table(*args, **kwargs):
    '''Функция сносит таблицу, название которой вы укажите в словаре (name_table: str)
    
    АККУРАТНО, ПОТЕРЯ ВСЕХ ЗАВИСИМОСТЕЙ И ДАННЫХ'''
    name_table = kwargs['name_table']

    try: 
        conn.execute(f'DROP TABLE {name_table};')
    
    except sqlite3.Error as e:
        print('WRONG!!! ERROR DROP!!!')
        print(e)

def select_data(*args, **kwargs) -> List | int:
    '''Функция запроса, есть два режима, получить все данные или определенные (нанести ограничения)
    необходимо заполнить словарь (ниже пример)'''
    name_table = kwargs['name_table']
    data = ', '.join([i for i in kwargs['data']])
    result = []

    try:
        if kwargs['where']:
            relate = kwargs['relate']
            where_body = f' {relate} '.join([f'{i}="%s"' for i in kwargs['where_data'].keys()])
            where_data = list(kwargs['where_data'].values())

            result = conn.execute(f'SELECT {data} FROM {name_table} WHERE {where_body};' % (*where_data, ))
        else:
            result = conn.execute(f'SELECT {data} FROM {name_table};')
    except sqlite3.Error as e:
        print('ERROR!!! WRONG SELECT!!!')
        print(e)
                

    return result.fetchall() if result != [] else 0

def insert_data(*args, **kwargs) -> None:
    '''Функция для добавления данных в таблицу
    пример ниже'''
    name_table = kwargs['name_table']
    values_body = ', '.join(["%s" for _ in kwargs['values_data'].keys()])
    values_name = ', '.join([i for i in kwargs['values_data'].keys()])
    values_data = ['"' + i + '"' for i in kwargs['values_data'].values()]

    try:
        conn.execute(f'INSERT INTO {name_table}({values_name}) VALUES ({values_body});' % (*values_data, ))
        conn.commit()
    except sqlite3.Error as e:
        print('ERROR!!! WRONG INSERT!!!')
        print(e)

def delete_data(*args, **kwargs):
    '''Функция удаления с двумя режимами: все данные или только определенные'''
    name_table = kwargs['name_table']

    try:
        if kwargs['where']:
            relate = kwargs['relate']
            where_body = f' {relate} '.join([f'{i}="%s"' for i in kwargs['where_data'].keys()])
            where_data = list(kwargs['where_data'].values())
            
            conn.execute(f'DELETE FROM {name_table} WHERE {where_body};' % (*where_data, ))
            conn.commit()
        else:
            conn.execute(f'DELETE FROM {name_table};')
            conn.commit()
    except sqlite3.Error as e:
        print('ERROR!!! WRONG DELETE!!!')
        print(e)

def replace_data(*args, **kwargs):
    '''Функция замены уже существующих данных'''
    name_table = kwargs['name_table']
    values_body = ', '.join(["%s" for _ in kwargs['values_data'].keys()])
    values_name = ', '.join([i for i in kwargs['values_data'].keys()])
    values_data = ['"' + i + '"' for i in kwargs['values_data'].values()]

    try:
        conn.execute(f'REPLACE INTO {name_table}({values_name}) VALUES ({values_body})' % (*values_data, ))
        conn.commit()
    except sqlite3.Error as e:
        print('ERROR!!! WRONG REPLACE!!!')
        print(e)

def update_data(*args, **kwargs):
    '''Обновление существующих данных'''
    name_table = kwargs['name_table']
    values_body = ', '.join([i+"=%s" for i in kwargs['values_data'].keys()])
    values_data = ['"' + i + '"' for i in kwargs['values_data'].values()]
    where_body = ', '.join([i+"=%s" for i in kwargs['where_body'].keys()])
    where_data = ['"' + i + '"' for i in kwargs['where_body'].values()]

    try:
        conn.execute(f'UPDATE {name_table} SET {values_body} WHERE ({where_body})' % (*values_data, *where_data))
        conn.commit()
    except sqlite3.Error as e:
        print('ERROR!!! WRONG REPLACE!!!')
        print(e)