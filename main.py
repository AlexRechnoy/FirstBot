from aiogram import Bot, Dispatcher, executor, types
#from aiogram.utils.markdown import text, bold, italic, code, pre
#from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.dispatcher.filters import Text
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from setuptools._distutils.command.config import config

from botKeyboard import botInlineKbd,botStartNotifyKbd
from botData import BotData
from botTimer import send_locko_message, send_locko_moex_message,noon_send_message
from botCommands import cmd_help, cmd_start
import config
import os
import re
import emoji
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('endproc', nargs='?')
    return parser


botData=BotData()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot) #Диспетчер — объект, занимающийся получением апдейтов от Telegram с последующим выбором хэндлера для обработки принятого апдейта.
dp.register_message_handler(cmd_help, commands="help")
dp.register_message_handler(cmd_start, commands="start")

#Реализация таймера
scheduler=AsyncIOScheduler()
scheduler.add_job(send_locko_message, "interval", minutes=60, args=(dp,botData))
scheduler.add_job(send_locko_moex_message, "interval", minutes=150, args=(dp,botData))
scheduler.add_job(noon_send_message, "cron",hour='12',minute='00', second='00',args=(dp,botData))
#

#message_handler — это декоратор, который реагирует на входящие сообщения и содержит в себе функцию ответа.
#Декоратор — это «обёртка» вокруг функций, позволяющая влиять на их работу без изменения кода самих функций.
#В нашем случае мы управляем функцией, считая команды пользователя;
#commands=['start'] — это команда, которая связана с декоратором и запускает вложенную в него функцию;


@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=botData.getRandomPhoto())

@dp.message_handler(commands=['USD'])
async def cmd_USD(message: types.Message):
    cbList,moexList,lockoList=botData.getCBCurrencies()
    await bot.send_message(message.from_user.id,
                           '*Курсы ЦБ на сегодня : *',
                           parse_mode='MarkdownV2')
    for str in cbList :
        await bot.send_message(message.from_user.id,str)
    await bot.send_message(message.from_user.id,
                           '*Биржевой курс : *',
                           parse_mode='MarkdownV2')
    for str in moexList:
        await bot.send_message(message.from_user.id,str)

    await bot.send_message(message.from_user.id,
                               '*Курс в Локо\-банке: *',
                               parse_mode='MarkdownV2')
    for str in lockoList:
        await bot.send_message(message.from_user.id,str)

@dp.message_handler(content_types=["photo"])
async def get_photo(message):
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(message.photo[-1].file_id)
    await message.photo[-1].download('img/'+file_info.file_path.split('photos/')[1])
    for file in os.listdir('img/'):
        print(file)

@dp.message_handler(Text(equals="Квадрат"))
async def send_2rd_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Число {} в квадрате = {}".format(float(botData.val),float(botData.val)*float(botData.val)),
                           reply_markup=types.ReplyKeyboardRemove())

@dp.callback_query_handler(text="square")
async def send_square(call: types.CallbackQuery):
    await call.message.answer("Число {} в квадрате = {}".format(float(botData.val),float(botData.val)*float(botData.val)))
    await call.answer()

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    reply = "ТЫ ЗДЕСЬ!!!\nШирота:  {}\nДолгота: {}".format(lat, lon)
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())

@dp.callback_query_handler(text="location")
async def send_cube(call: types.CallbackQuery):
    #lat = call.message.location.latitude
    #lon = call.message.location.longitude
    #reply = "ТЫ ЗДЕСЬ!!!\nШирота:  {}\nДолгота: {}".format(lat, lon)
    await call.message.answer('не могу обработать координаты!!!')


@dp.message_handler(Text(equals="Куб"))
async def send_3rd_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Число {} в кубе = {}".format(float(botData.val),float(botData.val)*float(botData.val)*float(botData.val)),
                           reply_markup=types.ReplyKeyboardRemove())

@dp.callback_query_handler(text="cube")
async def send_cube(call: types.CallbackQuery):
    await call.message.answer("Число {} в кубе = {}".format(float(botData.val),float(botData.val)*float(botData.val)*float(botData.val)))
    await call.answer()

@dp.callback_query_handler(text="stop_notify")
async def send_stop_notify(call: types.CallbackQuery):
    botData.getUserFromId(call.message.chat.id).notify=False
    await call.message.answer("Ну все! Больше тебе ничего не пришлю!!!(Оповещения отключены)",reply_markup=botStartNotifyKbd)
    await call.answer()

@dp.callback_query_handler(text="start_notify")
async def send_start_notify(call: types.CallbackQuery):
    botData.getUserFromId(call.message.chat.id).notify = True
    await call.message.answer("Начинаю спамит!!! (Оповещения включены)")
    await call.answer()

@dp.message_handler(commands=['bear'])
async def send_bear(message: types.Message):
    await bot.send_message(message.from_user.id,emoji.emojize(":bear:"))


@dp.message_handler()#Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message):
    print(message.text)
    botData.messageCounter+=1
    botData.writeSettingsToFile()
    botData.addMessageToDB(int(message.from_user.id),message.date,message.text)
    newID=-1

    if not botData.userIDexists(message.from_user.id):
        newID = message.from_user.id
        print('newID')
        botData.id.append(int(newID))
        botData.writeIDtoFile()

    #if message.from_user.id not in botData.id:
    #    newID=message.from_user.id
    #    botData.id.append(int(message.from_user.id))
    #    botData.writeIDtoFile()
    if re.match(r"^[0-9.\-]+$", message.text):
        botData.val=float(message.text)
        for botUser in botData.botUsers :
            userId=botUser.id
            if (newID!=-1) and (newID!=userId) :
                await bot.send_message(userId,"У меня новый пользователь с ID ={}".format(newID))
            if userId==message.from_user.id:
                await bot.send_message(userId,"Всего сообщений = {}".format(botData.messageCounter))
                await bot.send_message(userId,"Все пользователи = {}".format(botData.userIDs()))
            else:
                await bot.send_message(userId,"...Кто-то прислал мне число...Число {} в квадрате = {}".format(float(botData.val),float(botData.val)*float(botData.val)))

        #await message.answer("В какую степень возвести?", reply_markup=botKbd)
        await message.answer("В какую степень возвести?", reply_markup=botInlineKbd)
    else:
        await bot.send_message(message.from_user.id,
                               emoji.emojize(botData.getFailEmoji()))
        await bot.send_message(chat_id=message.from_user.id,
                               text="*'{}' \- Я не понимаю о чем ты\.\.\. Придется лезть в википедию \!\!\!*".format(message.text),
                               parse_mode='MarkdownV2')
        s=botData.wiki.getWikiText(str(message.text))
        await bot.send_message(message.from_user.id,s)

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    if not namespace.endproc:
        scheduler.start()
        executor.start_polling(dp, skip_updates=True)
