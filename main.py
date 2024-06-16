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
login = False

def create_keyboard_button(*args):
    kb = []
    for text in args:
        kb.append([KeyboardButton(text=text)])

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True) 
    return keyboard

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    '''Фунция старта, добавляет кнопку'''

    keyboard= create_keyboard_button('Зарегистрироваться✍️', 'Авторизоваться🚪')

    await message.answer(f'Привет!, {html.bold(message.from_user.full_name)}!\nЭто бот-автосалон!\
    \nЗдесь ты можешь посмотреть машины и их характеристики!', reply_markup=keyboard)

@dp.message()
async def another_message(message: Message) -> None:
    '''Функция обработки сообщений, отображает все марки автомобилей, регистирует и авторизовывает пользователя'''
    global login, auto
    if message.text == 'Посмотреть автомобили🚗':
        query_auto = db.select_data(name_table='car', data=['*'], where=False)
        auto = CardAuto(brand=-1, call="car", query=query_auto)
        await message.answer('Выберите автомобиль для просмотра', reply_markup=auto.show())

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
            person = Person()

            try:
                if person.login(password=data[2], email=data[3], username=data[1]):
                    login = True
                    keyboard = create_keyboard_button('Посмотреть автомобили🚗', 'Выйти👋')
                    await message.answer('Вы успешно авторизовались🥳', reply_markup=keyboard)
                else:
                    await message.answer('Такого аккаунта не существует!😔\nПопробуйте снова (нажмите на кнопку "Зарегистрироваться✍️" или введите "/start"')
            except:
                await message.answer('К сожалению, что-то пошло не так😔\nПопробуйте снова (нажмите на кнопку "Зарегистрироваться✍️" или введите "/start")')

        else:
            keyboard = create_keyboard_button('Посмотреть автомобили🚗', 'Выйти👋')     
            await message.answer('Вы уже авторизованы!', reply_markup=keyboard)

    if message.text == 'Выйти👋':
        if login:
            login = False
            keyboard= create_keyboard_button('Зарегистрироваться✍️', 'Авторизоваться🚪')
            await message.answer('Вы успешно вышли!', reply_markup=keyboard)
        else:
            await message.answer('Вы не авторизованы!\nПопробуйте снова (нажмите на кнопку "Авторизоваться🚪" или введите "/start")')


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

            if action[-1] == '-1':
                query_model = db.select_data(**query_data)
                model = CardModel(brand=action[2], model=-1, call='model', query=query_model)
                await query.message.answer('Выберите модель автомобиля', reply_markup=model.show())
            else:
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