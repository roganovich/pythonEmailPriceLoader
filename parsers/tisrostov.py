# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Tisrostov(Basic):
	name = "Tisrostov"
	suppliers_id = 108
	warhouse_id = 166
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Tisrostov/"
	# пупустить строк в файле
	clearLine = 6
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "xls"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 3, "bra": 1, "price": 8, "quality": 10, "desc":2, "art_sup":3}














