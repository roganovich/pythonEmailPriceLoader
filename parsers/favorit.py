# author Roganovich.R.M.

from parsers.basic import Basic
import config
import os
import log
import ftplib
import ssl

#import csv
#from loader import Loader

# получаем настройки приложения
config = config.getConfig()
class FavoritBasic(Basic):
    data = []
    email = {}
    # делитель CSV
    delimiter = ";"
    # пупустить строк в файле
    clearLine = 0
    # тип файла вложения
    parsertype = "file"
    # тип файла прайса
    filetype = "xlsx"


    # сопостовляем колонки в файле с назначениями полей
    colums = {"art": 1, "bra": 0, "price": 3, "quality": 4, "desc": 2, "art_sup": 1}

    def __init__(self):
        self.prepareDir()

    def prepareDir(self):
        self.basePath = config.get("path", "_DIR_")
        self.email['email_from'] = "ftp.favorit-parts.ru"
        self.filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        if (not os.path.exists(self.filePathExtract)):
            os.mkdir(self.filePathExtract)

    def downloadFiles(self):
        link = "ftp.favorit-parts.ru"
        user = "pavlenko"
        password = "mUDkXds7"

        log.print_r("Подключаюсь по FTP к " + link)
        ftps = ftplib.FTP_TLS()
        ftps.ssl_version = ssl.PROTOCOL_TLSv1

        ftp = ftplib.FTP(link)
        ftp.login(user, password)
        # Путь на нашем компьютере где сохранить файл.
        saveFile = self.filePathExtract +  self.fileName
        log.print_r("Сохраняю файл " + saveFile)
        with open(saveFile, 'wb') as f:
            ftp.retrbinary('RETR ' + self.fileName, f.write)
        ftp.quit()


class Favorit(FavoritBasic):
    name = "Favorit"
    suppliers_id = 35
    warhouse_id = 30
    fileName = "FAVORIT.xlsx"
    filePathExtract = "files/Favorit/"


class FavoritKRS(FavoritBasic):
    name = "FavoritKRS"
    suppliers_id = 122
    warhouse_id = 187
    fileName = "FAVORIT_KRS.xlsx"
    # путь к каталогу с файлами
    filePathExtract = "files/FavoritKRS/"
