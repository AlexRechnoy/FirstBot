# This Python file uses the following encoding: utf-8
from pathlib import Path
from botUser import BotUser
import configparser
import sqlite3
import random
import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from aiogram.types import InputFile

ids_txt_file = "userIDs.txt"
config_file_path="botSettings.ini"
fail_emoji=(":ogre:",":goblin:",":skull:")

class BotData:
    def __init__(self):
        self.messageCounter=0
        self.val=0
        self.botUsers=[]
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

    def getUserFromId(self,id):
        print('getUserFromId')
        print(id)
        for botUser in self.botUsers:
            if botUser.id==id:
                print('getUserFromId!!!')
                return botUser

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

    def getCBCurrencies(self):
        def calcCurrency(currencyList):
            currenciesList=[]
            for currency in currencyList :
                currPropList=currency.findAll('td')
                currencyName = currPropList[0].find('a').text
                currencyVal  = currPropList[1].text
                currenciesList.append('{} = {}'.format(currencyName,currencyVal))
                print('{} = {}'.format(currencyName,currencyVal))
            return currenciesList
        h = {'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 107.0.0.0 Safari / 537.36'}
        url = 'https://www.banki.ru/products/currency/'
        r = requests.get(url, headers=h)
        soup = BeautifulSoup(r.content, 'html.parser')
        rate_section = soup.find('div', class_="cb-current-rates")
        rate_list = rate_section.findAll('tr', class_='cb-current-rates__list__item')
        CBList=calcCurrency(rate_list)
        #
        moex_section = soup.find('table', class_='standard-table standard-table--row-highlight rate-indicators-table')
        usd_rate_section = moex_section.find('tr', {'data-test': 'moex-online-usd-row'})
        USDPropList = usd_rate_section.findAll('td')
        moexList=[]
        moexList.append('{} = {} (время : {})'.format(USDPropList[0].text.strip(),USDPropList[2].text.strip(),USDPropList[1].text.strip()))
        eur_rate_section = moex_section.find('tr', {'data-test': 'moex-online-eur-row'})
        EURPropList = eur_rate_section.findAll('td')
        moexList.append('{} = {} (время : {})'.format(EURPropList[0].text.strip(), EURPropList[2].text.strip(), EURPropList[1].text.strip()))
        #
        url = 'https://www.banki.ru/products/currency/bank/locko-bank/usd/moskva/#bank-rates'
        r = requests.get(url, headers=h)
        soup = BeautifulSoup(r.content, 'html.parser')
        locko_section = soup.find('tbody', {'class': 'font-size-medium'})
        usd_section = locko_section.find('tr', {'class': 'bg-beige'})
        currPropList = usd_section.findAll('td')
        lockoList=[]
        lockoList.append('{} = {} / {} ( {})'.format(currPropList[0].text.strip(),
                                                          currPropList[3].text.strip(),
                                                          currPropList[4].text.strip(),
                                                          currPropList[5].text.strip()))

        eur_section = locko_section.findAll('tr')[1]
        currPropList = eur_section.findAll('td')
        lockoList.append(
            '{} = {} / {} ( {})'.format(currPropList[0].text.strip(),
                                             currPropList[3].text.strip(),
                                             currPropList[4].text.strip(),
                                             currPropList[5].text.strip()))

        return CBList,moexList,lockoList

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

