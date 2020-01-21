# author Roganovich.R.M.
import os
from zipfile import ZipFile
import log
import csv
import config

# получаем настройки приложения
config = config.getConfig()

class Absparser:
    name = "ABS"
    suppliers_id = 16
    data = []
    filePath = ""
    # путь к каталогу с файлами
    filePathExtract = "files/ABS/"
    resultFileName = "adb_price.csv"
    # делитель CSV
    delimiter = "\t"
    # пупустить первую строку в файле
    firstLine = True

    # в файле ['Артикул', 'Бренд', 'Окончательная цена', 'Количество', 'Наименование номенклатуры', 'Полный артикул']
    # сопостовляем колонки в файле с назначениями полей
    colums =     {"art": 0, "bra": 1, "price": 2, "quality": 3}

    # 20	ABS-AUTO
    # 158	ABS
    # сопоставляем файлы и склады в базе
    unity = {
        #"ABS_AJUSA.txt":"1",
        #"ABS_Krasnodar.txt": "1",
        #"ABS_Krym_317.txt": "1",
        #"ABS_MercedesSochi.txt": "1",
        #"ABS_Valeo.txt": "1",

        "ABS_BOSCH.txt":"157",
        "ABS_Rostov.txt":"82",
        "ABS_Simferopol'.txt":"149",
        "ABS_Stavropol'.txt":"83",
        "ABS_Stolica.txt":"97",
        "ABS_Stolica_100_CS.txt":"122",

    }

    def upload(self):
        self.filePath = self.data['files']
        # если не существует дириктории создаем ее
        if not os.path.exists(self.filePathExtract):
            os.mkdir(self.filePathExtract)
        # распаковываем архивы
        self.zipdir()
        # работаем с файлами цен
        self.workWidthFiles()

    # функция работы с файлами
    def workWidthFiles(self):
        # находим все файлы прайсов в каталоге парсера поставщика
        files = os.listdir(self.filePathExtract)
        for file in files:
            priceFile = self.filePathExtract + file
            # проверяем файл по массиву соответствия
            if(file in self.unity):
                # читаем построчно файл
                self.csvReader(priceFile)
            log.print_r('Удаляю файл ' + priceFile)
            os.remove(priceFile)

    # функция распаковки архива
    def zipdir(self):
        # очистить каталог парсера
        self.clearPath()
        # проходим все архивы из письма и распаковываем их
        for file in self.filePath:
            if os.path.exists(file):
                # работа с архивом
                zip = ZipFile(file)
                log.print_r('Распаковываю архив ' + file)
                zip.extractall(self.filePathExtract)
                zip.close()
                # удаляем архив после распаковки
                os.remove(file)

    # функция очищает каталог от файлов их архива
    def clearPath(self):
        files = os.listdir(self.filePathExtract)
        for file in files:
            deleteFile = self.filePathExtract + file
            log.print_r('Удаляю файл ' + deleteFile)
            os.remove(deleteFile)

    # функция принимает путь файла, открывает его и работает построчно
    def csvReader(self,filePath):
        log.print_r('Подготавливаю файл ' + filePath)
        # открываем файл результата
        resultFilePath = config.get('resultsFolder') + self.resultFileName

        # очищаем файл результата
        if os.path.exists(resultFilePath):
            os.remove(resultFilePath)
        resultFile = open(resultFilePath, 'a',newline='', encoding='utf-8')
        writer = csv.writer(resultFile, delimiter=self.delimiter)
        with open(filePath, 'r', newline='', encoding='utf-8') as file_obj:
            reader = csv.reader(file_obj, delimiter=self.delimiter)
            i = 0
            for row in reader:
                i = i + 1
                # пропускаем первую строку
                if(self.firstLine == True and i == 1):
                    continue
                # берем из строки только нужные столбцы
                colData = self.prepareColumns(row)
                # записываем в файл результата
                writer.writerows([colData])

            resultFile.close()

    # функция из строки берет только нужные столбцы
    def prepareColumns(self, row):
        data = []
        # берем из строки только нужные столбцы
        for key in self.colums:
            data.append(row[self.colums[key]])
        return data











