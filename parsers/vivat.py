# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Vivat(Basic):
	name = "Vivat"
	suppliers_id = 129
	warhouse_id = 196
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Vivat/"
	# пупустить строк в файле
	clearLine = 2
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 2, "bra": 1, "price": 5, "quality": 4, "desc":3, "art_sup":2}














