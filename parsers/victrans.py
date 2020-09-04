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


class VictransPod(Basic):
	name = "VictransPod"
	suppliers_id = 9
	warhouse_id = 7

	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/VictransPod/"
	# тип файла прайса
	filetype = "csv"
	parsertype = "zip"
	fileEncoding = "utf-8"
	# делитель CSV
	delimiter = ";"
	# пупустить строк в файле
	clearLine = 1


	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 6, "quality": 3, "desc":2, "art_sup":1}

class VictransEkat(Basic):
	name = "VictransEkat"
	suppliers_id = 9
	warhouse_id = 173

	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/VictransEkat/"
	# тип файла прайса
	filetype = "csv"
	parsertype = "zip"
	fileEncoding = "utf-8"
	# делитель CSV
	delimiter = ";"
	# пупустить строк в файле
	clearLine = 1

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 6, "quality": 3, "desc":2, "art_sup":1}















