# This Python file uses the following encoding: utf-8
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


btn1 =KeyboardButton("Квадрат")
btn2 =KeyboardButton("Куб")
btn3 =KeyboardButton("Отправить свою локацию️ 🗺️", request_location=True)
botKbd = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).row(btn1,btn2)
botKbd.row(btn3)

botInlineKbd = InlineKeyboardMarkup(row_width=2)
btnsInline = [InlineKeyboardButton(text="Квадрат", callback_data="square"),
              InlineKeyboardButton(text="Куб", callback_data="cube"),
              InlineKeyboardButton(text="Отправить свою локацию️ 🗺", callback_data="location")]
botInlineKbd.add(*btnsInline)

botStopNotifyKbd = InlineKeyboardMarkup()
botStopNotifyKbd.add(InlineKeyboardButton(text="Отменить оповещения", callback_data="stop_notify"))
botStopNotifyKbd.add(InlineKeyboardButton(text="Найти лучшие курсы", callback_data="find_best"))

botStartNotifyKbd = InlineKeyboardMarkup()
botStartNotifyKbd.add(InlineKeyboardButton(text="Включить оповещения", callback_data="start_notify"))
