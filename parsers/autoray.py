# author Roganovich.R.M.
import os
import log
import csv
import xlrd
from loader import Loader
from parsers.basic import Basic
import config
import datetime
# получаем настройки приложения
config = config.getConfig()

class Autorayparser(Basic):
	name = "Autoray"
	suppliers_id = 89
	warhouse_id = 125
	data = []
	filePath = ""
	# путь к каталогу с файлами
	filePathExtract = "files/Autoray/"
	# делитель CSV
	delimiter = "\t"
	# пупустить первую строку в файле
	firstLine = True

	# в файле [КатНомер	Наименование	Производитель	Применяемость	Кроссы	Цена	Наличие]
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 2, "price": 5, "quality": 6, "desc":1, "art_sup":0}



	# функция работы с файлами
	def workWidthFiles(self):
		# находим все файлы прайсов в каталоге парсера поставщика
		files = os.listdir(self.filePathExtract)
		# перебираем все найденные файлы
		for file in files:
			# читаем построчно файл xls
			self.xlsReader(file)

	# функция принимает путь файла, открывает его и работает построчно
	def xlsReader(self,file):
		# получаем путь нахождения файла
		filePath = self.filePathExtract + file
		log.print_r('Подготавливаю файл ' + filePath)
		# открываем файл результата

		# формируем имя файла результата для этого поставщика
		suppliers_id = str(self.suppliers_id)
		warhouse_id = str(self.warhouse_id)
		dateCreate = str(datetime.datetime.today().strftime("%Y%m%d"))
		resultPath = config.get("email", "resultsFolder") + '/' + dateCreate + '/' + suppliers_id + '/' + warhouse_id + '/'

		# имя файла
		resultFileName = "price.csv"
		# если не существует дириктории создаем ее
		if(not os.path.exists(resultPath)):
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
		writer = csv.writer(resultFile, delimiter=self.delimiter)
		# создаем класс загрузчика
		loader = Loader(suppliers_id, warhouse_id)
		with open(filePath, 'r', newline='', encoding='utf-8') as file_obj:
			reader = csv.reader(file_obj, delimiter=self.delimiter)
			i = 0
			for row in range(sheet.nrows):
				i = i + 1
				# пропускаем первую строку
				if(self.firstLine == True and i == 1):
					continue
				# берем столбцы строки
				rowData = sheet.row_values(row)
				# берем из строки только нужные столбцы
				colData = self.prepareColumns(rowData)
				# записываем в файл результата
				writer.writerows([colData])
				#loader.writerests(colData)
			resultFile.close()
		log.print_r('Удаляю файл ' + filePath)
		os.remove(filePath)			













