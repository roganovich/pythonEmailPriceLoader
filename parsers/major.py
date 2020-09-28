# author Roganovich.R.M.
import os
import log
import urllib.request
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()


class Major(Basic):
	name = "Major"
	suppliers_id = 113
	warhouse_id = 170
	data = []
	email = {}
	# путь к каталогу с файлами
	filePathExtract = "files/Major/"
	# делитель CSV
	delimiter = "\t"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "csv"
	fileEncoding = "windows-1251"
	fileName = "price.csv"

	# сопостовляем колонки в файле с назначениями полей
	colums ={"art": 1, "bra": 0, "price": 3, "quality": 4, "desc": 2, "art_sup":1}

	def __init__(self):
		self.email['email_from'] = "ra.aamajor.ru"
		self.prepareDir()

	def prepareDir(self):
		self.basePath = config.get("path", "_DIR_")
		self.filePathExtract = os.path.join(self.basePath, self.filePathExtract)
		if (not os.path.exists(self.filePathExtract)):
			os.mkdir(self.filePathExtract)

	def downloadFiles(self):
		link = "ftp://opt3:gHfV5V1h@ra.aamajor.ru/parts_major.txt"

		log.print_r("Подключаюсь по FTP к " + link)
		# Путь на нашем компьютере где сохранить файл.
		saveFile = self.filePathExtract + self.fileName
		log.print_r("Сохраняю файл " + saveFile)

		with urllib.request.urlopen(link) as response, open(saveFile, 'wb') as out_file:
			data = response.read()  # a `bytes` object
			out_file.write(data)








