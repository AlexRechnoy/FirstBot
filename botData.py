# This Python file uses the following encoding: utf-8
from pathlib import Path
from botUser import BotUser
import copy
import configparser
import sqlite3
import random
import os
from botWiki import BotWiki
import copy
import requests
from bs4 import BeautifulSoup
from currenciesData import getAllCurrencies
from aiogram.types import InputFile

ids_txt_file = "userIDs.txt"
config_file_path="botSettings.ini"
fail_emoji=(":ogre:",":goblin:",":skull:")

dollarIMG = '\U0001F4B5'
eurIMG    = '\U0001F4B6'
timeIMG   = '\U0000231B'

class BotData:
    def __init__(self):
        self.messageCounter=0
        self.val=0
        self.lockoUSD    = dict(sale=0.0, buy=0.0)
        self.lockoEUR    = dict(sale=0.0, buy=0.0)
        self.lockoUSDold = dict(sale=0.0, buy=0.0)
        self.lockoEURold = dict(sale=0.0, buy=0.0)
        self.botUsers=[]
        self.wiki = BotWiki()
        #self.id=[]
        self.conn = sqlite3.connect('botData.db')
        self.cur= self.conn.cursor()
        self.__readIDfromFile()
        self.__readConfig()
        self.__init_bd()
        #self.addMessageToDB()

    def __init_bd(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS botData(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            userID INTEGER NOT NULL,
                            time TEXT NOT NULL,
                            message TEXT NOT NULL);
                         """)
        self.conn.commit()

    def __readConfig(self):
        file=Path(config_file_path)
        config = configparser.ConfigParser()
        if file.exists():
            config.read(config_file_path)
            self.messageCounter=int(config['BotData']['MessageCounter'])

    def __readIDfromFile(self):
        file=Path(ids_txt_file)
        if file.exists():
            f = open(ids_txt_file,'r')
            lines=f.readlines()
            for line in lines:
                userId=int(line)
                print(userId)
                self.botUsers.append(BotUser(userId))
                #self.id.append(userId)
            f.close()

    def _getUserFromId(self,id):
        print('getUserFromId')
        print(id)
        for botUser in self.botUsers:
            if botUser.id==id:
                print('getUserFromId!!!')
                return botUser

    def userIDexists(self, id):
        exists=False
        for botUser in self.botUsers:
            if botUser.id==id:
                exists=True
        return exists

    def userIDs(self):
        IDs=[]
        for botUser in self.botUsers:
            IDs.append(botUser.id)
        return IDs

    def getFailEmoji(self):
        index=random.randint(0,len(fail_emoji)-1)
        return fail_emoji[index]

    def getUSD(self):
        h = {'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 107.0.0.0 Safari / 537.36'}
        url = 'https://www.banki.ru/products/currency/cash/moskva_i_oblast~/dolgoprudnyiy/'
        r = requests.get(url, headers=h)
        soup = BeautifulSoup(r.content, 'html.parser')
        s2 = soup.findAll('div', 'table-flex__cell table-flex__cell--without-padding padding-left-default')
        answer=[]
        for line in s2:
            answer.append(line.text)
        return answer

    def __parseCurrencies(self):
        def calcCurrency(currencyList):
            currenciesList=[]
            for currency in currencyList :
                currPropList=currency.findAll('td')
                currencyName = currPropList[0].find('a').text
                currencyVal  = currPropList[1].text
                currenciesList.append('{} = {}'.format(currencyName,currencyVal))
            return currenciesList
        h = {'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 107.0.0.0 Safari / 537.36'}
        url = 'https://www.banki.ru/products/currency/'
        r = requests.get(url, headers=h)
        soup = BeautifulSoup(r.content, 'html.parser')
        rate_section = soup.find('div', class_="cb-current-rates")
        rate_list = rate_section.findAll('tr', class_='cb-current-rates__list__item')
        CBList=calcCurrency(rate_list)
        #Курс биржи
        moex_section = soup.find('table', class_='standard-table standard-table--row-highlight rate-indicators-table')
        usd_rate_section = moex_section.find('tr', {'data-test': 'moex-online-usd-row'})
        USDPropList = usd_rate_section.findAll('td')
        moexList=[]
        moexList.append('\U0001F4B5  {} (время : {})'.format(USDPropList[2].text.strip(),USDPropList[1].text.strip()))
        eur_rate_section = moex_section.find('tr', {'data-test': 'moex-online-eur-row'})
        EURPropList = eur_rate_section.findAll('td')
        moexList.append('\U0001F4B6  {} (время : {})'.format(EURPropList[2].text.strip(), EURPropList[1].text.strip()))
        #Курc локо
        lockoList,newLockoData=self.__parseLocko()
        return CBList,moexList,lockoList,newLockoData

    def __parseLocko(self):
        def getImage(dCourse):
            if dCourse>0:
                return '\U00002705'
            else:
                return '\U0000274C'
        def getLockoDataStr(currencyIMG,currencyDist : dict, oldCourse : float):
            dCourse = currencyDist['buy'] - oldCourse
            if dCourse==0:
                lockoStr=currencyIMG+'  {} / {} '.format(currencyDist['sale'],currencyDist['buy'])
            else:
                lockoStr=currencyIMG+'  {} / {} {} {:.2f} руб'.format(currencyDist['sale'],
                                                                    currencyDist['buy'],
                                                                    getImage(dCourse),
                                                                    dCourse)
            return lockoStr
        # Курc локо
        url = 'https://www.banki.ru/products/currency/bank/locko-bank/usd/moskva/#bank-rates'
        h = {'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 107.0.0.0 Safari / 537.36'}
        r = requests.get(url, headers=h)
        soup = BeautifulSoup(r.content, 'html.parser')
        locko_section = soup.find('tbody', {'class': 'font-size-medium'})
        usd_section = locko_section.find('tr', {'class': 'bg-beige'})
        currPropList = usd_section.findAll('td')
        # USD
        self.lockoUSD['sale'] = float(currPropList[3].text.strip().replace(",","."))
        self.lockoUSD['buy']  = float(currPropList[4].text.strip().replace(",","."))
        lockoList = []
        lockoList.append(getLockoDataStr(dollarIMG,self.lockoUSD,self.lockoUSDold['buy']))
        #EUR
        eur_section = locko_section.findAll('tr')[1]
        currPropList = eur_section.findAll('td')
        self.lockoEUR['sale'] = float(currPropList[3].text.strip().replace(",","."))
        self.lockoEUR['buy']  = float(currPropList[4].text.strip().replace(",","."))
        lockoList.append(getLockoDataStr(eurIMG,self.lockoEUR, self.lockoEURold['buy']))
        lockoList.append(timeIMG+'  {}'.format(currPropList[5].text.strip()))
        #Записать старые значения
        if (self.lockoUSD != self.lockoUSDold) or (self.lockoEUR != self.lockoEURold):
            self.lockoEURold = copy.deepcopy(self.lockoEUR)
            self.lockoUSDold = copy.deepcopy(self.lockoUSD)
            newLockoData = True
        else:
            newLockoData = False

        return lockoList,newLockoData

    def getCBCurrencies_(self):
        cbList, moexList, lockoList,newLockoData = self.__parseCurrencies()
        lockoStr,moexStr,cbStr = '','',''
        for str in lockoList:
             lockoStr += '\n' + str
        for str in moexList:
            moexStr+='\n'+str
        for str in cbList :
            cbStr+='\n'+str
        return lockoStr,moexStr,cbStr

    def getLockoCurrencies(self):
        lockoList,newLockoData = self.__parseLocko()
        lockoStr=''
        for str in lockoList:
             lockoStr += '\n' + str
        return lockoStr,newLockoData

    def getRandomPhoto(self):
        photo_list=[]
        for file in os.listdir('img/'):
            photo_list.append('img/'+file)
        return  InputFile(photo_list[random.randint(0,len(photo_list)-1)])


    def writeIDtoFile(self):
        f = open(ids_txt_file,'w')
        for id in self.id:
            f.write("%s\n" % id);
        f.close()

    def writeSettingsToFile(self):
        config = configparser.ConfigParser()
        config['BotData'] = {'MessageCounter': self.messageCounter}
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)

    def addMessageToDB(self,userID,time,message):
        self.cur.execute("INSERT INTO botData (userID,time,message) VALUES(?,?,?) ",
                          (userID,time,message)
                         )
        self.conn.commit()

