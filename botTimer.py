from botData import BotData
from botKeyboard import botStopNotifyKbd
from aiogram import Dispatcher


#Реализация таймера
async def  send_locko_moex_message(dp:Dispatcher,botData:BotData):
    for botUser in botData.botUsers :
        if botUser.notify:
            userId = botUser.id
            lockoStr, moexStr, cbStr = botData.getCBCurrencies_()
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
            await dp.bot.send_message(userId, lockoStr)


async def send_locko_message(dp: Dispatcher, botData: BotData):
    lockoStr,newData = botData.getLockoCurrencies()
    if newData:
        for botUser in botData.botUsers:
            if botUser.notify:
                userId = botUser.id
                await dp.bot.send_message(userId,'*Обновлен курс в Локо\-банке: *',parse_mode='MarkdownV2')
                await dp.bot.send_message(userId, lockoStr, reply_markup=botStopNotifyKbd)


async def noon_send_message(dp:Dispatcher,botData:BotData):
    for botUser in botData.botUsers:
        userId = botUser.id
        await dp.bot.send_message(userId ,"Куку!!! Полдень! Пора кушать!")

async def send_cb_message(dp: Dispatcher, botData: BotData):
    lockoStr, moexStr, cbStr = botData.getCBCurrencies_()
    for botUser in botData.botUsers:
        userId = botUser.id
        await dp.bot.send_message(userId, '*Курсы ЦБ на сегодня : *', parse_mode='MarkdownV2')
        await dp.bot.send_message(userId, cbStr)



