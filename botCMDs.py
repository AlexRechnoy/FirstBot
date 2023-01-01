from botData import BotData
from currenciesData import getAllCurrencies
from aiogram import Dispatcher,types

dollarIMG = '\U0001F4B5'
eurIMG    = '\U0001F4B6'
timeIMG   = '\U0000231B'

class BotCMD(BotData):
    #def __init__(self, dp : Dispatcher):
        #self.dp=dp

    #def cmdGetPhoto(self):
        #async def process_photo_command(message: types.Message):
        #    await self.dp.bot.send_photo(userID, photo=self.getRandomPhoto())

    def cmdGetAllCurrencies(self):
        """
        Ответ на команду "Показать все"
        """
        banksData = getAllCurrencies()
        banksData.sort(key=lambda banksData: banksData['eur''sale'])
        strList, str = [], ''
        strList.append('*Курсы покупки валюты в банках: *')
        index = 1
        for bankData in banksData:
            strList.append('{}){} {}{}  {}{}'.format(index, bankData['name'], eurIMG,
                                                     bankData['eur''sale'], dollarIMG,bankData['usd''sale']))
            index += 1
        for tekStr in strList:
            str += '\n' + tekStr
        return str

    def cmdGetBestCurrencies(self):
        """
        Ответ на команду "Найти лучшие курсы"
        """
        banksData=getAllCurrencies()
        banksData.sort(key=lambda banksData: banksData['eur''sale'])
        bestEUR=banksData[0]
        banksData.sort(key=lambda banksData: banksData['usd''sale'])
        bestUSD = banksData[0]
        strList,str=[],''
        strList.append('*Лучшие курсы обмена валют : *'.format(len(banksData)))
        strList.append('Нашел банков : {}'.format(len(banksData)))
        strList.append(dollarIMG + '  {}/{} ({})'.format(bestUSD['usd''buy'], bestUSD['usd''sale'], bestUSD['name']))
        strList.append(eurIMG   +'  {}/{} ({})'.format(bestEUR['eur''buy'],bestEUR['eur''sale'],bestEUR['name']))
        strList.append(timeIMG  +'  {}'.format(bestEUR['time']))
        for tekStr in strList:
             str += '\n' + tekStr
        return str

    def cmdNotify(self, userID, notify):
        """
        Ответ на команды "Включить/отключить опевещения"
        """
        self._getUserFromId(userID).notify = notify

botCMD=BotCMD()

