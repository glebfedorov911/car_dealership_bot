from aiogram import Bot, Dispatcher, html, F
from aiogram.types import Message, FSInputFile, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from typing import List, Tuple, Optional, Union

import db

class CardAuto:
    '''КЛАСС СОЗДАНИЯ КАРТЫ АВТОМОБИЛЕЙ ИЛИ МОДЕЛЕЙ'''
    def __init__(self, brand:int, model:int, call:str, query:Union[Tuple, List]):
        self.query = query
        self.brand = brand
        self.model = model
        self.call = call
        self.page = 1
        self.pages = {1:[0, 2], 2:[2, 4], 3:[4, 6], 4:[6, 8]} #временно, со временем будет редактироваться

    def next(self) -> Tuple:
        self.page += 1
        keyboard = self._create_button_auto()
        return keyboard

    def previous(self) -> Tuple:
        self.page -= 1
        keyboard = self._create_button_auto()
        return keyboard

    def show(self):
        return self._create_button_auto()


    def _create_button_auto(self) -> InlineKeyboardMarkup:
        kb = [*self._show_car()]

        if self.page == 1:
            kb.append([InlineKeyboardButton(text='>>>', callback_data=f'{self.call}_next_notbrand_notmodel')])

        elif self.page == len(self.query):
            kb.append([InlineKeyboardButton(text='<<<', callback_data=f'{self.call}_previous_notbrand_notmodel')])
        
        else:
            kb.append([InlineKeyboardButton(text='>>>', callback_data=f'{self.call}_next_notbrand_notmodel')])
            kb.append([InlineKeyboardButton(text='<<<', callback_data=f'{self.call}_previous_notbrand_notmodel')])

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        return keyboard

    def _show_car(self) -> List:
        kb = []

        for data in self.query[self.pages[self.page][0]:self.pages[self.page][1]]:
            if self.call == 'car':
                self.brand = data[0]    
            else:
                self.brand = data[-1]
                self.model = data[1]

            kb.append([InlineKeyboardButton(text=str(data[1]), callback_data=f'{self.call}_stay_{self.brand}_{self.model}')])

        return kb

class CardModel(CardAuto):
    def show_caption_model(self, query_model) -> Tuple:     
        return (f'''
        Модель: {query_model[0][1]}\nТип кузова: {query_model[0][2]}\nКоличество мест: {query_model[0][3]}\nДвигатель: {query_model[0][4]}
        ''', query_model[0][-2])