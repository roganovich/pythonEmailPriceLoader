# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Voltag(Basic):
	name = "Voltag"
	suppliers_id = 112
	warhouse_id = 169
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Voltag/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"
	fileEncoding = "utf-8"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 3, "price": 6, "quality": 5, "desc":4, "art_sup":1}














