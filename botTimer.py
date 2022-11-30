# This Python file uses the following encoding: utf-8
from aiogram import Dispatcher
from botData import BotData
from botKeyboard import botStopNotifyKbd
import emoji

#import asyncio
#import aioschedule


#Реализация таймера
async def send_locko_moex_message(dp:Dispatcher,botData:BotData):
    for botUser in botData.botUsers :
        if botUser.notify:
            userId = botUser.id
            #cbList, moexList, lockoList = botData.getCBCurrencies()
            lockoStr, moexStr, cbStr = botData.getCBCurrencies_()
            await dp.bot.send_message(userId,"\U0001F4B5")
            await dp.bot.send_message(userId,
                                  '*Напоминаю актуальные курсы  : *',
                                  parse_mode='MarkdownV2')

            await dp.bot.send_message(userId,
                                  '*Биржевой курс : *',
                                  parse_mode='MarkdownV2')
            await dp.bot.send_message(userId, moexStr)

            await dp.bot.send_message(userId,
                                  '*Курс в Локо\-банке: *',
                                  parse_mode='MarkdownV2')
            await dp.bot.send_message(message.from_user.id, lockoStr)


async def send_locko_message(dp: Dispatcher, botData: BotData):
    for botUser in botData.botUsers:
        if botUser.notify:
            userId = botUser.id
            lockoStr, moexStr, cbStr = botData.getCBCurrencies_()
            #cbList, moexList, lockoList = botData.getCBCurrencies()
            await dp.bot.send_message(userId, "\U0001F4B5")
            await dp.bot.send_message(userId,'*Курс в Локо\-банке: *',parse_mode='MarkdownV2')

            if botUser.notify:
                await dp.bot.send_message(userId, lockoStr, reply_markup=botStopNotifyKbd)
            #index=0
            # str in lockoList:
            #    if index==(len(lockoList)-1):
            #        if botUser.notify:
            #            await dp.bot.send_message(userId, str, reply_markup=botStopNotifyKbd)
            #    else:
            #        await dp.bot.send_message(userId, str)
            #    index+=1





        #await dp.bot.send_message(userId,"Буду слать это сообщение каждые 6666 секунд")

async def noon_send_message(dp:Dispatcher,botData:BotData):
    for botUser in botData.botUsers:
        userId = botUser.id
        await dp.bot.send_message(userId ,"Куку!!! Полдень! Пора кушать!")



