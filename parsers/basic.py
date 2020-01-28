# author Roganovich.R.M.
import os
from zipfile import ZipFile
import log
from os.path import splitext
import config
import datetime
# получаем настройки приложения
config = config.getConfig()

class Basic:

    def __init__(self):
        self.prepareDir()

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
        # распаковываем архивы
        self.zipdir()
        # работаем с файлами цен
        self.workWidthFiles()

    # функция распаковки архива
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