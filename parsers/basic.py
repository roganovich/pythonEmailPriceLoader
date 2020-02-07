# author Roganovich.R.M.
import os
import sys
from zipfile import ZipFile
import log
from os.path import splitext
import config
import datetime
import csv
import xlrd
from loader import Loader
# получаем настройки приложения
config = config.getConfig()
# устанавливаем максимальную длину строки csv
csv.field_size_limit(sys.maxsize)
class Basic:

    def __init__(self,email):
        self.email = email
        self.prepareDir()

    # функция работы с файлами
    def workWidthFiles(self):
        # находим все файлы прайсов в каталоге парсера поставщика
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        files = os.listdir(filePathExtract)
        # перебираем все найденные файлы
        for file in files:
            # получаем путь нахождения файла
            filePath = filePathExtract + file
            if os.path.exists(filePath):
                # читаем построчно файл xls
                if(self.filetype == "xls"):
                    self.xlsReader(file)
                # читаем построчно файл csv
                if (self.filetype == "csv"):
                    self.csvReader(file)
                log.print_r('Удаляю файл ' + filePath)
                os.remove(filePath)


    # очистка мусора из каталога
    def clearDir(self):
        # очищаем папку от мусора
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        files = os.listdir(filePathExtract)
        for file in files:
            # получаем полный путь к файлу
            findFile = filePathExtract + file
            if os.path.exists(findFile):
                log.print_r("Удаляю " + findFile)
                os.remove(findFile)

    def defGetResultFolder(self):
        # формируем имя файла результата для этого поставщика
        suppliers_id = str(self.suppliers_id)
        dateCreate = str(datetime.datetime.today().strftime("%Y%m%d"))
        path = config.get("email", "resultsFolder") + '/' + dateCreate + '/' + suppliers_id + '/'
        result = os.path.join(self.basePath, path)
        return result

    # подготавливаем базовые директории
    def prepareDir(self):
        self.basePath = config.get("path", "_DIR_")
        # если не существует дириктории создаем ее
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        if (not os.path.exists(filePathExtract)):
            os.mkdir(filePathExtract)

    # начинаем загрузку файла
    def upload(self):
        # если не существует дириктории создаем ее
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        if (not os.path.exists(filePathExtract)):
            os.mkdir(filePathExtract)

        if(self.parsertype == "zip"):
            # распаковываем zip архивы
            self.zipdir()
        if (self.parsertype == "rar"):
            # распаковываем rar архивы
            self.unrardir()
        # работаем с файлами цен
        self.workWidthFiles()

    # функция распаковки rar архива
    def unrardir(self):
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        files = os.listdir(filePathExtract)
        for file in files:
            # получаем полный путь к файлу
            findFile = filePathExtract + file
            if os.path.exists(findFile):
                # находим extension  файла
                extension = splitext(findFile)
                # если это архив распаковываем
                if(extension[1] == ".rar"):
                    os.system("unrar e " + findFile + " " + filePathExtract)
                    os.remove(findFile)


    # функция распаковки zip архива
    def zipdir(self):
        # проходим все архивы из письма и распаковываем их
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        files = os.listdir(filePathExtract)
        for file in files:
            # получаем полный путь к файлу
            findFile = filePathExtract + file
            if os.path.exists(findFile):
                # находим extension  файла
                extension = splitext(findFile)
                # если это архив распаковываем
                if(extension[1] == ".zip"):
                    # работа с архивом
                    zip = ZipFile(findFile)
                    log.print_r('Распаковываю архив ' + findFile)
                    zip.extractall(filePathExtract)
                    zip.close()
                    # удаляем архив после распаковки
                    os.remove(findFile)

    # функция из строки берет только нужные столбцы
    def prepareColumns(self, row):
        data = []
        # берем из строки только нужные столбцы
        for key in self.colums:
            data.append(row[self.colums[key]])
        return data

    # функция принимает путь файла, открывает его и работает построчно
    def xlsReader(self, file):
        # получаем путь нахождения файла
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        filePath = filePathExtract + file
        log.print_r('Подготавливаю файл ' + filePath)

        # создаем класс загрузчика
        loader = Loader(self)
        # начинаем работать с xls
        rb = xlrd.open_workbook(filePath, formatting_info=True)
        # открываем книгу
        sheet = rb.sheet_by_index(0)

        with open(filePath, 'r', newline='', encoding='utf-8') as file_obj:
            i = 0
            for row in range(sheet.nrows):
                i = i + 1
                # пропускаем первую строку
                if (self.clearLine and i <= self.clearLine):
                    continue
                # берем столбцы строки
                rowData = sheet.row_values(row)
                # берем из строки только нужные столбцы
                colData = self.prepareColumns(rowData)

                # записываем в таблицу загрузки
                loader.writerests(colData)
                # записываем в файл результата
                loader.writer.writerows([colData])
            loader.resultFile.close()
            loader.closeWrite()

    # функция принимает путь файла, открывает его и работает построчно
    def csvReader(self, file):
        # находим все файлы прайсов в каталоге парсера поставщика
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        filePath = filePathExtract + file
        log.print_r('Подготавливаю файл ' + filePath)
        # открываем файл результата
        # формируем имя файла результата для этого поставщика
        if(hasattr(self, 'unity')):
            if(file in self.unity):
                self.warhouse_id = str(self.unity[file])
            else:
                return False
        elif(hasattr(self, 'warhouse_id')):
            self.warhouse_id = str(self.warhouse_id)

        if(self.warhouse_id == 0):
            log.print_r('Не нашел склад для загрузки')
            return False
        # создаем класс загрузчика
        loader = Loader(self)
        with open(filePath, 'r', newline='', encoding=self.fileEncoding) as file_obj:
            reader = csv.reader(file_obj, delimiter=self.delimiter)
            i = 0
            for row in reader:
                i = i + 1
                # пропускаем первую строку
                if (self.clearLine  and i <= self.clearLine):
                    continue
                # берем из строки только нужные столбцы
                colData = self.prepareColumns(row)

                # записываем в таблицу загрузки
                loader.writerests(colData)
                # записываем в файл результата
                loader.writer.writerows([colData])
            loader.resultFile.close()
            loader.closeWrite()

    # проверка. нужно ли грузить это письмо. ищем каталог результата в котором учитываетьс дата, склад, поставщик
    def needToLoad(self):
        if os.path.exists(self.defGetResultFolder()):
            return False
        return True

    # получаем названия парсера, она же папка для регультата
    def getParserPath(self):
        self.clearDir()
        path = os.path.join(self.basePath, self.filePathExtract)
        return path


