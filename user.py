import db
import hashlib
from typing import List, Tuple


class Person:
    '''КЛАСС ПОЛЬЗОВАТЕЛЯ'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def signup(self, username: str, email: str | None, password: str):
        _password = self._password(password)

        insert = {
            'name_table':'user',
            'values_data': {'username':username, 'password':_password, 'is_admin': 'False'}
        }

        if email:
            insert['values_data']['email'] = email

        db.insert_data(**insert)

    def login(self, password: str, username: str | None, email: str | None) -> bool:
        first_select = {
            'name_table':'user', 
            'data':['password'], 
            'relate':'OR', 
            'where_data':{'username': username, 'email': email}, 
            'where':True
        }
        
        select = db.select_data(**first_select)
        return False if select == [] else select[0][0] == self._password(password)

    def _password(self, password):
        return hashlib.md5(password.encode('UTF-8')).hexdigest()

class Admin(Person):
    '''В разработке'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def delete_user_account(self, username: str) -> None:
        delete = {
            'name_table':'user',
            'where':True,
            'relate':'OR',
            'where_data':{'username':username}
        }

        db.delete_data(**delete)

    def set_admin_user(self, username: str) -> None:
        update = {
            'name_table': 'user',
            'values_data': {'is_admin':'True'},
            'where_body': {'username': username}
        }

        db.update_data(**update)

    def unset_admin_user(self, username: str) -> None:
        update = {
            'name_table': 'user',
            'values_data': {'is_admin':'False'},
            'where_body': {'username': username}
        }

        db.update_data(**update)

    def new_auto(self, owner: str, brand: str, img: str) -> None:
        insert = {
            'name_table': 'car',
            'values_data': {'owner':owner, 'brand':brand, 'img': img},
        }

        db.insert_data(**insert)

    def delete_auto(self, brand_id: int) -> None:
        delete = {
            'name_table': 'car',
            'where':True,
            'relate':'OR',
            'where_data':{'brand_id':brand_id}
        }

        db.delete_data(**delete)

    def show_auto(self) -> str:
        select = {
            'name_table':'car', 
            'data':['*'], 
            "where":False
        }

        data = ["brand_id, owner, brand, img"]

        for inf in db.select_data(**select):
            data.append(f'{inf[0]}, {inf[1]}, {inf[2]}, {inf[3]}')

        return '\n'.join(data)

    def new_model(self, model: str, type_of_body: str, count_of_place: str, type_of_engine: str, img: str, brand_id: str) -> None:       
        insert = {
            'name_table': 'specifications',
            'values_data': {'model':model, 'type_of_body':type_of_body, 'count_of_place': count_of_place, "type_of_engine":type_of_engine, "img":img, 'brand_id':brand_id},
        }

        db.insert_data(**insert)

    def delete_model(self, specifications_id: int) -> None:
        delete = {
            'name_table': 'specifications',
            'where':True,
            'relate':'OR',
            'where_data':{'specifications_id':specifications_id}
        }

        db.delete_data(**delete)

    def show_model(self) -> str:
        select = {
            'name_table':'specifications', 
            'data':['*'], 
            "where":False
        }

        data = ["specifications_id, model, type_of_body, count_of_place, type_of_engine, img, brand_id"]

        for inf in db.select_data(**select):
            print(inf)
            data.append(f'{inf[0]}, {inf[1]}, {inf[2]}, {inf[3]}, {inf[4]}, {inf[5]}, {inf[6]}')

        return '\n'.join(data)