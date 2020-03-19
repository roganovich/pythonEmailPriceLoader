# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Mosteknorot(Basic):
	name = "Mosteknorot"
	suppliers_id = 21
	warhouse_id = 21
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Mosteknorot/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"
	fileEncoding = "utf-8"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 2, "bra": 1, "price": 7, "quality": 3, "desc":5, "art_sup":2}














