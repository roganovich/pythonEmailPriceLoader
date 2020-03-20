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


class Avtodel(Basic):
	name = "Avtodel"
	suppliers_id = 104
	warhouse_id = 161
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Avtodel/"
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"
	fileEncoding = "utf-8"
	# пупустить строк в файле
	clearLine = 0

	# сопостовляем колонки в файле с назначениями полей
	colums ={"art": 0, "bra": 2, "price": 4, "quality": 3, "desc": 1, "art_sup":0}















