# author Roganovich.R.M.
import os
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
class Basic:

    def __init__(self):
        self.prepareDir()

    # функция работы с файлами
    def workWidthFiles(self):
        # находим все файлы прайсов в каталоге парсера поставщика
        files = os.listdir(self.filePathExtract)
        # перебираем все найденные файлы
        for file in files:
            # получаем путь нахождения файла
            filePath = self.filePathExtract + file
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
        files = os.listdir(self.filePathExtract)
        for file in files:
            # получаем полный путь к файлу
            findFile = self.filePathExtract + file
            if os.path.exists(findFile):
                log.print_r("Удаляю " + findFile)
                os.remove(findFile)

    def defGetResultFolder(self):
        # формируем имя файла результата для этого поставщика
        suppliers_id = str(self.suppliers_id)
        dateCreate = str(datetime.datetime.today().strftime("%Y%m%d"))
        return config.get("email", "resultsFolder") + '/' + dateCreate + '/' + suppliers_id + '/'

    # подготавливаем базовые директории
    def prepareDir(self):
        # если не существует дириктории создаем ее
        if (not os.path.exists(self.filePathExtract)):
            os.mkdir(self.filePathExtract)

    # начинаем загрузку файла
    def upload(self):
        # если не существует дириктории создаем ее
        if (not os.path.exists(self.filePathExtract)):
            os.mkdir(self.filePathExtract)

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
        files = os.listdir(self.filePathExtract)
        for file in files:
            # получаем полный путь к файлу
            findFile = self.filePathExtract + file
            if os.path.exists(findFile):
                # находим extension  файла
                extension = splitext(findFile)
                # если это архив распаковываем
                if(extension[1] == ".rar"):
                    os.system("unrar e " + findFile + " " + self.filePathExtract)
                    os.remove(findFile)


    # функция распаковки zip архива
    def zipdir(self):
        # проходим все архивы из письма и распаковываем их
        files = os.listdir(self.filePathExtract)
        for file in files:
            # получаем полный путь к файлу
            findFile = self.filePathExtract + file
            if os.path.exists(findFile):
                # находим extension  файла
                extension = splitext(findFile)
                # если это архив распаковываем
                if(extension[1] == ".zip"):
                    # работа с архивом
                    zip = ZipFile(findFile)
                    log.print_r('Распаковываю архив ' + findFile)
                    zip.extractall(self.filePathExtract)
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
        filePath = self.filePathExtract + file
        log.print_r('Подготавливаю файл ' + filePath)
        # открываем файл результата

        # формируем имя файла результата для этого поставщика
        suppliers_id = str(self.suppliers_id)
        warhouse_id = str(self.warhouse_id)
        dateCreate = str(datetime.datetime.today().strftime("%Y%m%d"))
        resultPath = config.get("email",
                                "resultsFolder") + '/' + dateCreate + '/' + suppliers_id + '/' + warhouse_id + '/'

        # имя файла
        resultFileName = "price.csv"
        # если не существует дириктории создаем ее
        if (not os.path.exists(resultPath)):
            log.print_r('Создаю директорию ' + resultPath)
            os.makedirs(resultPath)
        # путь к записи файла
        resultFilePath = resultPath + resultFileName

        # если не существует дириктории результатов создаем ее
        if not os.path.exists(config.get("email", "resultsFolder")):
            os.mkdir(config.get("email", "resultsFolder"))
        # очищаем файл результата
        if os.path.exists(resultFilePath):
            os.remove(resultFilePath)

        # начинаем работать с xls
        rb = xlrd.open_workbook(filePath, formatting_info=True)
        # открываем книгу
        sheet = rb.sheet_by_index(0)

        # открываем файл результата
        resultFile = open(resultFilePath, 'a', newline='', encoding='utf-8')
        writer = csv.writer(resultFile, delimiter='\t')
        # создаем класс загрузчика
        loader = Loader(suppliers_id, warhouse_id)
        with open(filePath, 'r', newline='', encoding='utf-8') as file_obj:
            i = 0
            for row in range(sheet.nrows):
                i = i + 1
                # пропускаем первую строку
                if (self.firstLine == True and i == 1):
                    continue
                # берем столбцы строки
                rowData = sheet.row_values(row)
                # берем из строки только нужные столбцы
                colData = self.prepareColumns(rowData)
                # записываем в файл результата
                writer.writerows([colData])
            # loader.writerests(colData)
            resultFile.close()

    # функция принимает путь файла, открывает его и работает построчно
    def csvReader(self, file):
        warhouse_id = 0
        filePath = self.filePathExtract + file
        log.print_r('Подготавливаю файл ' + filePath)
        # открываем файл результата
        # формируем имя файла результата для этого поставщика
        suppliers_id = str(self.suppliers_id)
        if(hasattr(self, 'unity')):
            if(file in self.unity):
                warhouse_id = str(self.unity[file])
        elif(hasattr(self, 'warhouse_id')):
            warhouse_id = str(self.warhouse_id)

        if(warhouse_id == 0):
            log.print_r('Не нашел склад для загрузки')
            return False

        dateCreate = str(datetime.datetime.today().strftime("%Y%m%d"))
        # формируем имя дириктории файла результата
        resultPath = config.get("email",
                                "resultsFolder") + '/' + dateCreate + '/' + suppliers_id + '/' + warhouse_id + '/'
        # имя файла
        resultFileName = "price.csv"
        # если не существует дириктории создаем ее
        if (not os.path.exists(resultPath)):
            log.print_r('Создаю директорию ' + resultPath)
            os.makedirs(resultPath)
        # путь к записи файла
        resultFilePath = resultPath + resultFileName
        # если не существует дириктории результатов создаем ее
        if not os.path.exists(config.get("email", "resultsFolder")):
            os.mkdir(config.get("email", "resultsFolder"))
        # очищаем файл результата
        if os.path.exists(resultFilePath):
            os.remove(resultFilePath)
        resultFile = open(resultFilePath, 'a', newline='', encoding='utf-8')
        writer = csv.writer(resultFile, delimiter=self.delimiter)
        # создаем класс загрузчика
        loader = Loader(suppliers_id, warhouse_id)
        with open(filePath, 'r', newline='', encoding=self.fileEncoding) as file_obj:
            reader = csv.reader(file_obj, delimiter=self.delimiter)
            i = 0
            for row in reader:
                i = i + 1
                # пропускаем первую строку
                if (self.firstLine == True and i == 1):
                    continue
                # берем из строки только нужные столбцы
                colData = self.prepareColumns(row)
                # записываем в файл результата
                writer.writerows([colData])
            # loader.writerests(colData)

            resultFile.close()

    # проверка. нужно ли грузить это письмо. ищем каталог результата в котором учитываетьс дата, склад, поставщик
    def needToLoad(self, ):
        if os.path.exists(self.defGetResultFolder()):
            return False
        return True

    # получаем названия парсера, она же папка для регультата
    def getParserPath(self):
        self.clearDir()
        return self.filePathExtract


