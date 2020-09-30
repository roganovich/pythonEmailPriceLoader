# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Apex(Basic):
	name = "Apex"
	suppliers_id = 127
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Apex/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 5, "quality": 3, "desc":2, "art_sup":1}
	unity = {
		"Севастополь":"193",
		"Москва":"194",
	}














