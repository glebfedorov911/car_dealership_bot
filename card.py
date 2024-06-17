from aiogram import Bot, Dispatcher, html, F
from aiogram.types import Message, FSInputFile, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from typing import List, Tuple

import db

class Card:
    '''КЛАСС РОДИТЕЛЬ ДЛЯ ВСЕХ КАРТ'''
    def __init__(self, call:str, query:Tuple | List, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        self.call = call
        self.page = 1
        self.pages = {1:[0, 2], 2:[2, 4], 3:[4, 6], 4:[6, 8]} #временно, со временем будет редактироваться

    def next(self) -> Tuple:
        self.page += 1
        keyboard = self._create_button()
        return keyboard

    def previous(self) -> Tuple:
        self.page -= 1
        keyboard = self._create_button()
        return keyboard

    def show(self):
        return self._create_button()

    def _create_button(self) -> InlineKeyboardMarkup:
        kb = [*self._show_card()]

        if self.page == 1:
            kb.append([InlineKeyboardButton(text='>>>', callback_data=f'{self.call}_next')])

        elif self.page == len(self.query):
            kb.append([InlineKeyboardButton(text='<<<', callback_data=f'{self.call}_previous')])
        
        else:
            kb.append([InlineKeyboardButton(text='>>>', callback_data=f'{self.call}_next')])
            kb.append([InlineKeyboardButton(text='<<<', callback_data=f'{self.call}_previous')])

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        return keyboard

    def _show_card(self) -> List:
        kb = []

        for data in self.query[self.pages[self.page][0]:self.pages[self.page][1]]:
            kb.append([InlineKeyboardButton(text=str(data[1]), callback_data=f'{self.call}_stay')])

        return kb

class CardAuto(Card):
    '''КЛАСС СОЗДАНИЯ КАРТЫ АВТОМОБИЛЕЙ'''
    def __init__(self, brand:int, **kwargs):
        super().__init__(**kwargs)
        self.brand = brand

    def _create_button(self) -> InlineKeyboardMarkup:
        kb = [*self._show_card()]

        if self.page == 1:
            kb.append([InlineKeyboardButton(text='>>>', callback_data=f'{self.call}_next_notbrand_notmodel')])

        elif self.page == len(self.query):
            kb.append([InlineKeyboardButton(text='<<<', callback_data=f'{self.call}_previous_notbrand_notmodel')])
        
        else:
            kb.append([InlineKeyboardButton(text='>>>', callback_data=f'{self.call}_next_notbrand_notmodel')])
            kb.append([InlineKeyboardButton(text='<<<', callback_data=f'{self.call}_previous_notbrand_notmodel')])

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        return keyboard

    def _show_card(self) -> List:
        kb = []

        for data in self.query[self.pages[self.page][0]:self.pages[self.page][1]]:
            self.brand = data[0]

            kb.append([InlineKeyboardButton(text=str(data[1]), callback_data=f'{self.call}_stay_{self.brand}_-1')])

        return kb

class CardModel(CardAuto):
    '''КЛАСС СОЗДАНИЯ КАРТЫ МОДЕЛЕЙ'''
    def __init__(self, model:int | None, **kwargs):
        super().__init__(**kwargs)
        self.model = model

    def show_caption_model(self, query_model) -> Tuple:     
        return (f'''
        Модель: {query_model[0][1]}\nТип кузова: {query_model[0][2]}\nКоличество мест: {query_model[0][3]}\nДвигатель: {query_model[0][4]}
        ''', query_model[0][-2])

    def _show_card(self) -> List:
        kb = []

        for data in self.query[self.pages[self.page][0]:self.pages[self.page][1]]:
            self.brand = data[-1]
            self.model = data[1]

            kb.append([InlineKeyboardButton(text=str(data[1]), callback_data=f'{self.call}_stay_{self.brand}_{self.model}')])

        return kb

class CardUser(Card):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_option(self) -> List:
        kb = []
        option = ['Назначить админом', 'Снять с админки', 'Удалить пользователя']

        for opt in option:
            kb.append([InlineKeyboardButton(text=opt, callback_data=f'{self.call}_{opt}')])

        return kb

    def _show_card(self) -> List:
        kb = []

        for data in self.query[self.pages[self.page][0]:self.pages[self.page][1]]:
            kb.append([InlineKeyboardButton(text=str(data[1]), callback_data=f'{self.call}_stay_{str(data[1])}')])

        return kb