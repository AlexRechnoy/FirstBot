# This Python file uses the following encoding: utf-8
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


#btn1 =KeyboardButton("Квадрат")
#btn2 =KeyboardButton("Куб")
btn =KeyboardButton("Отправить свою локацию️ 🗺️", request_location=True)
botLocationKbd = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
botLocationKbd.row(btn)

botInlineKbd = InlineKeyboardMarkup(row_width=2)
btnsInline = [InlineKeyboardButton(text="Отправить свою локацию️ 🗺", callback_data="location")]
botInlineKbd.add(*btnsInline)

botStopNotifyKbd = InlineKeyboardMarkup()
botStopNotifyKbd.add(InlineKeyboardButton(text="Отменить оповещения", callback_data="stop_notify"))
botStopNotifyKbd.row(InlineKeyboardButton(text="Найти лучшие курсы", callback_data="find_best"),
                     InlineKeyboardButton(text="Показать все", callback_data="show_all") )

botBanksKbd = InlineKeyboardMarkup()
botBanksKbd.row(InlineKeyboardButton(text="Найти лучшие курсы", callback_data="find_best"),
                InlineKeyboardButton(text="Показать все", callback_data="show_all") )

botStartNotifyKbd = InlineKeyboardMarkup()
botStartNotifyKbd.add(InlineKeyboardButton(text="Включить оповещения", callback_data="start_notify"))
