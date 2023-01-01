# This Python file uses the following encoding: utf-8
from aiogram import Bot,types
import emoji
import re
from botCMDs import botCMD
from botDispatcher import dp
from botKeyboard import botStartNotifyKbd, botStopNotifyKbd, botBanksKbd, botLocationKbd
import os

async def cmd_help(message: types.Message):
    await message.reply('*Я могу ответить на следующие команды:\n*'
                        '/bear\n'
                        '/photo\n'
                        '/currencies\n'
                        '/location\n',
                         parse_mode='MarkdownV2')

async def cmd_photo(message: types.Message):
    await dp.bot.send_photo(message.from_user.id, photo=botCMD.getRandomPhoto())

async def cmd_add_photo(message):
    file_info = await dp.bot.get_file(message.photo[-1].file_id)
    await message.photo[-1].download('img/'+file_info.file_path.split('photos/')[1])
    for file in os.listdir('img/'):
        print(file)

async def cmd_start(message: types.Message):
    await message.reply('Привет!!!\nЭто мой первый бот на python\.'
                        '\nБуду считать квадраты целых чисел\.\n'
                        'Используй /help \, чтобы узнать доступные команды')

async def cmd_bear(message: types.Message):
    await dp.bot.send_message(message.from_user.id,emoji.emojize(":bear:"))

async def callback_find_best(call: types.CallbackQuery):
    await call.message.answer(botCMD.cmdGetBestCurrencies(), parse_mode='Markdown')
    await call.answer()

async def callback_stop_notify(call: types.CallbackQuery):
    botCMD.cmdNotify(call.message.chat.id,False)
    await call.message.answer("Ну все! Больше тебе ничего не пришлю!!!(Оповещения отключены)",reply_markup=botStartNotifyKbd)
    await call.answer()

async def callback_start_notify(call: types.CallbackQuery):
    botCMD.cmdNotify(call.message.chat.id,True)
    await call.message.answer("Начинаю спамить!!! (Оповещения включены)",reply_markup=botStopNotifyKbd)
    await call.answer()

async def callback_show_all(call: types.CallbackQuery):
    await call.message.answer(botCMD.cmdGetAllCurrencies(), parse_mode='Markdown',reply_markup=botStopNotifyKbd)
    await call.answer()

async def cmd_currencies(message: types.Message):
    lockoStr,moexStr,cbStr=botCMD.getCBCurrencies_()
    await dp.bot.send_message(message.from_user.id,
                           '*Курсы ЦБ на сегодня : *',
                           parse_mode='MarkdownV2')
    await dp.bot.send_message(message.from_user.id, cbStr)

    await dp.bot.send_message(message.from_user.id,
                           '*Биржевой курс : *',
                           parse_mode='MarkdownV2')
    await dp.bot.send_message(message.from_user.id, moexStr)

    await dp.bot.send_message(message.from_user.id,
                               '*Курс в Локо\-банке: *',
                               parse_mode='MarkdownV2')
    await dp.bot.send_message(message.from_user.id, lockoStr , parse_mode='Markdown')

    await dp.bot.send_message(message.from_user.id, botCMD.cmdGetBestCurrencies(), parse_mode='Markdown', reply_markup= botBanksKbd)


async def cmd_any_words(message: types.Message):
    print(message.text)
    botCMD.messageCounter+=1
    botCMD.writeSettingsToFile()
    botCMD.addMessageToDB(int(message.from_user.id),message.date,message.text)
    newID=-1

    if not botCMD.userIDexists(message.from_user.id):
        newID = message.from_user.id
        print('newID')
        botCMD.id.append(int(newID))
        botCMD.writeIDtoFile()

    if re.match(r"^[0-9.\-]+$", message.text):
        botCMD.val=float(message.text)
        for botUser in botCMD.botUsers :
            userId=botUser.id
            if (newID!=-1) and (newID!=userId) :
                await dp.bot.send_message(userId,"У меня новый пользователь с ID ={}".format(newID))
            if userId==message.from_user.id:
                await dp.bot.send_message(userId,"Всего сообщений = {}".format(botCMD.messageCounter))
                await dp.bot.send_message(userId,"Все пользователи = {}".format(botCMD.userIDs()))
            else:
                await dp.bot.send_message(userId,"... Кто-то прислал  мне число...Число {} в квадрате = {}".format(float(botCMD.val),float(botCMD.val)*float(botCMD.val)))
        #await message.answer("В какую степень возвести?", reply_markup=botInlineKbd)
    else:
        await dp.bot.send_message(message.from_user.id,
                               emoji.emojize(botCMD.getFailEmoji()))
        await dp.bot.send_message(chat_id=message.from_user.id,
                               text="*'{}' \- Я не понимаю о чем ты\.\.\. Придется лезть в википедию \!\!\!*".format(message.text),
                               parse_mode='MarkdownV2')
        await dp.bot.send_message(message.from_user.id,botCMD.wiki.getWikiText(str(message.text)))
        await dp.bot.send_location(message.from_user.id,1,1)


async def cmd_request_location(message: types.Message):
    await dp.bot.send_message(message.from_user.id, 'Нажмите на кнопку, чтобы передать мне свою локацию', reply_markup=botLocationKbd)

async def cmd_process_location(message: types.Message):
    reply='Нет координат :((('
    if message.location is not None:
        lat = message.location.latitude
        lon = message.location.longitude
        reply = "Ваше местоположение : \nШирота:  {}\nДолгота: {}".format(lat, lon)
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())



