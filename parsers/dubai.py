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


class Dubai(Basic):
	name = "Dubai"
	suppliers_id = 98
	warhouse_id = 151

	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Dubai/"
	# тип файла прайса
	filetype = "csv"
	parsertype = "zip"
	fileEncoding = "utf-8"
	# делитель CSV
	delimiter = "\t"
	# пупустить строк в файле
	clearLine = 0
	# если в прайсе нет остатков, то исспользуем свойство min_quality
	min_quality = 10

	# сопостовляем колонки в файле с назначениями полей
	colums ={"art": 0, "bra": 1, "price": 4, "quality": 2, "desc": 2, "art_sup":0}















