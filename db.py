import sqlite3
from typing import List

#FOR HAVING AND JOIN etc U NEED TO WRITE YOURSELF SELECTS
#FOR ADMIN

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
    except:
        print('WRONG!!! ERROR CREATE!!!')
    
def drop_table(*args, **kwargs):
    '''Функция сносит таблицу, название которой вы укажите в словаре (name_table: str)
    
    АККУРАТНО, ПОТЕРЯ ВСЕХ ЗАВИСИМОСТЕЙ И ДАННЫХ'''
    name_table = kwargs['name_table']

    try: 
        conn.execute(f'DROP TABLE {name_table};')
    
    except:
        print('WRONG!!! ERROR DROP!!!')

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
    except:
        print('ERROR!!! WRONG SELECT!!!')
                

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
    except:
        print('ERROR!!! WRONG INSERT!!!')

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
    except:
        print('ERROR!!! WRONG DELETE!!!')

def replace_data(*args, **kwargs):
    '''Функция замены уже существующих данных'''
    name_table = kwargs['name_table']
    values_body = ', '.join(["%s" for _ in kwargs['values_data'].keys()])
    values_name = ', '.join([i for i in kwargs['values_data'].keys()])
    values_data = ['"' + i + '"' for i in kwargs['values_data'].values()]

    conn.execute(f'REPLACE INTO {name_table}({values_name}) VALUES ({values_body})' % (*values_data, ))
    conn.commit()


car = {
    'name_table': 'car', 
    'column_table': [
    'brand_id INTEGER PRIMARY KEY AUTOINCREMENT',
    'owner VARCHAR(50) NOT NULL',
    'brand VARCHAR(50) NOT NULL',
    'img VARCHAR(100) NOT NULL'
]}

specifications = {
    'name_table': 'specifications',
    'column_table': [
        'specifications_id INTEGER PRIMARY KEY AUTOINCREMENT',
        'model VARCHAR(50) NOT NULL',
        'type_of_body VARCHAR(30) NOT NULL',
        'count_of_place INTEGER NOT NULL',
        'type_of_engine VARCHAR(30) NOT NULL',
        'img VARCHAR(100) NOT NULL',
        'brand_id INT NOT NULL',
        'FOREIGN KEY (brand_id) REFERENCES car (brand_id)'
    ]
}

first_select = {
    'name_table':'car', 
    'data':['*'], 
    'relate':'OR', 
    'where_data':{'brand_id': 1, 'owner': 'FORD CO'}, 
    'where':True
}

first_insert = {
    'name_table':'car',
    'values_data': {'owner':'FORD CO', 'brand':'FORD'}
}

first_delete = {
    'name_table':'car',
    'where':True,
    'relate':'OR',
    'where_data':{'brand_id':4, "owner":'dasds'}
}

drop_car = {
    'name_table':'car'
}

drop_specifications = {
    'name_table':'specifications'
}

replace_first = {
    'name_table': 'car',
    'values_data':{'brand_id': "1", 'owner':'FORD11 CO', 'brand':'FORD11'},
}

create_table(name_table=specifications['name_table'], column_table=specifications['column_table'])
create_table(name_table=car['name_table'], column_table=car['column_table'])
# select_data(name_table=first_select['name_table'], data=first_select['data'], relate=first_select['relate'], where_data=first_select['where_data'], where=first_select['where'])
# insert_data(name_table=first_insert['name_table'], values_data=first_insert['values_data'])
# delete_data(name_table=first_delete['name_table'], where=first_delete['where'], relate=first_delete['relate'], where_data=first_delete['where_data'])
# drop_table(name_table=drop_car['name_table'])
# drop_table(name_table=drop_specifications['name_table'])
# replace_data(name_table=replace_first['name_table'], values_data=replace_first['values_data'])
