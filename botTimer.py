# This Python file uses the following encoding: utf-8
from aiogram import Dispatcher
from botData import BotData
import emoji

#import asyncio
#import aioschedule


#Реализация таймера
async def send_locko_moex_message(dp:Dispatcher,botData:BotData):
    for userId in botData.id :
        cbList, moexList, lockoList = botData.getCBCurrencies()
        await dp.bot.send_message(userId,"\U0001F4B5")
        await dp.bot.send_message(userId,
                                  '*Напоминаю актуальные курсы  : *',
                                  parse_mode='MarkdownV2')
        await dp.bot.send_message(userId,
                                  '*Биржевой курс : *',
                                  parse_mode='MarkdownV2')
        for str in moexList:
            await dp.bot.send_message(userId, str)

        await dp.bot.send_message(userId,
                                  '*Курс в Локо\-банке: *',
                                  parse_mode='MarkdownV2')
        for str in lockoList:
            await dp.bot.send_message(userId, str)

async def send_locko_message(dp: Dispatcher, botData: BotData):
    for userId in botData.id:
        cbList, moexList, lockoList = botData.getCBCurrencies()
        await dp.bot.send_message(userId, "\U0001F4B5")
        await dp.bot.send_message(userId,'*Курс в Локо\-банке: *',parse_mode='MarkdownV2')
        for str in lockoList:
            await dp.bot.send_message(userId, str)


        #await dp.bot.send_message(userId,"Буду слать это сообщение каждые 6666 секунд")

async def noon_send_message(dp:Dispatcher,botData:BotData):
    for userId in botData.id :
        await dp.bot.send_message(userId ,"Куку!!! Полдень! Пора кушать!")



