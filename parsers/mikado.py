# author Roganovich.R.M.

from parsers.basic import Basic
import config
from urllib.request import urlopen
import os
import log
from os.path import splitext
from zipfile import ZipFile
import csv
from loader import Loader

# получаем настройки приложения
config = config.getConfig()


class Mikado(Basic):
    name = "Mikado"
    suppliers_id = 52
    data = []
    email = {}
    # путь к каталогу с файлами
    filePathExtract = "files/Mikado/"
    # делитель CSV
    delimiter = ";"
    # пупустить строк в файле
    clearLine = 0
    # тип файла вложения
    parsertype = "zip"
    # тип файла прайса
    filetype = "csv"
    fileEncoding = "cp1251"

    pricesFiles = {"76": "https://polomkam.net/office/GetFile.asp?File=MikadoStock.zip&CLID=12370&PSW=xmmlra152",
                   "180": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=92&CLID=12370&PSW=xmmlra152",
                   "118": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=82&CLID=12370&PSW=xmmlra152",
                   "150": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=23&CLID=12370&PSW=xmmlra152",
                   "198": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=61&CLID=12370&PSW=xmmlra152",
                   "199": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=34&CLID=12370&PSW=xmmlra152"}

    # сопостовляем колонки в файле с назначениями полей
    colums = {"art": 1, "bra": 2, "price": 4, "quality": 5, "desc": 3, "art_sup": 0}

    def __init__(self):
        self.prepareDir()

    def prepareDir(self):
        self.basePath = config.get("path", "_DIR_")
        self.email['email_from'] = "polomkam.net"
        self.filePathExtract = os.path.join(self.basePath, self.filePathExtract)

    def downloadFiles(self):
        if (not os.path.exists(self.filePathExtract)):
            os.mkdir(self.filePathExtract)
        # скачиваем файлы прайса
        for file in self.pricesFiles:

            war_id = file
            path = self.pricesFiles[file]

            # получаем полный пусть сохранения
            pathExtract = os.path.join(self.filePathExtract, war_id)
            if (not os.path.exists(pathExtract)):
                os.mkdir(pathExtract)
            fileName = pathExtract + "/price.zip"
            # если этот файл уже есть удалить
            if os.path.exists(fileName):
                log.print_r('Удаляем старый файл ' + fileName)
                os.remove(fileName)
            log.print_r('Начал скачивание ' + path)
            # делаем запрос на получение архива
            url = urlopen(path)
            f = url.read()
            log.print_r('Копируем в ' + fileName)
            # создаем файл для записи результатов
            file = open(fileName, "wb")
            file.write(f)
            # закрываем файл
            file.close()

            # работа с архивом
            zip = ZipFile(fileName)
            log.print_r('Распаковываю архив ' + fileName)
            zip.extractall(pathExtract)
            zip.close()
            # удаляем архив после распаковки
            os.remove(fileName)

    # функция формирует путь файла, открывает его и работает построчно
    def workWidthFiles(self, warhouse_id):
        # назначаем склад для этого файла поставщика
        self.warhouse_id = str(warhouse_id)
        # получаем полный путь файла склада
        pathExtract = os.path.join(self.filePathExtract, self.warhouse_id)
        # находим все файлы прайсов в каталоге парсера поставщика
        files = os.listdir(pathExtract)
        # перебираем все найденные файлы
        for file in files:
            # получаем путь нахождения файла
            filePath = pathExtract + "/" + file
            # найти разрешение фапйла. что бы не грузил картинки и прочее
            # находим extension  файла
            extension = splitext(filePath)
            if (extension[1] in ['.csv']):
                log.print_r('Работаю с файлом ' + filePath)
                # создаем класс загрузчика
                loader = Loader(self)
                with open(filePath, 'r', newline='', encoding=self.fileEncoding) as file_obj:
                    reader = csv.reader(file_obj, delimiter=self.delimiter)
                    # проверка на целостность данных
                    i = 0
                    for row in reader:

                        i = i + 1
                        #log.print_r('Работаю со строкой ' + str(i) + ' ' + str(row))
                        # пропускаем первую строку
                        if (self.clearLine and i <= self.clearLine):
                            continue
                        if (len(row) < 5):
                            continue
                        # берем из строки только нужные столбцы
                        colData = self.prepareColumns(row)

                        if (len(colData) < 5):
                            continue
                        # проверяем данные
                        clearData = loader.validate(colData)
                        if (clearData):
                            # записываем в таблицу загрузки
                            loader.writerests(clearData)
                            # записываем в файл результата
                            loader.writer.writerows([clearData.values()])
                    loader.resultFile.close()
                    loader.closeWrite()

            # удаляем файл
            os.remove(filePath)
