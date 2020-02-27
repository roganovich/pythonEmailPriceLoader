# author Roganovich.R.M.

from parsers.basic import Basic
import config
from urllib.request import urlopen
import os
import log
from zipfile import ZipFile

# получаем настройки приложения
config = config.getConfig()

class Mikado(Basic):
	name = "Mikado"
	suppliers_id = 52
	data = []
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
	fileEncoding = "windows-1251"

	pricesFiles = {"76": "https://polomkam.net/office/GetFile.asp?File=MikadoStock.zip&CLID=12370&PSW=xmmlra152",
			 "180": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=92&CLID=12370&PSW=xmmlra152",
			 "118": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=82&CLID=12370&PSW=xmmlra152",
			 "150": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=23&CLID=12370&PSW=xmmlra152",
			 "198": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=61&CLID=12370&PSW=xmmlra152",
			 "199": "https://polomkam.net/office/GetFile.asp?File=MikadoStockReg.zip&regID=34&CLID=12370&PSW=xmmlra152"}

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 2, "price": 4, "quality": 5, "desc":3, "art_sup":0}

	def downloadFiles(self):
		basePath = config.get("path", "_DIR_")
		self.filePathExtract = os.path.join(basePath, self.filePathExtract)

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

	def workWidthFiles(self):
		log.print_r('Копируем в ')
















