# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Kyariz(Basic):
	name = "Kyariz"
	suppliers_id = 51
	warhouse_id = 73
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Kyariz/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"
	fileEncoding = "utf-8"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 3, "price": 4, "quality": 2, "desc":1, "art_sup":0}














