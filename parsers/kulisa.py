# author Roganovich.R.M.

from parsers.basic import Basic
import config
import os
import log
import requests

# получаем настройки приложения
config = config.getConfig()
class Kulisa(Basic):
    data = []
    email = {}
    # делитель CSV
    delimiter = "\t"
    # пупустить строк в файле
    clearLine = 1
    # тип файла вложения
    parsertype = "file"
    # тип файла прайса
    filetype = "csv"


    # сопостовляем колонки в файле с назначениями полей
    colums = {"art": 1, "bra": 0, "price": 3, "quality": 4, "desc": 2, "art_sup": 1}

    def downloadFiles(self):
        link = "http://bahchisaray.myserv.top:44000/kulisa_ostatki.txt"
        # получаем путь сохранения файла из письма
        path = self.getParserPath()
        filePath = path + 'price.csv'
        print(filePath)
        exit()
        # сохраняем файл в папку для дальнейшей загрузки
        with open(filePath, 'wb') as handle:
            response = requests.get(link, stream=True)
            handle.write(block)





