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


class RadialPlus(Basic):
	name = "RadialPlus"
	suppliers_id = 73
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/RadialPlus/"
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"
	# пупустить строк в файле
	clearLine = 6
	# сопостовляем колонки в файле с назначениями полей
	colums ={"art": 1, "bra": 2, "price": 5, "quality": 7, "desc": 3, "art_sup":1}

	# сопоставляем файлы и склады в базе
	unity = {
		"шины лето":"174",
		"шины зима":"174",
		"шины всесезон":"174",
	}














