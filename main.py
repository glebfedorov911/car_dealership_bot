import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from card import *
from user import *

load_dotenv()

TOKEN = os.getenv('TOKEN')

dp = Dispatcher()
auto = 0
model = 0
users = 0
person = 0
who_use_func = 0
login = False
is_admin = False

def create_keyboard_button(*args):
    kb = []
    for text in args:
        kb.append([KeyboardButton(text=text)])

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True) 
    return keyboard

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    '''Фунция старта, добавляет кнопку'''
    global is_admin, login, person

    if login:
        if is_admin:
            keyboard = create_keyboard_button('Посмотреть автомобили🚗', 'Выйти👋', 'Админ Панель')  
        else:
            keyboard = create_keyboard_button('Посмотреть автомобили🚗', 'Выйти👋')
    else:
        keyboard = create_keyboard_button('Зарегистрироваться✍️', 'Авторизоваться🚪')

    await message.answer(f'Привет!, {html.bold(message.from_user.full_name)}!\nЭто бот-автосалон!\
    \nЗдесь ты можешь посмотреть машины и их характеристики!', reply_markup=keyboard)

@dp.message()
async def another_message(message: Message) -> None:
    '''Функция обработки сообщений, отображает все марки автомобилей, регистирует и авторизовывает пользователя'''
    global login, auto, is_admin, users, person 
    if message.text == 'Посмотреть автомобили🚗':
        if login:
            query_auto = db.select_data(name_table='car', data=['*'], where=False)
            auto = CardAuto(brand=-1, call="car", query=query_auto)
            await message.answer('Выберите автомобиль для просмотра', reply_markup=auto.show())
        else:
            keyboard = create_keyboard_button('Зарегистрироваться✍️', 'Авторизоваться🚪')
            await message.answer('Необходимо авторизоваться!!', reply_markup=keyboard)

    if message.text == 'Зарегистрироваться✍️':
        await message.answer('Введите логин, пароль и email через пробел\nНе забудьте написать тэг #регистрация')

    if '#регистрация' in message.text:
        if not login:
            data = message.text.split('\n')
            person = Person()
            select = {
                'name_table':'user', 
                'data':['username', 'email'], 
                'relate':'OR', 
                'where_data':{'username': data[1], 'email': data[3]}, 
                'where':True
            }

            username_email = db.select_data(**select)
            try:
                if username_email != []:
                    await message.answer('Данное имя или email уже заняты!\nПопробуйте снова (нажмите на кнопку "Зарегистрироваться✍️" или введите "/start")')
                else:
                    login = True
                    person.signup(username=data[1], password=data[2], email=data[3])

                    keyboard = create_keyboard_button('Посмотреть автомобили🚗', 'Выйти👋')   

                    await message.answer('Вы успешно зарегистрировались🥳', reply_markup=keyboard)
            except:
                await message.answer('К сожалению, что-то пошло не так😔\nПопробуйте снова (нажмите на кнопку "Зарегистрироваться✍️" или введите "/start")')
        else:
            await message.answer('Вы уже авторизованы!')

    if message.text == 'Авторизоваться🚪':
        await message.answer('Введите логин, пароль и email через пробел\nНе забудьте написать тэг #авторизация')

    if '#авторизация' in message.text:
        if not login:
            data = message.text.split('\n')
            select = {
                'name_table':'user', 
                'data':['is_admin'], 
                'relate':'OR', 
                'where_data':{'username': data[1], 'email': data[3]}, 
                'where':True
            }
                
            is_admin = bool(db.select_data(**select)[0][0])

            try:
                if is_admin:
                    person = Admin()
                else:
                    person = Person()

                if person.login(password=data[2], email=data[3], username=data[1]):
                    login = True

                    if is_admin:
                        keyboard = create_keyboard_button('Посмотреть автомобили🚗', 'Выйти👋', 'Админ Панель')
                        await message.answer('Для добавления нового автомобиля напишите характеристики с тэгом #добавитьавто owner brand img\nдля удаления автомобиля #удалитьавто brand_id\nдля просмотра всех существующих автомобилей с brand_id напишите #покажиавто', reply_markup=keyboard)
                        await message.answer('Для добавления нового модели напишите характеристики с тэгом #добавитьмодель owner brand img\nдля удаления моделей #удалитьмодель brand_id\nдля просмотра всех существующих моделей с brand_id напишите #покажимодели', reply_markup=keyboard)
                        await message.answer('!!! Не забывайте про перенос между параметрами !!!', reply_markup=keyboard)
                    else:
                        keyboard = create_keyboard_button('Посмотреть автомобили🚗', 'Выйти👋')

                    await message.answer('Вы успешно авторизовались🥳', reply_markup=keyboard)
                else:
                    await message.answer('Такого аккаунта не существует!😔\nПопробуйте снова (нажмите на кнопку "Зарегистрироваться✍️" или введите "/start"')
            except:
                await message.answer('К сожалению, что-то пошло не так😔\nПопробуйте снова (нажмите на кнопку "Зарегистрироваться✍️" или введите "/start")')

        else:
            if is_admin:
                keyboard = create_keyboard_button('Посмотреть автомобили🚗', 'Выйти👋', 'Админ Панель')
            else:
                keyboard = create_keyboard_button('Посмотреть автомобили🚗', 'Выйти👋')     
            await message.answer('Вы уже авторизованы!', reply_markup=keyboard)

    if message.text == 'Выйти👋':
        if login:
            login = False
            is_admin = False
            keyboard= create_keyboard_button('Зарегистрироваться✍️', 'Авторизоваться🚪')
            await message.answer('Вы успешно вышли!', reply_markup=keyboard)
        else:
            await message.answer('Вы не авторизованы!\nПопробуйте снова (нажмите на кнопку "Авторизоваться🚪" или введите "/start")')

    if message.text == 'Админ Панель':
        if is_admin:
            query_admin = db.select_data(name_table='user', data=['*'], where=False)
            users = CardUser(call='admin', query=query_admin)
            await message.answer('Выберите Пользователя', reply_markup=users.show())
    
    if '#добавитьавто' in message.text:
        if is_admin:
            data = message.text.split('\n')
            person.new_auto(owner=data[1], brand=data[2], img=data[3])
            await message.answer('Автомобиль добавлен!')
    
    if '#покажиавто' in message.text:
        if is_admin:
            await message.answer(str(person.show_auto()))

    if '#удалитьавто' in message.text:
        if is_admin:
            data = message.text.split('\n')
            person.delete_auto(brand_id=data[1])
            await message.answer('Автомобиль удален!')

    if '#добавитьмодель' in message.text:
        if is_admin:
            data = message.text.split('\n')
            person.new_model(model=data[1], type_of_body=data[2], count_of_place=data[3], type_of_engine=data[4], img=data[5], brand_id=data[6])
            await message.answer('Модель добавлена!')
    
    if '#покажимодели' in message.text:
        if is_admin:
            await message.answer(str(person.show_model()))
    
    if '#удалитьмодель' in message.text:
        if is_admin:
            data = message.text.split('\n')
            person.delete_model(specifications_id=data[1])
            await message.answer('Модель удалена!')


@dp.callback_query(F.data.startswith('admin_'))
async def answer_to_callback_admin(query: CallbackQuery) -> None:
    global is_admin, person, users, who_use_func
    if is_admin:

        action = query.data.split('_')
        if action[1] == 'next':
            await query.message.edit_reply_markup(reply_markup=users.next())
        if action[1] == 'previous':
            await query.message.edit_reply_markup(reply_markup=users.previous())
        if action[1] == 'stay':
            keyboard = InlineKeyboardMarkup(inline_keyboard=users.show_option())
            who_use_func = action[2]
            is_admin_user_use_func = db.select_data(name_table='user', data=['is_admin'], where=True, relate='OR', where_data={'username':who_use_func})
            
            if is_admin_user_use_func[0][0] == 'True':
                await query.message.edit_reply_markup(reply_markup=keyboard)
                await query.message.answer('Пользователь является администратором')
            else:
                await query.message.edit_reply_markup(reply_markup=keyboard)
                await query.message.answer('Пользователь не является администратором')


        if action[1] == 'Назначить админом':
            person.set_admin_user(who_use_func)
            await query.message.answer('Пользователь назначен администратором\nдля продолжения введите /start или нажмите Админ Панель')
        if action[1] == 'Снять с админки':
            person.unset_admin_user(who_use_func)
            await query.message.answer('Пользователь снят с поста администратора\nдля продолжения введите /start или нажмите Админ Панель')
        if action[1] == 'Удалить пользователя':
            person.delete_user_account(who_use_func)

            query_admin = db.select_data(name_table='user', data=['*'], where=False)
            users = CardUser(call='admin', query=query_admin)

            await query.message.edit_reply_markup(reply_markup=users.show())
            await query.message.answer('Пользователь успешно удален\nдля продолжения введите /start или нажмите Админ Панель')


@dp.callback_query(F.data.startswith('car_') | F.data.startswith('model_'))
async def answer_to_callback(query: CallbackQuery) -> None:
    global auto, model
    action = query.data.split('_')

    try:
        if action[1] == 'next':
            if action[0] == 'car':
                await query.message.edit_reply_markup(reply_markup=auto.next())
            else:
                await query.message.edit_reply_markup(reply_markup=model.next())

        if action[1] == 'previous':
            if action[0] == 'car':
                await query.message.edit_reply_markup(reply_markup=auto.previous())
            else:
                await query.message.edit_reply_markup(reply_markup=model.previous())

        if action[1] == 'stay':
            query_data = {
                'name_table': 'specifications',
                'data': ['*'],
                'relate': '',
                'where': True,
                'where_data': {'brand_id':action[2]},
            }

            if action[-1] == '-1': #проверка на модель
                query_model = db.select_data(**query_data)
                model = CardModel(brand=action[2], model=-1, call='model', query=query_model)
                await query.message.answer('Выберите модель автомобиля', reply_markup=model.show())
            else: #есть модель - выводим данные о ней
                query_data['relate'] = 'AND'
                query_data['where_data']['model'] = action[3]
                query_model = db.select_data(**query_data)
                show_caption_model = model.show_caption_model(query_model)
                await query.message.answer_photo(photo=FSInputFile(f'media/{show_caption_model[1]}', filename='car'), caption=show_caption_model[0])

    except:
        await query.message.answer('К сожалению, что-то пошло не так😔\nПопробуйте снова (нажмите на кнопку "Посмотреть автомобили🚗" или введите "/start")')

    await query.answer()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())