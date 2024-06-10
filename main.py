import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html, F
from aiogram.types import Message, FSInputFile, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

import db

load_dotenv()

TOKEN = os.getenv('TOKEN')

dp = Dispatcher()
page = 0
page_model = 0
pages = {1:[0, 2], 2:[2, 4], 3:[4, 6], 4:[6, 8]}
owner = 0

def create_button_auto(data: list, page: int, call: str) -> InlineKeyboardMarkup:
    kb = []
    for car in data[pages[page][0]:pages[page][1]]:  
        if call == 'model':
            brand = car[-1]
            model = car[1]
        else:
            brand = car[0]
            model = -1

        kb.append([InlineKeyboardButton(text=str(car[1]), callback_data=f'{call}_._{brand}_{model}')])

    if page == 1:
        kb.append([InlineKeyboardButton(text='>>>', callback_data=f'{call}_next')])
    elif page > 1 and page < max(pages.keys()):
        kb.append([InlineKeyboardButton(text='>>>', callback_data=f'{call}_next')])
        kb.append([InlineKeyboardButton(text='<<<', callback_data=f'{call}_previous')])
    else:
        kb.append([InlineKeyboardButton(text='<<<', callback_data=f'{call}_previous')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    global page, page_model
    page_model = 0
    page = 0
    kb = [
        [KeyboardButton(text='Посмотреть автомобили🚗')]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(f'Привет!, {html.bold(message.from_user.full_name)}!\nЭто бот-автосалон!\
    \nЗдесь ты можешь посмотреть машины и их характеристики!', reply_markup=keyboard)

@dp.message()
async def check_auto(message: Message) -> None:
    global page, page_model
    
    if message.text == 'Посмотреть автомобили🚗':
        page = 1
        page_model = 1
        auto = db.select_data(name_table='car', data=['*'], where=False)

        keyboard = create_button_auto(auto, page, 'car')

        await message.answer('Выбери автомобили, который хочешь посмотреть!', reply_markup=keyboard) 

    if message.text == 'Домой🏠':
        page = 0
        page_model = 0
        kb = [
            [KeyboardButton(text='Посмотреть автомобили🚗')]
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=False)
        await message.answer(f'Ты снова хочешь посмотреть авто?', reply_markup=keyboard)
    
@dp.callback_query(F.data.startswith('car_') | F.data.startswith('model_'))
async def answer_to_callback_car(query: CallbackQuery) -> None:
    global page, page_model, owner
    action = query.data.split('_')
    auto = db.select_data(name_table='car', data=['*'], where=False)

    try:    
        if action[1] == 'next' and action[0] == 'car':
            #след. страница с фирмами
            page += 1

            keyboard = create_button_auto(auto, page, 'car')
            
            await query.message.edit_reply_markup(reply_markup=keyboard)

        elif action[1] == 'previous' and action[0] == 'car':
            #пред. страница с фирмами
            page -= 1

            keyboard = create_button_auto(auto, page, 'car')

            await query.message.edit_reply_markup(reply_markup=keyboard)
        elif action[1] == 'next' and action[0] == 'model':
            #след. страница с модельками
            model = db.select_data(name_table='specifications', data=['*'], where=True, relate='OR', where_data={'brand_id':owner})    
            page_model += 1

            keyboard = create_button_auto(model, page_model, 'model')
            
            await query.message.edit_reply_markup(reply_markup=keyboard)
        elif action[1] == 'previous' and action[0] == 'model':
            #пред. страница с модельками
            model = db.select_data(name_table='specifications', data=['*'], where=True, relate='OR', where_data={'brand_id':owner})    
            page_model -= 1

            keyboard = create_button_auto(model, page_model, 'model')

            await query.message.edit_reply_markup(reply_markup=keyboard)
        elif action[1] == '.' and action[0] == 'model':
            #отображение инфы о модели
            data = db.select_data(name_table='specifications', data=['*'], where=True, relate='OR', where_data={'model':action[-1]})[0]
            kb = [[KeyboardButton(text='Домой🏠')]]
            keyboard = ReplyKeyboardMarkup(keyboard=kb)
            
            await query.message.answer_photo(photo= FSInputFile(f'media/{data[-2]}', filename='1'), caption=f'{data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[6]}', reply_markup=keyboard)
            
        else:
            #cоздание показа моделей авто
            owner = action[2]
            model = db.select_data(name_table='specifications', data=['*'], where=True, relate='OR', where_data={'brand_id':owner})
            keyboard = create_button_auto(model, page_model, 'model')
            await query.message.answer('Выберите модель автомобиля', reply_markup=keyboard)
    except:
        await query.message.answer('Ошибка😔 Попробуйте снова!!', reply_markup=keyboard)


    await query.answer()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())