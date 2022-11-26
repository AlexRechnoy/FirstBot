import wikipedia
import re

class BotWiki():
    def __init__(self):
        wikipedia.set_lang("ru")

    def getWikiText(self, keyWord):
        ny = wikipedia.page(keyWord)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')  # Разделяем по точкам
        wikimas = wikimas[:-1]  # Отбрасываем всЕ после последней точки
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not ('==' in x):
                if (len((
                        x.strip())) > 3):  # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        print(wikitext2)
        return wikitext2