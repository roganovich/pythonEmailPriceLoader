# author Roganovich.R.M.
import os
import sys
from zipfile import ZipFile
import log
from os.path import splitext
import config
import datetime
import csv
import pandas as pd
import xlrd
from loader import Loader

# получаем настройки приложения
config = config.getConfig()
# устанавливаем максимальную длину строки csv
csv.field_size_limit(sys.maxsize)
class Basic:

    def __init__(self):
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
            # найти разрешение фапйла. что бы не грузил картинки и прочее
            # находим extension  файла
            extensionRow = splitext(filePath)
            extension = extensionRow[1]
            # автоматическое определение расширения файла
            if (self.filetype == 'auto'):
                filetype = extension.replace('.', '')
            else:
                filetype = self.filetype

            if(filetype in ['csv','xls', 'xlsx', 'txt', 'xml']):
                if os.path.exists(filePath):
                    # читаем построчно файл xls
                    if(filetype == "xls"):
                        self.xlsReader(file)
                    if (filetype == "xlsx"):
                        # меняем разрещшение файла xls на xlsx
                        if (extension == ".xls"):
                            filePathOld = filePath
                            file = file.replace('.xls', '.xlsx')
                            filePath = filePathExtract + file
                            os.rename(filePathOld, filePath)
                        self.xlsxReader(file)
                    # читаем построчно файл csv
                    if (filetype == "csv"):
                        self.csvReader(file)
                    # читаем  файл xml
                    if (filetype == "xml"):
                        self.xmlReader(file)
                else:
                    log.print_r('Не нашел файл ' + filePath)
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
        # дополнительно проверяем по складу
        if (hasattr(self, 'warhouse_id')):
            path = path + str(self.warhouse_id) + '/'

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
            # проверяем на наличие ключа в списке колонок строки
            try:
                d = str(row[self.colums[key]])
            except IndexError:
                d = '-'

            # если бошльше одной точки в строке то ничего не делаем
            if(d.count('.')==1):
                # если тип поля xls указан как номер то excl в конец добавляе .0 - мы это очищаем
                if (d[-2:] == '.0'):
                    data.append(d[0:-2])
                else:
                    data.append(d)
            else:
                data.append(d)
        return data

    # функция принимает путь файла, открывает его и работает построчно
    def xlsReader(self, file):
        # получаем путь нахождения файла
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        filePath = filePathExtract + file
        log.print_r('Работаю с файлом xls ' + filePath)


        # находим все файлы прайсов в каталоге парсера поставщика
        if(hasattr(self, 'unity')):
            self.warhouse_id = 0;
            for unity in self.unity:
                if (unity in file):
                    self.warhouse_id = str(self.unity[unity])
        elif(hasattr(self, 'warhouse_id')):
            self.warhouse_id = str(self.warhouse_id)

        if(self.warhouse_id == 0):
            log.print_r('Не нашел склад для загрузки')
            return False

        # создаем класс загрузчика
        loader = Loader(self)
        # начинаем работать с xls
        rb = xlrd.open_workbook(filePath, formatting_info=True)
        # открываем книгу
        sheet = rb.sheet_by_index(0)

        with open(filePath, 'r', newline='', encoding='utf-8', errors='ignore') as file_obj:
            i = 0
            for row in range(sheet.nrows):
                i = i + 1
                # пропускаем первую строку
                if (self.clearLine and i <= self.clearLine):
                    continue

                # берем столбцы строки
                rowData = sheet.row_values(row)
                if (len(rowData) < 5):
                    continue
                # берем из строки только нужные столбцы
                colData = self.prepareColumns(rowData)

                if (len(colData) < 5):
                    continue
                # проверяем данные
                clearData = loader.validate(colData)
                if (clearData):
                    try:
                        # записываем в таблицу загрузки
                        loader.writerests(clearData)
                        # записываем в файл результата
                        loader.writer.writerows([clearData.values()])
                    except:
                        log.print_r('Не смог записать строку в базу ' + str(i))
            log.print_r('Обработал ' + str(i) + " строк")

            loader.resultFile.close()
            loader.closeWrite()

    # функция принимает путь файла, открывает его и работает построчно
    def xlsxReader(self, file):
        # получаем путь нахождения файла
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        filePath = filePathExtract + file
        log.print_r('Работаю с файлом xlsx ' + filePath)

        # находим все файлы прайсов в каталоге парсера поставщика
        if(hasattr(self, 'unity')):
            self.warhouse_id = 0;
            for unity in self.unity:
                if (unity in file):
                    self.warhouse_id = str(self.unity[unity])
        elif(hasattr(self, 'warhouse_id')):
            self.warhouse_id = str(self.warhouse_id)

        if(self.warhouse_id == 0):
            log.print_r('Не нашел склад для загрузки')
            return False

        # создаем класс загрузчика
        loader = Loader(self)
        # начинаем работать с xls
        xls = pd.ExcelFile(filePath)
        # открываем книгу
        df = pd.read_excel(xls, sheet_name=0, skiprows=self.clearLine)
        i = 0
        for index, row in df.iterrows():
            i = i + 1
            rowData = []
            # превращаем строку в массив
            columns = row.tolist()
            k = 0
            # перебераем колонки
            for cell in columns:
                rowData.append(cell)
                k = k + 1

            # берем столбцы строки
            if(len(rowData) <4):
                continue
            #берем из строки только нужные столбцы
            colData = self.prepareColumns(rowData)

            if (len(colData) < 5):
                continue

            #проверяем данные
            clearData = loader.validate(colData)
            if(clearData):
                try:
                    # записываем в таблицу загрузки
                    loader.writerests(clearData)
                    # записываем в файл результата
                    loader.writer.writerows([clearData.values()])
                except:
                    log.print_r('Не смог записать строку в базу ' + str(i))

        log.print_r('Обработал ' + str(i) + " строк")
        loader.resultFile.close()
        loader.closeWrite()




    # функция принимает путь файла, открывает его и работает построчно
    def csvReader(self, file):
        # находим все файлы прайсов в каталоге парсера поставщика
        filePathExtract = os.path.join(self.basePath, self.filePathExtract)
        filePath = filePathExtract + file
        log.print_r('Работаю с файлом csv ' + filePath)
        # открываем файл результата
        # формируем имя файла результата для этого поставщика
        if(hasattr(self, 'unity')):
            self.warhouse_id = 0;
            if(file in self.unity):
                self.warhouse_id = str(self.unity[file])
            else:
                return False
        elif(hasattr(self, 'warhouse_id')):
            self.warhouse_id = str(self.warhouse_id)

        if (self.warhouse_id == 0):
            log.print_r('Не нашел склад для загрузки')
            return False
        # создаем класс загрузчика
        loader = Loader(self)
        with open(filePath, 'r', newline='', encoding=self.fileEncoding, errors='ignore') as file_obj:
            reader = csv.reader(file_obj, delimiter=self.delimiter)
            i = 0
            for row in reader:
                i = i + 1
                try:
                    row
                except:
                    log.print_r('Не смог прочитать строку ' + str(i))
                    continue
                # пропускаем первую строку
                if (self.clearLine  and i <= self.clearLine):
                    continue
                if(len(row) <5):
                    continue
                # берем из строки только нужные столбцы
                colData = self.prepareColumns(row)
                if (len(colData) < 5):
                    continue
                # проверяем данные
                try:
                    clearData = loader.validate(colData)
                    if(clearData):
                        try:
                            # записываем в таблицу загрузки
                            loader.writerests(clearData)
                            # записываем в файл результата
                            loader.writer.writerows([clearData.values()])
                        except:
                            log.print_r('Не смог записать строку в базу ' + str(i))
                except:
                    log.print_r('Не смог прочитать строку ' + str(i))
                    continue

            log.print_r('Обработал ' + str(i) + " строк")
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


