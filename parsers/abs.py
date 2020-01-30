# author Roganovich.R.M.
import os
import log
import csv
import datetime
from loader import Loader
from parsers.basic import Basic
import config
# получаем настройки приложения
config = config.getConfig()


class Absparser(Basic):
	name = "ABS"
	suppliers_id = 16
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/ABS/"
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "csv"
	fileEncoding = "utf-8"
	# делитель CSV
	delimiter = "\t"
	# пупустить первую строку в файле
	firstLine = True
	# в файле ['Артикул', 'Бренд', 'Окончательная цена', 'Количество', 'Наименование номенклатуры', 'Полный артикул']
	# сопостовляем колонки в файле с назначениями полей
	colums ={"art": 0, "bra": 1, "price": 2, "quality": 3, "desc": 4, "art_sup":5}

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

	# функция принимает путь файла, открывает его и работает построчно
	def csvReader(self, file):
		filePath = self.filePathExtract + file
		log.print_r('Подготавливаю файл ' + filePath)
		# открываем файл результата
		# формируем имя файла результата для этого поставщика
		suppliers_id = str(self.suppliers_id)
		warhouse_id = str(self.unity[file])
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
		with open(filePath, 'r', newline='', encoding='utf-8') as file_obj:
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
		log.print_r('Удаляю файл ' + filePath)
		os.remove(filePath)













