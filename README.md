﻿# car_dealership_bot

# ФОРМАТЫ ВВОДА

username - имя пользователя

email - почта

password - пароль

owner - собственник авто (пример Hyundai)

brand - бренд под владением собственника (пример Hyundai -> KIA)

img - фотография

brand_id - ID бренда в таблице CAR, посмотреть их можно в #покажиавто

model - модель автомобиля (название)

type_of_body - тип автомобиля (седан, хэтчбек, универсал)

count_of_place - количество мест

type_of_engine - тип двигателя

specifications_id - ID модели

# АВТОРИЗАЦИЯ

#авторизация
username
password

ИЛИ

#авторизация
email
password

ИЛИ

#авторизация
username
password
email

# РЕГИСТРАЦИЯ

#регистрация
username
password
email

# ПОКАЗАТЬ АВТОМОБИЛЬ

#покажиавто

# ДОБАВИТЬ АВТОМОБИЛЬ

#добавитьавто
owner
brand
img

# УДАЛИТЬ АВТОМОБИЛЬ

#удалитьавто
brand_id

# ПОКАЗАТЬ МОДЕЛЬ

#покажимодель

# ДОБАВИТЬ МОДЕЛЬ

#добавитьмодель
model
type_of_body
count_of_place
type_of_engine
img
brand_id

# УДАЛИТЬ МОДЕЛЬ

#удалитьмодели
specifications_id

# ФОТОГРАФИИ

#photo
img
