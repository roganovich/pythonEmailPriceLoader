# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Autorayparser(Basic):
	name = "Autoray"
	suppliers_id = 89
	warhouse_id = 125
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Autoray/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"
	fileEncoding = "utf-8"

	# в файле [КатНомер	Наименование	Производитель	Применяемость	Кроссы	Цена	Наличие]
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 2, "price": 5, "quality": 6, "desc":1, "art_sup":0}














