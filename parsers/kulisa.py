# author Roganovich.R.M.

from parsers.basic import Basic
import config
import os
import log
import requests

# получаем настройки приложения
config = config.getConfig()
class Kulisa(Basic):
    name = "Kulisa"
    suppliers_id = 105
    warhouse_id = 162
    data = []
    # путь к каталогу с файлами
    filePathExtract = "files/Kulisa/"
    data = []
    # делитель CSV
    delimiter = "\t"
    # пупустить строк в файле
    clearLine = 0
    # тип файла вложения
    parsertype = "file"
    # тип файла прайса
    filetype = "csv"
    # сопостовляем колонки в файле с назначениями полей
    colums = {"art": 0, "bra": 2, "price": 4, "quality": 1, "desc": 3, "art_sup": 10

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





