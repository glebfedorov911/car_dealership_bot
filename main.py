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
pages = {1:[0, 2], 2:[2, 4], 3:[4, 6], 4:[6, 8]}

def create_button_auto(data: list, page: int) -> InlineKeyboardMarkup:
    kb = []
    for car in data[pages[page][0]:pages[page][1]]:     
        kb.append([InlineKeyboardButton(text=str(car[1]), callback_data=f'car_{car[0]}')])

    if page == 1:
        kb.append([InlineKeyboardButton(text='>>>', callback_data=f'car_next')])
    elif page > 1 and page < max(pages.keys()):
        kb.append([InlineKeyboardButton(text='>>>', callback_data=f'car_next')])
        kb.append([InlineKeyboardButton(text='<<<', callback_data=f'car_previous')])
    else:
        kb.append([InlineKeyboardButton(text='<<<', callback_data=f'car_previous')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    global page, page_model
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
        auto = db.select_data(name_table='car', data=['*'], where=False)

        keyboard = create_button_auto(auto, page)

        await message.answer('Выбери автомобили, который хочешь посмотреть!', reply_markup=keyboard) 

    if message.text == 'Домой🏠':
        page = 0
        kb = [
            [KeyboardButton(text='Посмотреть автомобили🚗')]
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=False)
        await message.answer(f'Ты снова хочешь посмотреть авто?', reply_markup=keyboard)
    
@dp.callback_query(F.data.startswith('car_'))
async def answer_to_callback(query: CallbackQuery) -> None:
    global page
    action = query.data.split('_')
    auto = db.select_data(name_table='car', data=['*'], where=False)

    if action[1] == 'next':
        page += 1

        keyboard = create_button_auto(auto, page)
        
        await query.message.edit_reply_markup(reply_markup=keyboard)

    elif action[1] == 'previous':
        page -= 1

        keyboard = create_button_auto(auto, page)

        await query.message.edit_reply_markup(reply_markup=keyboard)

    await query.answer()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())