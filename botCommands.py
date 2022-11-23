# This Python file uses the following encoding: utf-8
from aiogram import Bot,types
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from botData import BotData


async def cmd_help(message: types.Message):
    await message.reply('*Я могу ответить на следующие команды:\n*'
                        '/bear\n'
                        '/photo\n'
                        '/USD\n',
                         parse_mode='MarkdownV2')


async def cmd_start(message: types.Message):
    await message.reply('Привет!!!\nЭто мой первый бот на python\.'
                        '\nБуду считать квадраты целых чисел\.\n'
                        'Используй /help \, чтобы узнать доступные команды')
