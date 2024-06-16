import db
import hashlib


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
    
    def delete_user_account(self, username: str) -> bool:
        pass

    def set_admin_user(self, username: str) -> bool:
        pass

    def unset_admin_user(self, username: str) -> bool:
        pass

    def new_auto(self, owner: str, brand: str, img: str) -> None:
        pass

    def delete_auto(self, brand_id: int) -> None:
        pass