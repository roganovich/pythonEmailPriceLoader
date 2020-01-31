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
	# пупустить строк в файле
	clearLine = 1
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














