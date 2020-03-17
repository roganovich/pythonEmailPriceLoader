# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config
import xml.etree.ElementTree as etree
# получаем настройки приложения
config = config.getConfig()
from loader import Loader

class Avtosputnik(Basic):
	name = "Avtosputnik"
	suppliers_id = 63
	warhouse_id = 90
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Avtosputnik/"
	# пупустить строк в файле
	clearLine = 10
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "xml"
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 1, "price": 3, "quality": 4, "desc":2, "art_sup":0}

	# функция принимает путь файла, открывает его и работает
	def xmlReader(self, file):
		filePathExtract = os.path.join(self.basePath, self.filePathExtract)
		filePath = filePathExtract + file
		log.print_r('Работаю с файлом xls ' + filePath)

		tree = etree.parse(filePath)
		root = tree.getroot()
		rowData = []
		# перерабатываем xml в массив
		i = 0
		xmlRows = root[3][0]
		for rows in xmlRows:
			i = i + 1
			if (i < self.clearLine):
				continue
			row = []
			for cels in rows:
				for cel in cels:
					row.append(str(cel.text))
			rowData.append(row)
		# создаем класс загрузчика
		loader = Loader(self)
		i = 0
		for row in rowData:
			i = i + 1
			# проверяем данные
			# берем из строки только нужные столбцы
			colData = self.prepareColumns(row)
			try:
				clearData = loader.validate(colData)
				if (len(colData) < 5):
					continue
				if (clearData):
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




