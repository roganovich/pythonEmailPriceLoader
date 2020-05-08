# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Tavriyaauto(Basic):
	name = "Tavriyaauto"
	suppliers_id = 94
	warhouse_id = 143
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Tavriyaauto/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"
	fileEncoding = "utf-8"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 2, "bra": 4, "price": 6, "quality": 5, "desc":1, "art_sup":1}














