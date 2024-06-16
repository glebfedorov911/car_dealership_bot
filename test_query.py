from db import *


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

user = {
    'name_table': 'user',
    'column_table': [
        'user_id INTEGER PRIMARY KEY AUTOINCREMENT',
        'username VARCHAR(100) UNIQUE NOT NULL',
        'password VARCHAR(100) NOT NULL',
        'is_admin BOOLEAN NOT NULL',
        'email VARCHAR(100) UNIQUE NOT NULL'
    ]
}

first_select = {
    'name_table':'car', 
    'data':['*'], 
    'relate':'OR', 
    'where_data':{'brand_id': 1}, 
    'where':True
    # "where":False
}

first_insert = {
    'name_table':'car',
    'values_data': {'owner':'FORD CO', 'brand':'FORD'}
}

first_delete = {
    'name_table':'car',
    'where':True,
    'relate':'OR',
    'where_data':{'brand_id':4}
}

drop_car = {
    'name_table':'car'
}

drop_specifications = {
    'name_table':'specifications'
}

drop_user = {
    'name_table':'user'
}

replace_first = {
    'name_table': 'car',
    'values_data':{'brand_id': "1", 'owner':'FORD11 CO', 'brand':'FORD11'},
}

# create_table(**specifications)
# create_table(**car)
# print(select_data(**first_select))
# insert_data(**first_insert)
# delete_data(**first_delete)
# drop_table(**drop_car)
# drop_table(**drop_specifications)
# replace_data(**replace_first)
# create_table(**user)
# drop_table(**drop_user)